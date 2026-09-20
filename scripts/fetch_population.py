"""Hae väkiluvut Eurostatista ja tallenna data/population.json (+ kopio site/data/).

Lähde: Eurostat, taulukko tps00001 "Population on 1 January - total". Valitaan uusin vuosi, jolta on luku
kaikille maille, joissa on ECHE-haltijoita (upstream.json) - siis yksi yhteinen vuosi, ei sekoitusta.
Maakoodit normalisoidaan ISO 3166-1 alpha-2 -muotoon (Eurostat: EL -> GR, UK -> GB), samaan muotoon kuin
site.json:n country_code. Ajetaan käsin, esim. kerran vuodessa; ei kuulu päivitysketjuun.
"""

import json
import sys
import urllib.request

from common import POPULATION, UPSTREAM, publish, today

API = ("https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/tps00001"
       "?format=JSON&lang=EN&freq=A&indic_de=JAN")
USER_AGENT = "music-hei-eche-fetch/0.1"
ISO = {"EL": "GR", "UK": "GB"}
SKIP = ("EU", "EA", "FX")  # yhteenvetorivit ja Ranskan osa-aggregaatti


def fetch():
    req = urllib.request.Request(API, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.load(resp)


def parse(d):
    """JSON-stat -> {vuosi: {iso2: (väkiluku, lippu, nimi)}}"""
    ids, sizes = d["id"], d["size"]
    strides = {}
    acc = 1
    for name, size in reversed(list(zip(ids, sizes))):
        strides[name] = acc
        acc *= size
    geo = d["dimension"]["geo"]["category"]
    years = d["dimension"]["time"]["category"]["index"]
    status = d.get("status", {})
    out = {}
    for year, ti in years.items():
        rows = {}
        for code, gi in geo["index"].items():
            if code.startswith(SKIP):
                continue
            key = str(gi * strides["geo"] + ti * strides["time"])
            v = d["value"].get(key)
            if v is not None:
                rows[ISO.get(code, code)] = (int(v), status.get(key), geo["label"][code])
        out[year] = rows
    return out


def main():
    data = fetch()
    by_year = parse(data)
    needed = {r["countryCodeIso"] for r in json.loads(UPSTREAM.read_text(encoding="utf-8")) if r.get("countryCodeIso")}
    year = next((y for y in sorted(by_year, reverse=True) if needed <= set(by_year[y])), None)
    if year is None:
        year = max(by_year)
        print(f"VAROITUS: yhtäkään vuotta, jolta kaikki maat ({sorted(needed)}) löytyisivät; käytetään {year}")
    rows = by_year[year]
    out = {
        "source": "Eurostat, table tps00001: Population on 1 January - total",
        "url": API,
        "year": int(year),
        "retrieved": today(),
        "eurostat_updated": data.get("updated"),
        "note": "Population on 1 January of the given year. Flags: p = provisional, e = estimated.",
        "countries": {c: {"name": n, "population": v, **({"flag": f} if f else {})} for c, (v, f, n) in sorted(rows.items())},
    }
    POPULATION.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    publish(POPULATION)
    missing = sorted(needed - set(rows))
    print(f"Vuosi {year}, {len(rows)} maata -> {POPULATION}")
    print(f"ECHE-maita ilman väkilukua: {missing or 'ei yhtään'}")
    flagged = {c: v["flag"] for c, v in out["countries"].items() if v.get("flag") and c in needed}
    print(f"Liput (ECHE-maat): {flagged or 'ei'}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
