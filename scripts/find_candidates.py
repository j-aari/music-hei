"""Vaihe 2 (vain nimihaku): etsi upstream.json:sta musiikkikorkeakoulujen ehdokkaat.

Ei kirjoita annotations.json-tiedostoa. Tulos menee data/candidates_name.json-tiedostoon
(generoitu, ylikirjoitetaan) ja tulostetaan maittain tarkistettavaksi. Strict-osumista
poissuljetut (CNAM, draama, pelkkä tanssi) kirjataan syineen data/excluded.json-tiedostoon.

Avain on normalisoitu Erasmus-koodi (erasmusCodeNormalized); raaka koodi säilyy kentässä
erasmus_code_raw. Jos normalisoitua koodia ei ole, avaimena on raaka koodi ja key_source
kertoo sen.

Kaksi tasoa:
  strict - briefin nimihaun sanalista (lähes aina osumia)
  weak   - väljä musiikkiin viittaava kanta, joka ei osunut strictiin; näytetään erikseen,
           jotta briefin listan aukot (esim. "Hochschule für Musik") näkyvät
"""

import json
import re
import sys
import unicodedata
from collections import defaultdict

from common import DATA, UPSTREAM

OUT = DATA / "candidates_name.json"
EXCLUDED = DATA / "excluded.json"


FOLD_EXTRA = str.maketrans({"ø": "o", "æ": "ae", "ł": "l", "đ": "d", "ð": "d", "þ": "th", "ß": "ss", "ı": "i"})


def fold(s):
    """Pienet kirjaimet, ilman diakriitteja: 'Zeneakadémia' -> 'zeneakademia'."""
    s = unicodedata.normalize("NFKD", s.casefold())
    s = "".join(c for c in s if not unicodedata.combining(c))
    # NFKD ei pura näitä diakriitteja; muunnetaan käsin (ø, æ, ł, đ, ð, þ, ß)
    return s.translate(FOLD_EXTRA)


# Briefin lista. Etuliitehaut (ei loppurajaa), jotta taivutetut muodot osuvat
# (muzyczna/muzycznej, hudebni/hudebnich, conservatorio/conservatoire/conservatorium/...).
STRICT = {
    # Conservatorio/-oire/-orium/-ory, Konservatorium/-orij; ei loppurajaa eikä alkurajaa,
    # jotta yhdyssanat (Musikkonservatorium) osuvat mutta "conservation" ei
    "conservatorio/-oire/-orium, konservatorium": r"[ck]onservato(r[iy]|ir)",
    "musikhochschule": r"musikhochschule",
    "academy of music": r"academy of music",
    "muziekhogeschool": r"muziekhogeschool",
    "accademia musicale": r"accademia (di )?music",
    "academia de musica": r"academia de musica",
    "muzyczna": r"\bmuzyczn",
    "zeneakademia": r"\bzeneakad",
    "hudebni": r"\bhudebn",
    "hochschule fur musik": r"hochschule (fur|fuer) musik",
    # Kirkkomusiikkikorkeakoulut ovat tutkintoa myöntäviä musiikkikorkeakouluja
    # (Halle, Tübingen: "Evangelische Hochschule für Kirchenmusik"; Regensburg: "... katholische Kirchenmusik ...")
    "hochschule fur kirchenmusik": r"hochschule (fur|fuer) (\w+ )?kirchenmusik",
    # Britannia ja Sveitsi: eivät ole nykyisessä ECHE-listassa, valmiina siltä varalta että ilmestyvät
    # (ks. BRIEF.md, rajausteksti). "Royal Conservatoire" ja "Conservatorio della Svizzera italiana"
    # osuisivat jo conservato-hakuun, mutta ne on listattu erikseen dokumentoinnin vuoksi.
    "royal college of music": r"royal college of music",
    "royal academy of music": r"royal academy of music",
    "royal northern college of music": r"royal northern college of music",
    "royal conservatoire": r"royal conservatoire",
    "guildhall school": r"guildhall school",
    "trinity laban": r"trinity laban",
    "haute ecole de musique": r"haute ecole de musique",
    "conservatorio della svizzera italiana": r"conservatorio della svizzera italiana",
}

WEAK = {
    "music/musik/musiq/musi-": r"musi[ckq]|musiikk|musica|musique",
    "muzi-/muzy-": r"\bmuz[iy]",
    "zene": r"\bzene",
    "hudb-": r"\bhudb|\bhudeb",
    "glasb/glazb": r"\bgla[sz]b",
    "muusika/muzika": r"muusika|muzika|muzik",
    # Kielimuodot erikseen listattuna (osa osuu jo yllä): viro muusika, suomi musiikki,
    # islanti tónlist / Listaháskóli, turkki müzik, kreikka mousik-, tanska/norja musikhøjskole/-hogskole
    "musiikki (fi)": r"musiikki",
    "tonlist (is)": r"tonlist",
    "listahaskoli (is)": r"listahaskol",
    "muzik (tr)": r"muzik",
    "mousik- (el)": r"mousik",
    "musikhojskole/-hogskole (dk/no/se)": r"musik(hojskol|hogskol|hoegskol)",
}


def compile_all(d):
    return {k: re.compile(v) for k, v in d.items()}


STRICT_RE, WEAK_RE = compile_all(STRICT), compile_all(WEAK)

