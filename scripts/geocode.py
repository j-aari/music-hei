"""Vaihe 4: geokoodaa annotoidut laitokset Nominatimilla, tulos data/geo.json-tiedostoon.

Ajetaan käsin kerran. Kunnioittaa Nominatimin käyttöehtoja: enintään yksi pyyntö sekunnissa,
tunnistautuva User-Agent. Jo geokoodatut avaimet ohitetaan (jatkaa keskeytyneestä ajosta);
--retry-failed yrittää epäonnistuneet uudelleen, --force geokoodaa kaiken uudelleen.

Jokaiselle laitokselle kokeillaan tarkkuusportaita, kunnes tulos osuu odotettuun maahan:
  address - jäsennelty haku: katu + kaupunki (+ postinumero)
  name    - vapaa haku: laitoksen nimi, kaupunki, maa
  city    - jäsennelty haku: vain kaupunki (kartalle riittävä, ei osoitetarkka)
Maasuodatinta (countrycodes) ei käytetä, jotta väärään maahan osuvat tulokset näkyvät.
Jos mikään aste ei osu oikeaan maahan mutta jokin tulos löytyi, ensimmäinen tallennetaan
merkinnällä country_mismatch=true.

Kaupunkitarkistus (pysyvä): osoite- ja nimihaun tulos hylätään ja haku siirtyy seuraavalle
asteelle, jos tuloksen kaupunki ei vastaa upstreamin kaupunkia. Vertailu kestää eri kielet
(Vienna/Wien, Milan/Milano): jos kaupungin nimi ei löydy tuloksen nimestä, verrataan tuloksen
etäisyyttä upstreamin kaupungin keskipisteeseen (CITY_TOLERANCE_KM). Hylätyt haut kirjataan
kenttään "rejected" ja raportoidaan varoituksina. --check ajaa tarkistuksen olemassa olevalle
geo.json-tiedostolle ilman uudelleengeokoodausta. Avaimet komentorivillä geokoodaa vain ne
uudelleen.
"""

import json
import math
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import date

from common import GEO, load_annotations, load_upstream

ENDPOINT = "https://nominatim.openstreetmap.org/search"
# Nominatimin käyttöehdot vaativat tunnistautuvan User-Agentin yhteystietoineen.
USER_AGENT = "music-hei-eche-geocoder/0.1 (one-off geocoding of ECHE music institutions; jyriaarila@gmail.com)"
CITY_TOLERANCE_KM = 12  # nimen ei löytyessä: suurin sallittu etäisyys upstreamin kaupungin keskipisteestä
MIN_INTERVAL = 1.1  # s, ehdoissa 1 pyyntö/s
_last_request = 0.0


def clean_city(city):
    """'PARIS CEDEX 03' -> 'PARIS', 'Adria (RO)' -> 'Adria', 'Odense C.' -> 'Odense'."""
    c = re.sub(r"\(.*?\)", "", city or "")
    c = re.sub(r"\bcedex\b.*", "", c, flags=re.I)
    c = re.sub(r"\s+[A-Z]\.$", "", c.strip())
    c = re.sub(r"\s+\d+$", "", c)  # 'Dublin 2' -> 'Dublin'
    c = re.sub(r"(?<=[A-Z]{4})\s+[A-Z]{2}$", "", c)  # 'SAN DOMENICO DI FIESOLE FI' -> '... FIESOLE' (provinssikoodi)
    return c.strip(" ,-")


def request(params):
    """Yksi Nominatim-haku, rate limit ja uudelleenyritys 429/5xx-virheissä. Palauttaa tulosluettelon."""
    global _last_request
    url = ENDPOINT + "?" + urllib.parse.urlencode({**params, "format": "jsonv2", "addressdetails": 1, "limit": 1, "accept-language": "en"})
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    for attempt in range(4):
        wait = MIN_INTERVAL - (time.monotonic() - _last_request)
        if wait > 0:
            time.sleep(wait)
        _last_request = time.monotonic()
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.load(resp)
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504) and attempt < 3:
                time.sleep(10 * (attempt + 1))
                continue
            raise
        except urllib.error.URLError:
            if attempt < 3:
                time.sleep(5)
                continue
            raise


_centroids = {}


def city_centroid(r):
    """Upstreamin kaupungin keskipiste (lat, lon) tai None; välimuistissa."""
    city, country = clean_city(r["city"]), r["countryName"]
    if (city, country) not in _centroids:
        res = request({"city": city, "country": country})
        _centroids[(city, country)] = (float(res[0]["lat"]), float(res[0]["lon"])) if res else None
    return _centroids[(city, country)]


