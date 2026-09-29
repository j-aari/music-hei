"""Laske laitoskohtainen Erasmus+ -liikkuvuusyhteenveto (data/mobility.json, kopio site/data/).

    python scripts/build_mobility.py

Lähtötiedot: fetch_mobility.py:n poimimat korkeakoulurivit (data/raw/mobility/he_YYYY.csv.gz) ja käsin
tarkistettu nimiluettelo data/mobility_names.json (laitos -> nimimuodot, joilla se esiintyy datassa).

Per laitos, vuosien FIRST_YEAR..LAST_YEAR (liikkuvuuden aloitusvuosi) yhteenvetona:
  - liikkuvuustyypit: opiskelijavaihto, harjoittelu, henkilöstön opetus- ja koulutusvaihto, sekä
    lyhytkestoinen opiskelijaliikkuvuus (enintään 30 päivää; vain SHORT_FROM alkaen, jolloin nämä jaksot
    tulivat ohjelmaan, pääosin BIP-jaksoja; BIP:iä ei voi erottaa datasta omaksi tyypikseen)
  - kunkin tyypin laajuus neljänä luokkana (harjoittelut kolmena), lähtevä ja saapuva erikseen. Luokkarajat ovat
    kvartiilit (tertiilit) niiden musiikkilaitosten joukossa, joilla tyyppiä esiintyy datassa (tyyppi- ja suuntakohtaisesti)
  - lyhytkestoinen liikkuvuus lasketaan dataan, mutta sivu ei toistaiseksi näytä sitä (useimmilla ei esiinny datassa)
  - viisi yleisintä kumppanimaata (vastapuolen maa, kaikki tyypit ja molemmat suunnat)
Tyyppi, jota ei ole datassa, merkitään "ei esiinny datassa" – se ei tarkoita, ettei laitos tarjoaisi sitä.

Taideyliopistojen musiikkiyksiköt (taso 2): mukaan vain rivit, joiden koulutusala on "Music and performing
arts" (sisältää myös teatterin ja tanssin); henkilöstöriveistä ala puuttuu usein, joten niiden luvut jäävät alakanttiin.
Jos tyyppiä on vain riveillä, joilta ala puuttuu, luokka on null ("alaa ei kirjattu"), ei 0 ("ei esiinny datassa").
Sivulle julkaistaan vain luokat ja luokkarajat, ei tarkkoja lukuja: nimien yhdistäminen ja datan puutteet
(organisaation nimi puuttuu osasta rivejä) tekevät tarkoista luvuista näennäisen tarkkoja.
"""

import csv
import gzip
import json
import statistics
import sys
from collections import Counter, defaultdict

from common import MOBILITY, MOBILITY_NAMES, MOBILITY_RAW, SITE, publish, today

FIRST_YEAR, LAST_YEAR = 2014, 2022
SHORT_FROM = 2021
SHORT_MAX_DAYS = 30
SOURCE_URL = "https://data.europa.eu/data/datasets/erasmus-mobility-raw-data"
TYPES = {
    "studies": "Student exchange (studies)",
    "traineeships": "Student traineeships",
    "teaching": "Staff teaching exchange",
    "training": "Staff training exchange",
    "short": "Short-term student mobility (up to 30 days, mostly BIPs)",
}
CLASS_LABELS = ["Small", "Moderate", "Large", "Very large"]
# Harjoittelujen luvut ovat pieniä ja kvartiilirajat menisivät päällekkäin, joten niissä on kolme luokkaa (tertiilit)
N_CLASSES = {"traineeships": 3}
LABELS = {3: ["Small", "Moderate", "Large"], 4: CLASS_LABELS}
MUSIC_FIELD = "music and performing arts"


def activity_type(a):
    """'HE-STA - Staff mobility for teaching' (2020-) tai 'Staff mobility for teaching between Programme Countries' (2014-2019)."""
    code = a.split(" - ")[0].strip().upper()
    for suffix, t in (("SMS", "studies"), ("SMT", "traineeships"), ("STA", "teaching"), ("STT", "training")):
        if code.startswith("HE-") and code.endswith(suffix):
            return t
    a = a.lower()
    for words, t in (("for studies", "studies"), ("traineeship", "traineeships"), ("for teaching", "teaching"), ("for training", "training")):
        if words in a:
            return t
    return None


def country_code(s):
    cc = s[:2]
    return {"UK": "GB", "EL": "GR"}.get(cc, cc)


