"""next.py [N] : tulosta seuraavat N keräämätöntä laitosta site.json-järjestyksessä (koodi | nimi | taso | verkko-osoite)."""
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
site = json.load(open(os.path.join(ROOT, "data", "site.json"), encoding="utf-8"))["institutions"]
done = set(json.load(open(os.path.join(ROOT, "data", "programmes.json"), encoding="utf-8"))["meta"]["institutions"])
todo = [i for i in site if i["erasmus_code"] not in done]
n = int(sys.argv[1]) if len(sys.argv) > 1 else 20
print(f"Keräämättä {len(todo)} / {len(site)}")
for i in todo[:n]:
    print(f"{i['erasmus_code']!r} | {i['name']} | {i['tier']} | {i['website']}" + (f" | osa: {i['parent_name']}" if i["parent_name"] else ""))
