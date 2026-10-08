"""Vaihe 5: generoi data/site.json yhdistämällä upstream.json, annotations.json ja geo.json.

Mukaan vain annotoidut laitokset (aktiiviset annotaatiot, tasot 1 ja 2); orphaned-osio ohitetaan.
Generoitu tiedosto, ylikirjoitetaan joka kerta. Sivu lataa vain tämän.

Nimi: _verified-nimi jos saatavilla, muuten upstreamin nimi; pelkät versaalit (tai pienet) siistitään
luettavaan muotoon. Annotaation valinnainen kenttä display_name ohittaa tämän (esim. kun diakriitit
puuttuvat upstreamista: "Universitat" -> "Universität"). Verkko-osoitteet normalisoidaan
(https:// lisätään jos puuttuu); puuttuva osoite jää tyhjäksi (null), osoitteita ei arvata.
Annotaation valinnainen kenttä website_override korvaa upstreamin webpage-kentän, kun se on
todistettavasti väärä (esim. väärä TLD tai hyödytön yleisosoite); käytä säästeliäästi ja perustele notes-kentässä.
"""

import json
import sys
from collections import Counter
from datetime import date

from common import (CONTACTS, DISCIPLINES, GEO, NETWORKS, PROGRAMMES, SITE, SITE_PUBLIC, STRATEGIES, UPSTREAM, UPSTREAM_META, load_annotations, load_upstream, nice_case, normalize_url,
                    publish, today)

# Sivun tekstit ovat englanniksi; laitosten nimet säilyvät alkuperäiskielellä.
TIER_LABELS = {
    1: "Independent music institution",
    2: "Music unit of an arts university",
    3: "Music unit of a general university",
}
# Taso 3: kaikki AEC:n jäsenluettelon yksiköt on käyty läpi; nämä maat lisäksi kokonaan (rajausteksti kertoo tämän)
TIER3_COUNTRIES = ["Norway", "Serbia", "Sweden"]
# Partneritiedot eivät ole virallista tietoa: lähde ja vastuulauseke näytetään sivulla
PARTNER_SOURCE_NAME = "the exchange-destination list published by the University of the Arts Helsinki"
PARTNER_SOURCE = f"Partner information is taken from {PARTNER_SOURCE_NAME}."
DISCLAIMER = ("This page is an informal compilation of public data and is not an official publication of the "
              "European Commission or of any of the institutions listed.")
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
          "November", "December"]


def scope_text(fetched, items):
    """Aikasidonnainen rajausteksti (BRIEF.md): määrät lasketaan sivun datasta (ei käsin), hakupäivä, tasot,
    tason 3 kattavuus (AEC-jäsenet + TIER3_COUNTRIES kokonaan), Britannia ja Sveitsi."""
    d = date.fromisoformat(fetched)
    counts = Counter(i["tier"] for i in items)
    countries = len({i["country_code"] for i in items})
    full = f"{', '.join(TIER3_COUNTRIES[:-1])} and {TIER3_COUNTRIES[-1]}"
    return (
        f"The list has {len(items)} institutions in {countries} countries. Included are holders of the Erasmus Charter "
        "for Higher Education (ECHE) where music is an independent degree-awarding institution "
        f"({counts[1]}) or the music unit of an arts university ({counts[2]}), and music units of general universities "
        f"and universities of applied sciences whose parent holds the ECHE ({counts[3]}). "
        "For these units the coverage is based on the member list of the AEC (European Association of Conservatoires); "
        f"{full} have also been gone through in full, so elsewhere units that are not AEC members may still be missing. "
        f"Data retrieved {d.day} {MONTHS[d.month - 1]} {d.year} from the European Commission's ECHE list. "
        "Institutions in the United Kingdom and Switzerland will be added once they have been awarded an ECHE "
        "(association with Erasmus+ from 1 January 2027)."
    )