def main():
    site = json.loads(SITE.read_text(encoding="utf-8"))["institutions"]
    by_code = {i["erasmus_code"]: i for i in site}
    names = json.loads(MOBILITY_NAMES.read_text(encoding="utf-8"))
    lookup = {}  # (maa, datan nimi) -> erasmus-koodi
    for code, v in names.items():
        if code not in by_code:
            sys.exit(f"mobility_names.json: tuntematon laitos {code}")
        for n in v["names"]:
            key = (by_code[code]["country_code"], n)
            if key in lookup and lookup[key] != code:
                sys.exit(f"mobility_names.json: nimi {n!r} kahdella laitoksella ({lookup[key]}, {code})")
            lookup[key] = code
    tier2 = {c for c, i in by_code.items() if i["tier"] == 2}

    counts = defaultdict(lambda: defaultdict(float))  # koodi -> (tyyppi, suunta) -> osallistujia
    no_field = defaultdict(set)  # taso 2: (tyyppi, suunta), joilla on rivejä, mutta koulutusala puuttuu
    partners = defaultdict(Counter)
    country_names = {}
    unknown = Counter()
    for year in range(FIRST_YEAR, LAST_YEAR + 1):
        path = MOBILITY_RAW / f"he_{year}.csv.gz"
        if not path.exists():
            sys.exit(f"{path} puuttuu: aja ensin python scripts/fetch_mobility.py")
        with gzip.open(path, "rt", encoding="utf-8", newline="") as f:
            for r in csv.DictReader(f):
                ends = {}
                for side, d in (("Sending", "out"), ("Receiving", "in")):
                    cc = country_code(r[f"{side} Country"])
                    country_names.setdefault(cc, r[f"{side} Country"][5:].strip())
                    code = lookup.get((cc, r[f"{side} Organization"].strip()))
                    if code:
                        ends[d] = code
                if not ends:
                    continue
                t = activity_type(r["Activity (mob)"])
                if t is None:
                    unknown[r["Activity (mob)"]] += 1
                    continue
                n = float(r["Participants"] or 0)
                try:
                    days = float(r["Mobility Duration"])
                except ValueError:
                    days = None
                short = (t in ("studies", "traineeships") and year >= SHORT_FROM
                         and days is not None and days <= SHORT_MAX_DAYS)
                field = r["Field of Education"].lower()
                music = MUSIC_FIELD in field
                field_missing = field.strip() in ("", "-") or "unknown" in field
                for d, code in ends.items():
                    if code in tier2 and not music:
                        if field_missing:
                            no_field[code].add((t, d))
                            if short:
                                no_field[code].add(("short", d))
                        continue
                    counts[code][(t, d)] += n
                    if short:
                        counts[code][("short", d)] += n
                    other = country_code(r[("Receiving" if d == "out" else "Sending") + " Country"])
                    if other != by_code[code]["country_code"]:
                        partners[code][other] += n
    if unknown:
        print("tunnistamattomat aktiviteetit:", unknown.most_common(5))

    classes = {}
    for t in TYPES:
        for d in ("out", "in"):
            vals = sorted(round(counts[c][(t, d)]) for c in names if round(counts[c][(t, d)]) > 0)
            k_n = N_CLASSES.get(t, 4)
            if len(vals) < k_n:
                continue
            q = [int(x) for x in statistics.quantiles(vals, n=k_n, method="inclusive")]
            lo = [vals[0]] + [x + 1 for x in q]
            hi = q + [vals[-1]]
            # Small whole numbers tie: a class whose range is empty (e.g. 2-1) stays empty and is shown as such
            ranges = [[lo[k], hi[k]] if lo[k] <= hi[k] else None for k in range(k_n)]
            per = [sum(1 for v in vals if r and r[0] <= v <= r[1]) for r in ranges]
            classes[f"{t}.{d}"] = {"labels": LABELS[k_n], "ranges": ranges, "institutions": per,
                                   "absent": sum(1 for c in names if round(counts[c][(t, d)]) == 0)}

    def cls(t, d, v):
        c = classes.get(f"{t}.{d}")
        if not c or v == 0:
            return 0
        return next(k + 1 for k, r in enumerate(c["ranges"]) if r and v <= r[1])

    out_inst = {}
    for code in sorted(names):
        # None = the type appears only in rows without a field of education (tier 2): not the same as "not in the data"
        rec = {"types": {t: [None if not round(counts[code][(t, d)]) and (t, d) in no_field[code] else cls(t, d, round(counts[code][(t, d)]))
                             for d in ("out", "in")] for t in TYPES},
               "partners": [cc for cc, _ in partners[code].most_common(5)]}
        if code in tier2:
            rec["music_field_only"] = True
        out_inst[code] = rec

    out = {
        "meta": {
            "generated": today(),
            "source": "Erasmus+ Mobility Raw Data, European Commission (Key Action 1, higher education)",
            "source_url": SOURCE_URL,
            "years": [FIRST_YEAR, LAST_YEAR],
            "short_term_years": [SHORT_FROM, LAST_YEAR],
            "types": TYPES,
            "class_labels": CLASS_LABELS,
            "classes": classes,
            "country_names": {cc: country_names[cc] for cc in sorted({p for r in out_inst.values() for p in r["partners"]})},
            "institutions_covered": len(out_inst),
        },
        "institutions": out_inst,
    }
    MOBILITY.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    publish(MOBILITY)

    print(f"{len(out_inst)}/{len(site)} laitosta, vuodet {FIRST_YEAR}-{LAST_YEAR}")
    for key, c in classes.items():
        t, d = key.split(".")
        rng = "  ".join(f"{c['labels'][k]} {r[0]}-{r[1]}: {n}" if r else f"{c['labels'][k]} (tyhjä)" for k, (r, n) in enumerate(zip(c["ranges"], c["institutions"])))
        print(f"  {t:13} {d:3}  {rng}  | ei datassa: {c['absent']}")


if __name__ == "__main__":
    main()
