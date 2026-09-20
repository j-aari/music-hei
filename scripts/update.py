"""Päivitysketju: hae ECHE-lista uudelleen, vertaa vanhaan, raportoi muutokset ja (vain --apply) päivitä.

    python scripts/update.py            # hakee ja tulostaa muutosraportin; EI kirjoita mitään
    python scripts/update.py --apply    # raportin jälkeen kirjoittaa ja ajaa koko ketjun

Raportti tulostetaan aina ennen kuin mitään kirjoitetaan (BRIEF.md). Ketju --apply-tilassa:
  1. upstream.json ja upstream.meta.json ylikirjoitetaan uudella haulla
  2. poistuneiden laitosten annotaatiot siirretään annotations.json:n orphaned-osioon
     (ei poisteta; tämä on ainoa automaattinen kirjoitus annotations.json:iin)
  3. ehdokaslistat (candidates_name.json, excluded.json) generoidaan uudelleen
  4. geokoodataan annotoidut laitokset, joilta koordinaatit puuttuvat
  5. site.json generoidaan uudelleen
  6. katvealueet (coverage.json) lasketaan uudelleen uusista koordinaateista
Uudet laitokset eivät päädy sivulle ennen kuin ne on annotoitu käsin.
"""

import json
import sys

import build_coverage
import build_site
import fetch_upstream
import find_candidates
import geocode
from common import UPSTREAM, key_of, load_annotations, save_annotations, today

MAX_LISTED = 60  # pisin lista, jonka raportti tulostaa kokonaan


def compare(old, new, annotated, orphaned_keys=()):
    """Vertaa kahta upstream-tilaa (avain -> rivi). Palauttaa raportin tiedot.

    added / removed / renamed sisältävät rivit; possible_recode = poistunut+uusi laitos, joilla on sama
    OID tai PIC (Erasmus-koodi on todennäköisesti vaihtunut); returned = orphaned-avaimet, jotka ovat taas listalla.
    """
    added = [new[k] for k in new.keys() - old.keys()]
    removed = [old[k] for k in old.keys() - new.keys()]
    renamed = [
        (old[k], new[k])
        for k in old.keys() & new.keys()
        if old[k]["organisationLegalName"] != new[k]["organisationLegalName"]
        or (old[k].get("_verified") or {}).get("organisationLegalName") != (new[k].get("_verified") or {}).get("organisationLegalName")
    ]
    possible_recode = []
    for rem in removed:
        for add in added:
            same = [f for f in ("oid", "pic") if rem.get(f) and rem.get(f) == add.get(f)]
            if same:
                possible_recode.append((rem, add, same))
    returned = [k for k in orphaned_keys if k in new]
    return {
        "added": sorted(added, key=key_of),
        "removed": sorted(removed, key=key_of),
        "renamed": sorted(renamed, key=lambda p: key_of(p[1])),
        "possible_recode": possible_recode,
        "returned": returned,
        "annotated_removed": [r for r in removed if key_of(r) in annotated],
        "annotated_renamed": [p for p in renamed if key_of(p[1]) in annotated],
    }


def display_name(r):
    return (r.get("_verified") or {}).get("organisationLegalName") or r["organisationLegalName"]


def rename_text(a, b):
    """Näyttää muuttuneet nimikentät: ECHE-listan nimi ja/tai _verified-nimi."""
    parts = []
    if a["organisationLegalName"] != b["organisationLegalName"]:
        parts.append(f"{a['organisationLegalName']}  ->  {b['organisationLegalName']}")
    va, vb = (a.get("_verified") or {}).get("organisationLegalName"), (b.get("_verified") or {}).get("organisationLegalName")
    if va != vb:
        parts.append(f"(verified: {va}  ->  {vb})")
    return " ".join(parts)