def build():
    up = load_upstream()
    ann, _orphaned = load_annotations()
    geo = json.loads(GEO.read_text(encoding="utf-8")) if GEO.exists() else {}
    meta_in = json.loads(UPSTREAM_META.read_text(encoding="utf-8")) if UPSTREAM_META.exists() else {}
    warnings = []

    items = []
    for key, a in ann.items():
        r = up.get(key)
        if r is None:
            warnings.append(f"{key}: annotaatio ilman upstream-riviä (pitäisi olla orphaned; aja update.py)")
            continue
        v = r.get("_verified") or {}
        cc = r["countryCodeIso"] or r["countryCode"]

        name_src = v.get("organisationLegalName") or r["organisationLegalName"]
        name = a.get("display_name") or nice_case(name_src, cc)
        # Musiikkiyksikkö ECHE-haltijan sisällä (taso 3, joskus 2): sivulla näytetään yksikkö, emo-organisaatio erikseen.
        # Emon katuosoite ei ole yksikön osoite, joten se jätetään pois, jos yksikkö on eri kaupungissa.
        unit = a.get("unit_name")
        parent_name = name if unit else None
        if unit:
            name = unit
        webpage_raw = a.get("website_override") or v.get("webpage") or r["webpage"]
        webpage = normalize_url(webpage_raw)
        if webpage_raw and not webpage:
            warnings.append(f"{key}: verkko-osoite hylätty (ei näytä osoitteelta): {webpage_raw!r}")

        g = geo.get(key)
        has_geo = bool(g) and "lat" in g and not g.get("country_mismatch") and not g.get("city_mismatch")
        if not has_geo:
            warnings.append(f"{key}: ei käyttökelpoisia koordinaatteja")

        items.append(
            {
                "id": key,
                "erasmus_code": r["erasmusCode"],
                "oid": r["oid"],
                "name": name,
                "name_lang": v.get("organisationLegalNameLang") if v.get("organisationLegalName") else None,
                # Nimi komission listan muodossa (versaalit säilyvät); vain jos se eroaa näytettävästä nimestä, myös pelkän kirjainkoon osalta
                "name_upstream": r["organisationLegalName"] if r["organisationLegalName"].strip() != name else None,
                "country": r["countryName"],
                "country_code": cc,
                "city": a.get("unit_city") or nice_case(v.get("city") or r["city"], cc),
                "street": None if a.get("unit_city") else nice_case((v.get("street") or r["street"] or "").strip(" ,"), cc) or None,
                "postal_code": None if a.get("unit_city") else v.get("postalCode") or r["postalCode"],
                "website": normalize_url(a["unit_website"]) if a.get("unit_website") else webpage,
                "parent_name": parent_name,
                "tier": a["tier"],
                "institution_type": a["institution_type"],
                "languages_of_instruction": a.get("languages_of_instruction"),
                "partner_of_siba": a.get("partner_of_siba"),
                "public_note": a.get("public_note"),  # julkinen englanninkielinen huomautus; classification_note ja notes ovat sisäisiä
                "lat": g["lat"] if has_geo else None,
                "lon": g["lon"] if has_geo else None,
                "geo_precision": g["precision"] if has_geo else None,
            }
        )
    items.sort(key=lambda i: (i["country"], i["name"].casefold()))

    fetched = meta_in.get("fetched")
    if not fetched:
        fetched = today()
        warnings.append("upstream.meta.json puuttuu: hakupäiväksi asetettu tämä päivä (aja fetch_upstream.py)")
    counts = Counter(i["tier"] for i in items)
    site = {
        "meta": {
            "fetched": fetched,
            "generated": today(),
            "upstream_file": UPSTREAM.name,
            "upstream_source": meta_in.get("source"),
            "counts": {"tier1": counts[1], "tier2": counts[2], "tier3": counts[3], "total": len(items)},
            "tier3_countries": TIER3_COUNTRIES,
            "tier_labels": {str(k): v for k, v in TIER_LABELS.items()},
            "scope_text": scope_text(fetched, items),
            "partner_source": PARTNER_SOURCE,
            "partner_source_name": PARTNER_SOURCE_NAME,
            "disclaimer": DISCLAIMER,
        },
        "institutions": items,
    }
    SITE.write_text(json.dumps(site, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    if SITE_PUBLIC:  # kopio julkaistavaan kansioon, jotta site/ on itsenäinen
        SITE_PUBLIC.parent.mkdir(parents=True, exist_ok=True)
        SITE_PUBLIC.write_text(SITE.read_text(encoding="utf-8"), encoding="utf-8")
    if STRATEGIES.exists():  # käsin ylläpidetty tiedosto; vain kopioidaan mukaan, ei generoida
        publish(STRATEGIES)
    if CONTACTS.exists():  # käsin tarkistettu, kuten strategiat
        publish(CONTACTS)
    if NETWORKS.exists():  # käsin tarkistettu, kuten strategiat
        publish(NETWORKS)
    if PROGRAMMES.exists() and DISCIPLINES.exists():  # käsin kerätty; sivu tarvitsee taksonomian alojen nimiin
        publish(PROGRAMMES)
        publish(DISCIPLINES)
    return site, warnings


def main():
    site, warnings = build()
    m = site["meta"]
    print(f"site.json: {m['counts']['total']} laitosta (taso 1: {m['counts']['tier1']}, taso 2: {m['counts']['tier2']}, taso 3: {m['counts']['tier3']}), "
          f"haettu {m['fetched']}  ->  {SITE}")
    no_web = [i["id"] for i in site["institutions"] if not i["website"]]
    print(f"Ilman verkko-osoitetta: {len(no_web)} {no_web if no_web else ''}")
    if warnings:
        print(f"\nVaroitukset ({len(warnings)}):")
        for w in warnings:
            print("  " + w)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
