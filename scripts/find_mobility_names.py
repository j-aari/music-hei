"""Ehdota, millä nimillä kukin laitos esiintyy Erasmus+ -liikkuvuusdatassa (data/mobility_candidates.json).

    python scripts/find_mobility_names.py

Liikkuvuusdatassa ei ole Erasmus-koodia, OID:tä eikä PIC:iä, vain organisaation vapaatekstinimi, kaupunki ja maa,
ja samalla laitoksella on usein monta kirjoitusasua. Tämä skripti tuottaa ehdotukset; lopullinen, käsin
tarkistettu luettelo on data/mobility_names.json, ja vain sitä käytetään (build_mobility.py).

Ehdotussääntö (sama maa):
  - datan nimen kaikki sanat löytyvät laitoksen nimestä tai kaupungista (pienet kirjoitusvirheet sallitaan), ja
  - datan nimessä on jokin laitoksen oma erottava sana (ei yleissana kuten "conservatorio", "hochschule",
    "music"), tai laitoksen nimessä ei ole muuta erottavaa kuin kaupunki, tai kyse on italialaisesta tai
    espanjalaisesta konservatoriosta, joka nimetään kaupungin mukaan ("Conservatorio di Como").
Jos sama datan nimi sopii usealle laitokselle, se annetaan selvästi parhaiten sopivalle tai jätetään pois.
"""

import csv
import gzip
import json
import re
import unicodedata
from collections import defaultdict
from difflib import SequenceMatcher

from common import MOBILITY_CANDIDATES, MOBILITY_RAW, SITE

EXTRA = str.maketrans({"ø": "o", "æ": "ae", "ł": "l", "đ": "d", "ß": "ss", "ı": "i", "œ": "oe"})
STOP = set("""di de del della dello dei la le el il lo of the and und for fur fuer in im w we an et du des der die
das da do dos van voor en og och ja na iz ve prof st""".split())
GENERIC = STOP | set("""conservatorio conservatori conservatoire conservatorium conservatory konservatorium konservatorij
konservatoriet konservatoorium statale stato state national nazionale nacional superior superiore superieur hoger
hogere hochschule hogeschool hogskole hogskolen hoegskolan hogskolan hogskola musikhogskolan musikhogskole
musikkhogskole musikkhogskolen music musica musik muzyki muzyczna muzicii musique muziek musiikki musical musicale
musicali academy akademie akademia accademia academia academie akademi akademiet university universita universitat
universitaet universidad universite universitet universiteit uniwersytet universitatea universiteti college school
scuola escola escuela istituto instituto institut institute institutt ecole schule arts art arti artes kunst kunste
kunsten kunstuniversitat umeni umenia sztuk private privat privatuniversitat privathochschule gmbh ev srl performing
darstellende dramatic drama dance danza tanz theatre teatro theater alta formazione artistica studi higher education
professional royal kungl koninklijk koninklijke det kongelige danske stichting fundacio fundacion""".split())
NO_NAME = {"", "-", "?", "? Unknown ?"}


def toks(s):
    s = str(s).lower().replace("&apos;", "'").replace("&quot;", '"').translate(EXTRA)
    s = "".join(c for c in unicodedata.normalize("NFD", s) if not unicodedata.combining(c))
    return [t for t in re.sub(r"[^a-z0-9]+", " ", s).split() if len(t) > 1]


def has(tok, pool):
    return any(tok == p or (len(tok) >= 5 and SequenceMatcher(None, tok, p).ratio() >= 0.88) for p in pool)


def country_code(s):
    cc = s[:2]
    return {"UK": "GB", "EL": "GR"}.get(cc, cc)


def load_orgs():
    """(maa, nimi) -> {'n': osallistujia (lähtevä + saapuva), 'cities': {kaupunki: n}}"""
    orgs = defaultdict(lambda: {"n": 0, "cities": defaultdict(int)})
    for path in sorted(MOBILITY_RAW.glob("he_*.csv.gz")):
        with gzip.open(path, "rt", encoding="utf-8", newline="") as f:
            for r in csv.DictReader(f):
                n = float(r["Participants"] or 0)
                for side in ("Sending", "Receiving"):
                    name = r[f"{side} Organization"].strip()
                    if name in NO_NAME:
                        continue
                    o = orgs[(country_code(r[f"{side} Country"]), name)]
                    o["n"] += n
                    o["cities"][r[f"{side} City"]] += n
    return orgs


def main():
    site = json.loads(SITE.read_text(encoding="utf-8"))["institutions"]
    orgs = load_orgs()
    by_cc = defaultdict(list)
    for (cc, name), o in orgs.items():
        at = [t for t in toks(name) if t not in STOP]
        by_cc[cc].append((name, o, at, [t for t in at if t not in GENERIC]))

    found = defaultdict(list)
    claimed = defaultdict(list)
    for i in site:
        cc = i["country_code"]
        name_t = set(toks(i["name"]) + toks(i.get("name_upstream") or ""))
        city_t = set(toks(i["city"] or ""))
        inst_all = (name_t | city_t) - STOP
        own = {t for t in name_t if t not in GENERIC} - city_t
        for name, o, at, dt in by_cc[cc]:
            if not dt or not all(has(t, inst_all) for t in at):
                continue
            own_hit = any(has(t, own) for t in dt)
            city_only = not own and any(has(t, city_t) for t in dt)
            cityform = cc in ("IT", "ES") and all(has(t, city_t) for t in dt) and any(t.startswith("conserv") for t in at)
            if not (own_hit or city_only or cityform):
                continue
            cov = sum(has(t, at) for t in inst_all) / max(1, len(inst_all))
            found[i["id"]].append({"name": name, "participants": round(o["n"]),
                                   "cities": sorted(o["cities"], key=lambda c: -o["cities"][c])[:3],
                                   "coverage": round(cov, 2)})
            claimed[(cc, name)].append((i["id"], cov))

    for (cc, name), v in claimed.items():
        if len(v) < 2:
            continue
        v.sort(key=lambda x: -x[1])
        keep = v[0][0] if v[0][1] - v[1][1] >= 0.15 else None
        for iid, _ in v:
            if iid != keep:
                found[iid] = [c for c in found[iid] if c["name"] != name]

    out = {}
    for i in sorted(site, key=lambda i: (i["country_code"], i["name"])):
        out[i["erasmus_code"]] = {"name": i["name"], "city": i["city"], "tier": i["tier"],
                                  "candidates": sorted(found[i["id"]], key=lambda c: -c["participants"])}
    MOBILITY_CANDIDATES.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"{sum(1 for v in out.values() if v['candidates'])}/{len(out)} laitokselle ehdotuksia -> {MOBILITY_CANDIDATES.name}")


if __name__ == "__main__":
    main()