def print_report(c, old_n, new_n, annotated):
    print(f"\n=== Muutosraportti: {old_n} -> {new_n} laitosta ===")
    if not any(c[k] for k in ("added", "removed", "renamed", "returned")):
        print("Ei muutoksia.")
        return

    def listing(title, rows, fmt):
        print(f"\n{title} ({len(rows)}):")
        for r in rows[:MAX_LISTED]:
            print("  " + fmt(r))
        if len(rows) > MAX_LISTED:
            print(f"  ... ja {len(rows) - MAX_LISTED} muuta")

    def music_hint(r):
        s = find_candidates.match(r, find_candidates.STRICT_RE)
        if s:
            return "  <-- osuu nimihakuun (strict): harkitse annotointia"
        return "  <-- osuu väljään nimihakuun (weak)" if find_candidates.match(r, find_candidates.WEAK_RE) else ""

    listing("Uudet laitokset", c["added"], lambda r: f"[{key_of(r)}] {display_name(r)} — {r['city']}, {r['countryName']}{music_hint(r)}")
    listing(
        "Poistuneet laitokset",
        c["removed"],
        lambda r: f"[{key_of(r)}] {display_name(r)} — {r['city']}, {r['countryName']}"
        + ("  <-- ANNOTOITU: annotaatio siirretään orphaned-osioon" if key_of(r) in annotated else ""),
    )
    listing(
        "Nimenmuutokset",
        c["renamed"],
        lambda p: f"[{key_of(p[1])}] {rename_text(p[0], p[1])}" + ("  <-- ANNOTOITU" if key_of(p[1]) in annotated else ""),
    )
    if c["possible_recode"]:
        print(f"\nMahdolliset koodinvaihdokset ({len(c['possible_recode'])}): sama OID/PIC, eri Erasmus-koodi:")
        for rem, add, same in c["possible_recode"]:
            print(f"  [{key_of(rem)}] -> [{key_of(add)}] ({', '.join(same)}) {display_name(add)}")
        print("  Jos vanhalla koodilla on annotaatio, siirrä se käsin uudelle avaimelle orphaned-osiosta.")
    if c["returned"]:
        print(f"\nOrphaned-avaimia, jotka ovat taas listalla ({len(c['returned'])}): {c['returned']}")
        print("  Palauta annotaatio käsin orphaned-osiosta tarvittaessa.")


def apply(new_rows, c, annotations, orphaned):
    print("\n=== Kirjoitetaan ===")
    fetch_upstream.write(new_rows)
    print(f"upstream.json ({len(new_rows)} riviä) ja upstream.meta.json päivitetty")

    if c["annotated_removed"]:
        succ = {key_of(rem): [key_of(add) for r2, add, _ in c["possible_recode"] if r2 is rem] for rem in c["annotated_removed"]}
        for r in c["annotated_removed"]:
            k = key_of(r)
            entry = annotations.pop(k)
            orphaned[k] = {**entry, "orphaned_on": today(), "orphaned_reason": "ei enää ECHE-listassa",
                           **({"possible_successors": succ[k]} if succ.get(k) else {})}
        save_annotations(annotations, orphaned)
        print(f"annotations.json: {len(c['annotated_removed'])} annotaatiota siirretty orphaned-osioon (tarkistettavaksi)")
    else:
        print("annotations.json: ei siirrettäviä annotaatioita (ei koskettu)")

    print("\n--- ehdokaslistat ---")
    find_candidates.main(quiet=True)
    print("\n--- geokoodaus ---")
    geocode.run()
    print("\n--- site.json ---")
    build_site.main()
    print("\n--- katvealueet (coverage.json) ---")
    build_coverage.main()  # riippuu site.json:n koordinaateista


def main():
    do_apply = "--apply" in sys.argv
    old_by_key = {key_of(r): r for r in json.loads(UPSTREAM.read_text(encoding="utf-8"))} if UPSTREAM.exists() else {}
    annotations, orphaned = load_annotations()

    print("Haetaan ECHE-lista...")
    new_rows = fetch_upstream.fetch()
    new_by_key = {key_of(r): r for r in new_rows}

    c = compare(old_by_key, new_by_key, set(annotations), set(orphaned))
    print_report(c, len(old_by_key), len(new_by_key), set(annotations))

    if not do_apply:
        print("\nEi kirjoitettu mitään. Aja `python scripts/update.py --apply` päivittääksesi.")
        return
    apply(new_rows, c, annotations, orphaned)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
