"""Lisää keruuerä data/programmes.json-tiedostoon.

Käyttö: python scripts/add_programmes.py ERÄ.json

Erätiedosto (tiivis muoto, kirjoitetaan käsin keruun aikana):
{
  "collected": "2026-10-08",
  "method": "Mitä sivuja luettiin ja miten (menee verification_logiin).",
  "institutions": {
    "A  LINZ17": [
      ["piano", "BA", "Tasteninstrumente – Künstlerisches Bachelorstudium", "https://..."],
      ["arts-management", null, "Kulturmanagement (Lehrgang)", "https://...", "huomautus: taso ei ilmene"]
    ]
  },
  "notes": {"B  GENT40": "Only doctoral study (docARTES) without named fields."}
}

Rivi = [ala, taso (BA/MA/Doc tai null), ohjelman nimi sivulla, sivun osoite, valinnainen huomautus].
Ala on disciplines.json-tunniste. Aloittain kirjattaessa riittää yksi rivi per ala ja taso.
notes: laitokset, joilta ei löytynyt kirjattavia ohjelmia; huomautus näytetään sivulla.
Laitoksen aiemmat rivit korvataan, joten erän voi ajaa uudelleen korjattuna.
"""

import json
import sys
from collections import OrderedDict

from common import DATA, SITE

PROGRAMMES = DATA / "programmes.json"
DISCIPLINES = DATA / "disciplines.json"
LEVELS = ("BA", "MA", "Doc")


def main(path):
    batch = json.loads(open(path, encoding="utf-8").read())
    prog = json.loads(PROGRAMMES.read_text(encoding="utf-8"))
    disc_ids = {d["id"] for d in json.loads(DISCIPLINES.read_text(encoding="utf-8"))["disciplines"]}
    codes = {i["erasmus_code"] for i in json.loads(SITE.read_text(encoding="utf-8"))["institutions"]}

    errors = []
    new = []
    for code, rows in batch["institutions"].items():
        if code not in codes:
            errors.append(f"{code!r}: ei sivun laitoksissa")
        by_disc = OrderedDict()
        for r in rows:
            d, level, name, url = r[:4]
            note = r[4] if len(r) > 4 else None
            if d not in disc_ids:
                errors.append(f"{code}: tuntematon ala {d!r}")
            if level is not None and level not in LEVELS:
                errors.append(f"{code}: tuntematon taso {level!r}")
            if not (name and url and url.startswith("http")):
                errors.append(f"{code}: nimi tai osoite puuttuu rivillä {r}")
            ev = {"level": level, "programme_name": name, "url": url}
            if note:
                ev["note"] = note
            evs = by_disc.setdefault(d, [])
            if not any(e["level"] == level for e in evs):  # yksi todiste per ala ja taso riittää
                evs.append(ev)
        for d, evs in by_disc.items():
            levels = [lv for lv in LEVELS if any(e["level"] == lv for e in evs)]
            new.append({"erasmus_code": code, "discipline": d, "levels": levels, "source_url": evs[0]["url"],
                        "evidence": evs, "verified": False})
    notes = batch.get("notes", {})
    for code in notes:
        if code not in codes:
            errors.append(f"{code!r}: ei sivun laitoksissa")
    if errors:
        print("Virheitä, mitään ei tallennettu:")
        for e in errors:
            print("  " + e)
        sys.exit(1)

    done = set(batch["institutions"]) | set(notes)
    prog["programmes"] = [p for p in prog["programmes"] if p["erasmus_code"] not in done] + new
    meta = prog["meta"]
    meta["institutions"] = sorted(set(meta["institutions"]) | done)
    inst_notes = meta.setdefault("institution_notes", {})
    for code in done:
        inst_notes.pop(code, None)
    inst_notes.update(notes)
    meta["collected"] = batch["collected"]
    meta["description"] = ("Study programmes per institution and fine-grained discipline (see disciplines.json). "
                           f"Collected so far: {len(meta['institutions'])} institutions.")
    meta["verification_log"].append({"erasmus_codes": sorted(done), "date": batch["collected"], "method": batch["method"]})
    PROGRAMMES.write_text(json.dumps(prog, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"Lisätty {len(done)} laitosta, {len(new)} riviä. Yhteensä {len(meta['institutions'])} laitosta.")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main(sys.argv[1])
