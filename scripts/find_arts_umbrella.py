"""Vaihe 2 (lisä): etsi monialaiset taide-/kuvataideyliopistot, joissa musiikki voi olla emo-
organisaation sisällä (esim. Taideyliopisto -> Sibelius-Akatemia).

Haku ei riipu siitä, osuiko laitos nimihakuun (find_candidates.py); sarake "tila" kertoo
sen. Vain tulostus, ei kirjoita tiedostoja.
"""

import json
import re
import sys
from collections import defaultdict

from find_candidates import EXCLUDED, OUT, UPSTREAM, fold, names_of

# Osahakuja foldattuun nimeen (ei diakriitteja, pienet kirjaimet).
UMBRELLA = re.compile(
    "|".join(
        [
            r"taideyliopisto",
            r"listahaskol",
            r"konstuniversitet|konstnarliga",
            r"university of (the )?(fine )?arts",
            r"arts university|art university|university of art\b",
            r"universitat der kunste",
            r"kunstuniversit",
            r"kunsthochschule|hochschule (der|fur) (bildenden )?kunst",
            r"academy of (the )?(fine )?arts",
            r"akademie der (bildenden )?kunste",
            r"hogeschool (voor de |der )kunsten|hogeschool (voor )?(de )?kunst",
            r"kunstakademi|kunsthogskol|kunstfack|konstfack",
            r"akademia sztuk|akademija umjetnosti|akademia sztuki",
            r"kunstiakadeemia|makslas akademija|dailes akademija",
            r"universidad de las artes|universita delle arti|universidade das artes",
            r"universitatea de arte|universitatea de arta",
            r"guzel sanatlar|fine arts university|sanat universitesi",
            r"academie des beaux|accademia di belle arti|academia de bellas artes",
        ]
    )
)


def main():
    rows = json.loads(UPSTREAM.read_text(encoding="utf-8"))
    status = {}
    for c in json.loads(OUT.read_text(encoding="utf-8")):
        status[c["key"]] = c["tier"]
    for c in json.loads(EXCLUDED.read_text(encoding="utf-8")):
        status[c["key"]] = "excluded"

    by_country = defaultdict(list)
    for r in rows:
        if any(UMBRELLA.search(fold(n)) for n in names_of(r)):
            key = r["erasmusCodeNormalized"] or r["erasmusCode"]
            by_country[r["countryName"]].append((r["organisationLegalName"], key, r["city"], status.get(key, "-")))

    total = sum(len(v) for v in by_country.values())
    print(f"Monialaisia taide-/kuvataideorganisaatioita: {total}")
    print("tila: strict/weak = osui nimihakuun, excluded = poissuljettu, - = ei osunut\n")
    for country in sorted(by_country):
        items = sorted(by_country[country], key=lambda t: (t[2] or "", t[0]))
        print(f"== {country} ({len(items)})")
        for name, key, city, st in items:
            print(f"  [{st:8}] {name} | {city} | {key}")
        print()


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