# Poissulkusäännöt strict-osumille. Poissuljetut kirjataan data/excluded.json-tiedostoon syineen.
# (id, syy, sääntö nimelle foldattuna)
EXCLUDE = [
    (
        "cnam",
        "Conservatoire national des arts et métiers (CNAM) ei ole musiikkilaitos",
        lambda n: re.search(r"conservatoire (national )?des arts et metiers", n) is not None,
    ),
    (
        "drama",
        "Draamakonservatorio: näyttelijäkoulutus, ei musiikkia",
        lambda n: re.search(r"art dramatique|arte dramatico|art dramatic\b", n) is not None,
    ),
    (
        "dance-only",
        'Pelkkä tanssilaitos: nimessä "Danza"/"Dansa" mutta ei "Música"',
        lambda n: re.search(r"\bdan[sz]a\b", n) is not None and "musica" not in n,
    ),
]


# Käsin tehdyt poissulkupäätökset (avain -> syy), koskevat myös weak-tasoa. Kirjataan
# data/excluded.json-tiedostoon. (Ks. BRIEF.md: ECHE-haltijuus tarkoittaa korkeakoulun
# asemaa; kysymys on vain kuuluuko laitos musiikkiin.)
MANUAL_EXCLUDE = {
    "I  NOVARA02": "Scuola del Teatro Musicale: musiikkiteatterin ammatillinen koulu, ei tutkintoa myöntävä musiikkikorkeakoulu",
    "E  BARCELO259": "Jam Session SL: yksityinen musiikkikoulu, ei virallista título superior -tutkintoa",
    "CY NICOSIA42": "Hellenic College of Music: yksityinen musiikkikoulu",
    "P  LISBOA118": "MUSICA Educação e Cultura: koulutusyhdistys, ei korkeakoulu",
    "F  LYON128": "CEFEDEM Auvergne Rhône-Alpes: musiikinopettajien DE-tutkintokoulutus, ei musiikkialan korkeakoulututkintoa",
    "F  ROUEN44": "CEFEDEM Normandie: musiikinopettajien DE-tutkintokoulutus, ei musiikkialan korkeakoulututkintoa",
    "F  MELUN07": "Centre des Musiques Didier Lockwood: yksityinen jazzkeskus, ei tutkintoa myöntävä korkeakoulu",
}


def excluded_reason(r):
    """Palauttaa (id, syy) jos jokin nimi täyttää poissulkusäännön, muuten None."""
    for rule_id, reason, test in EXCLUDE:
        if any(test(fold(n)) for n in names_of(r)):
            return rule_id, reason
    return None


def names_of(r):
    names = [r["organisationLegalName"]]
    v = (r.get("_verified") or {}).get("organisationLegalName")
    if v and v not in names:
        names.append(v)
    return names


def match(r, patterns):
    hits = []
    for label, rx in patterns.items():
        if any(rx.search(fold(n)) for n in names_of(r)):
            hits.append(label)
    return hits


def main(quiet=False):
    rows = json.loads(UPSTREAM.read_text(encoding="utf-8"))
    out, excluded = [], []
    for r in rows:
        strict = match(r, STRICT_RE)
        weak = [] if strict else match(r, WEAK_RE)
        if not (strict or weak):
            continue
        rec = {
            "key": r["erasmusCodeNormalized"] or r["erasmusCode"],
            "key_source": "normalized" if r["erasmusCodeNormalized"] else "raw (normalisoitua ei ole)",
            "erasmus_code_raw": r["erasmusCode"],
            "name": r["organisationLegalName"],
            "name_verified": (r.get("_verified") or {}).get("organisationLegalName"),
            "city": r["city"],
            "country_code": r["countryCode"],
            "country": r["countryName"],
            "webpage": r["webpage"],
            "tier": "strict" if strict else "weak",
            "matched": strict or weak,
        }
        if rec["key"] in MANUAL_EXCLUDE:
            excluded.append({**rec, "excluded_by": "manual", "reason": MANUAL_EXCLUDE[rec["key"]]})
        elif strict and (ex := excluded_reason(r)):
            excluded.append({**rec, "excluded_by": ex[0], "reason": ex[1]})
        else:
            out.append(rec)
    sort_key = lambda c: (c["country"], c["tier"] != "strict", c["city"] or "", c["name"])
    out.sort(key=sort_key)
    excluded.sort(key=sort_key)
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    EXCLUDED.write_text(json.dumps(excluded, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    keys = [c["key"] for c in out]
    dup = {k for k in keys if keys.count(k) > 1}

    by_country = defaultdict(list)
    for c in out:
        by_country[c["country"]].append(c)

    n_strict = sum(c["tier"] == "strict" for c in out)
    print(f"Rivejä upstreamissa: {len(rows)}")
    print(f"Ehdokkaita: {len(out)}  (strict {n_strict}, weak {len(out) - n_strict})  ->  {OUT}")
    if dup:
        print(f"HUOM: avainkonflikti ehdokkaissa: {sorted(dup)}")
    print(f"Poissuljettu: {len(excluded)}  ->  {EXCLUDED}")
    for e in excluded:
        print(f"  x [{e['key']}] {e['name']} — {e['city']}  ({e['excluded_by']})")
    print()
    for country, items in sorted(by_country.items()):
        if quiet:
            break
        ns = sum(i["tier"] == "strict" for i in items)
        print(f"== {country} ({len(items)}; strict {ns}, weak {len(items) - ns})")
        for i in items:
            mark = "S" if i["tier"] == "strict" else "w"
            print(f"  {mark} [{i['key']}] {i['name']} — {i['city']}")
        print()


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