def km(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 6371 * 2 * math.asin(math.sqrt(h))


def city_check(r, display_name, lat, lon):
    """Palauttaa (ok, selite). ok=None jos tarkistusta ei voitu tehdä (keskipistettä ei löytynyt).

    Ensin nimivertailu (upstreamin kaupunki tuloksen nimessä); jos ei löydy, etäisyys kaupungin
    keskipisteeseen, jotta englanninkieliset/paikalliset nimet (Vienna/Wien) eivät anna hälytystä.
    """
    from find_candidates import fold

    city = fold(clean_city(r["city"]))
    if city and city in fold(display_name or ""):
        return True, "nimi"
    c = city_centroid(r)
    if c is None:
        return None, f"kaupungin '{clean_city(r['city'])}' keskipistettä ei löytynyt"
    d = km(c, (lat, lon))
    return d <= CITY_TOLERANCE_KM, f"{d:.0f} km kaupungin '{clean_city(r['city'])}' keskipisteestä"


def attempts(r):
    """(tarkkuus, hakuparametrit) tarkkuusjärjestyksessä."""
    city = clean_city(r["city"])
    country = r["countryName"]
    out = []
    street = (r.get("street") or "").strip()
    if street:
        p = {"street": street, "city": city, "country": country}
        if r.get("postalCode"):
            out.append(("address", {**p, "postalcode": r["postalCode"]}))
        out.append(("address", p))
    out.append(("name", {"q": f"{r['organisationLegalName']}, {city}, {country}"}))
    out.append(("city", {"city": city, "country": country}))
    return out


def geocode(r, expected):
    tried, first_wrong, rejected = [], None, []
    for precision, params in attempts(r):
        res = request(params)
        q = json.dumps(params, ensure_ascii=False)
        if not res:
            tried.append({"precision": precision, "query": q, "result": "ei tuloksia"})
            continue
        hit = res[0]
        got = (hit.get("address", {}).get("country_code") or "").upper()
        rec = {
            "lat": float(hit["lat"]),
            "lon": float(hit["lon"]),
            "precision": precision,
            "query": q,
            "display_name": hit.get("display_name"),
            "osm": f"{hit.get('osm_type')}/{hit.get('osm_id')}",
            "country_returned": got,
            "country_expected": expected,
            "country_mismatch": got != expected,
            "geocoded": date.today().isoformat(),
        }
        if rec["country_mismatch"]:
            tried.append({"precision": precision, "query": q, "result": f"väärä maa: {got}"})
            first_wrong = first_wrong or rec
            continue
        if precision != "city":
            ok, why = city_check(r, rec["display_name"], rec["lat"], rec["lon"])
            if ok is False:
                rejected.append({"precision": precision, "query": q, "display_name": rec["display_name"], "reason": why})
                first_wrong = first_wrong or {**rec, "city_mismatch": True}
                continue
            rec["city_check"] = why if ok else "ei tarkistettu: " + why
        if rejected:
            rec["rejected"] = rejected
        return rec
    if first_wrong:
        return {**first_wrong, "rejected": rejected} if rejected else first_wrong
    return {"status": "failed", "tried": tried, "geocoded": date.today().isoformat()}


def report(geo, up):
    failed = {k: v for k, v in geo.items() if v.get("status") == "failed"}
    wrong = {k: v for k, v in geo.items() if v.get("country_mismatch")}
    from collections import Counter

    prec = Counter(v["precision"] for v in geo.values() if "precision" in v and not v.get("country_mismatch"))
    print(f"\nGeokoodattu: {len(geo)}; tarkkuus: {dict(prec)}")
    warn = {k: v for k, v in geo.items() if v.get("rejected") or v.get("city_mismatch")}
    print(f"\nKaupunkivaroitukset ({len(warn)}): tulos ei vastannut upstreamin kaupunkia")
    for k, v in warn.items():
        used = "TALLENNETTU SILTI VÄÄRÄN KAUPUNGIN TULOS" if v.get("city_mismatch") else f"käytössä: {v['precision']}"
        print(f"  [{k}] {up[k]['organisationLegalName']} — upstream: {up[k]['city']}; {used}")
        for rj in v.get("rejected", []):
            print(f"      hylätty ({rj['precision']}): {rj['display_name'][:100]} — {rj['reason']}")
    print(f"\nEpäonnistui ({len(failed)}):")
    for k, v in failed.items():
        print(f"  [{k}] {up[k]['organisationLegalName']} — {up[k]['city']}, {up[k]['countryName']}")
    print(f"\nOsui eri maahan kuin upstream ({len(wrong)}):")
    for k, v in wrong.items():
        print(f"  [{k}] {up[k]['organisationLegalName']} — odotettu {v['country_expected']}, tuli {v['country_returned']}: {v['display_name']}")


def run(only=None, force=False, retry=False):
    """Geokoodaa annotoidut laitokset, joilta koordinaatit puuttuvat (tai only-avaimet); tulostaa raportin."""
    up = load_upstream()
    keys = list(load_annotations()[0])
    geo = json.loads(GEO.read_text(encoding="utf-8")) if GEO.exists() and not force else {}

    todo = only or [k for k in keys if k not in geo or (retry and geo[k].get("status") == "failed")]
    print(f"Laitoksia {len(keys)}, geokoodataan {len(todo)} (arvio ~{len(todo) * 2 // 60 + 1} min)", flush=True)
    for i, k in enumerate(todo, 1):
        r = up[k]
        expected = r["countryCodeIso"]
        geo[k] = geocode(r, expected)
        g = geo[k]
        status = "EPÄONNISTUI" if g.get("status") == "failed" else ("VÄÄRÄ MAA" if g["country_mismatch"] else g["precision"])
        print(f"[{i}/{len(todo)}] {k}: {status}", flush=True)
        GEO.write_text(json.dumps(dict(sorted(geo.items())), ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    if geo:
        report(geo, up)


def check():
    """Tarkista olemassa olevat tulokset ilman uudelleengeokoodausta."""
    up = load_upstream()
    geo = json.loads(GEO.read_text(encoding="utf-8"))
    bad = 0
    for k, v in geo.items():
        if "lat" in v and v["precision"] != "city":
            ok, why = city_check(up[k], v["display_name"], v["lat"], v["lon"])
            if ok is not True:
                bad += 1
                print(f"  {'VAROITUS' if ok is False else 'ei tarkistettu'} [{k}] {up[k]['organisationLegalName']} — {up[k]['city']}: {why}", flush=True)
    print(f"Tarkistettu {len(geo)}, huomautuksia {bad}")


def main():
    args = sys.argv[1:]
    if "--check" in args:
        return check()
    run(only=[a for a in args if not a.startswith("--")], force="--force" in args, retry="--retry-failed" in args)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
