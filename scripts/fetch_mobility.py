"""Hae Erasmus+ KA1 -liikkuvuusdata (Euroopan komissio, "Erasmus+ Mobility Raw Data") ja poimi korkeakoulurivit.

    python scripts/fetch_mobility.py          # lataa puuttuvat vuodet ja poimii niistä korkeakoulurivit
    python scripts/fetch_mobility.py --force  # lataa ja poimii kaikki uudelleen

Lähde: https://data.europa.eu/data/datasets/erasmus-mobility-raw-data (yksi xlsx-tiedosto aloitusvuotta kohden).
Raakatiedostot (~600 Mt) tallennetaan data/raw/mobility/-kansioon, joka ei ole versionhallinnassa. Jokaisesta
vuodesta poimitaan vain Field = "Higher Education" -rivit tiiviiksi CSV:ksi (he_YYYY.csv.gz), jota
build_mobility.py lukee. Xlsx luetaan standardikirjastolla (zipfile + iterparse), koska skriptit eivät käytä
kolmannen osapuolen kirjastoja.

Vuodet: YEARS alla. Uusimmat vuodet ovat vajaita, koska komissio julkaisee lopulliset luvut vasta kun hanke
(kesto jopa 3 vuotta) on suljettu; siksi sivun yhteenveto rajataan vuoteen build_mobility.LAST_YEAR asti.
"""

import csv
import gzip
import re
import sys
import urllib.request
import zipfile
from xml.etree.ElementTree import iterparse

from common import MOBILITY_RAW

URL = "https://ec.europa.eu/assets/eac/erasmus-plus/statistics/mobility/Erasmus-KA1-Mobility-Data-{year}.xlsx"
YEARS = range(2014, 2023)

NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
# Otsikot vaihtelevat vuosittain; kaikki muodot yhtenäistetään näihin nimiin
ALIASES = {
    "Mobility Start Year/Month": "Mobility Start Month",
    "Mobility Duration - calendar days": "Mobility Duration",
    "Sending Organisation": "Sending Organization",
    "Receiving Organisation": "Receiving Organization",
}
KEEP = ["Academic Year", "Mobility Start Month", "Mobility Duration", "Activity (mob)", "Field of Education",
        "Participant Profile", "Sending Country", "Sending City", "Sending Organization",
        "Receiving Country", "Receiving City", "Receiving Organization", "Participants"]


def col_index(ref):
    """Solun viite (esim. 'AB12') -> sarakeindeksi 0:sta."""
    n = 0
    for ch in re.match(r"[A-Z]+", ref).group():
        n = n * 26 + ord(ch) - 64
    return n - 1


def xlsx_rows(path):
    """Ensimmäisen taulukon rivit listoina (tyhjät solut ''), luettuna virtana."""
    with zipfile.ZipFile(path) as z:
        shared = []
        if "xl/sharedStrings.xml" in z.namelist():
            with z.open("xl/sharedStrings.xml") as f:
                for _, el in iterparse(f):
                    if el.tag == NS + "si":
                        shared.append("".join(t.text or "" for t in el.iter(NS + "t")))
                        el.clear()
        sheet = sorted(n for n in z.namelist() if re.match(r"xl/worksheets/sheet\d+\.xml$", n))[0]
        with z.open(sheet) as f:
            for _, el in iterparse(f):
                if el.tag != NS + "row":
                    continue
                row = []
                for c in el.iter(NS + "c"):
                    i = col_index(c.get("r"))
                    while len(row) < i:
                        row.append("")
                    t = c.get("t")
                    if t == "s":
                        v = shared[int(c.find(NS + "v").text)]
                    elif t == "inlineStr":
                        v = "".join(x.text or "" for x in c.iter(NS + "t"))
                    else:
                        v = c.find(NS + "v")
                        v = v.text if v is not None else ""
                    row.append(v)
                yield row
                el.clear()


def extract(xlsx, out):
    """Poimi korkeakoulurivit tiiviiksi CSV:ksi. Palauttaa (rivejä, korkeakoulurivejä)."""
    rows = xlsx_rows(xlsx)
    hdr = [ALIASES.get(h.strip(), h.strip()) for h in next(rows)]
    hdr = ["Participants" if h.startswith("Actual Participants") else h for h in hdr]
    ix = {h: i for i, h in enumerate(hdr)}
    missing = [k for k in KEEP + ["Field"] if k not in ix]
    if missing:
        sys.exit(f"{xlsx.name}: sarakkeet puuttuvat: {missing}")
    n = he = 0
    with gzip.open(out, "wt", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(KEEP)
        for r in rows:
            n += 1
            if len(r) <= ix["Field"] or r[ix["Field"]] != "Higher Education":
                continue
            he += 1
            w.writerow([r[ix[k]] if ix[k] < len(r) else "" for k in KEEP])
    return n, he


def main(force=False):
    MOBILITY_RAW.mkdir(parents=True, exist_ok=True)
    for year in YEARS:
        xlsx = MOBILITY_RAW / f"Erasmus-KA1-Mobility-Data-{year}.xlsx"
        out = MOBILITY_RAW / f"he_{year}.csv.gz"
        if force or not xlsx.exists():
            print(f"{year}: ladataan {URL.format(year=year)}", flush=True)
            urllib.request.urlretrieve(URL.format(year=year), xlsx)
        if force or not out.exists():
            n, he = extract(xlsx, out)
            print(f"{year}: {n} riviä, joista korkeakoulu {he}", flush=True)
        else:
            print(f"{year}: valmiina ({out.name})")


if __name__ == "__main__":
    main(force="--force" in sys.argv)
