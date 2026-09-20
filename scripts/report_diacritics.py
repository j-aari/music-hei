"""Listaa laitokset, joiden sivulla näkyvästä nimestä voi puuttua diakriitteja.

Upstream (ECHE-lista) on usein pelkkää ASCII-versaalia, joten esim. "UNIVERSITAT FUR MUSIK" on oikeasti
"Universität für Musik". Korjaus tehdään käsin lisäämällä annotations.json-merkintään display_name;
build_site.py käyttää sitä ensisijaisena. Tämä skripti vain listaa, ei korjaa mitään.

  A - lähde on pelkkää versaalia ja lopputulos pelkkää ASCIIta: diakriitit todennäköisesti puuttuvat
  B - lähde on sekakirjaimista mutta pelkkää ASCIIta: yleensä oikein, mutta tarkista (esim. "Musica")
"""

import sys
from collections import defaultdict

from common import load_annotations, load_upstream, nice_case


def is_shouty(s):
    letters = [c for c in s if c.isalpha()]
    return len(letters) >= 3 and (all(c.isupper() for c in letters) or all(c.islower() for c in letters))


def main():
    up = load_upstream()
    ann, _ = load_annotations()
    groups = {"A": defaultdict(list), "B": defaultdict(list)}
    done = 0
    for k, a in sorted(ann.items()):
        r = up[k]
        src = (r.get("_verified") or {}).get("organisationLegalName") or r["organisationLegalName"]
        done += bool(a.get("display_name"))
        # display_name ohittaa siistityn nimen, mutta jos sekin on pelkkää ASCIIta, laitos pysyy listalla
        name = a.get("display_name") or nice_case(src, r["countryCodeIso"] or r["countryCode"])
        if not name.isascii():
            continue
        mark = "  (display_name asetettu, vielä ilman diakriitteja)" if a.get("display_name") else ""
        groups["A" if is_shouty(src) else "B"][r["countryName"]].append((k, name + mark, r["city"]))
    print(f"display_name asetettu: {done} laitokselle\n")
    for g, title in (("A", "A - versaalilähde, pelkkää ASCIIta (diakriitit todennäköisesti puuttuvat)"),
                     ("B", "B - sekakirjaiminen lähde, pelkkää ASCIIta (yleensä oikein, tarkista)")):
        n = sum(len(v) for v in groups[g].values())
        print(f"== {title}: {n}")
        for country in sorted(groups[g]):
            print(f"  {country}")
            for k, name, city in groups[g][country]:
                print(f"    [{k}] {name}  ({city})")
        print()


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
