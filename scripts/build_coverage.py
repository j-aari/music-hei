"""Laske katvealueet: alueet, joilta on yli 300 km lähimpään mukana olevaan laitokseen.

Lähtötiedot: laitosten koordinaatit (data/site.json) ja maiden rajat (Natural Earth 110 m,
data/reference/, public domain). Tulos: data/coverage.json (+ kopio site/data/), jonka sivu piirtää kartalle.

Menetelmä
  - ruudukko 0,1 asteen välein (n. 11 km) Euroopan alueella (lat 34-72, lon -25...45)
  - jokaisen ruudun keskipisteestä lasketaan suuriympyrämatka (haversine) lähimpään laitokseen
  - katveessa on ruutu, jonka lähin laitos on yli THRESHOLD_KM päässä JA joka on jonkin ECHE-listan maan maa-alueella
    (sen maan, jossa on ECHE-haltijoita; muiden maiden ja merialueiden katvetta ei raportoida)
  - SAMAN MAAN SÄÄNTÖ: ruutu on katve, jos yhtäkään laitosta ei ole THRESHOLD_KM (300 km) sisällä eikä samassa maassa
    olevaa laitosta SAME_COUNTRY_KM (600 km) sisällä. Jos ruudulla ei ole laitosta 300 km:n sisällä mutta samassa maassa
    on laitos 300-600 km:n päässä, ruutua ei lasketa katveeksi; se tallennetaan erikseen (runs_same_country) ja
    näytetään vaaleampana. Eri maan laitokseen raja on siis 300 km, saman maan laitokseen 600 km.
  - etäisyys lasketaan kaikkiin laitoksiin maasta riippumatta, joten rajan takana oleva laitos kattaa myös
  - tulos tallennetaan riveinä [lat, lon_alku, lon_loppu] (peräkkäiset katveruudut yhdistetty)
Rajat ovat 110 m -tarkkuudella, joten reunat ovat likimääräisiä (muutaman kilometrin luokkaa).
Standardikirjasto vain.
"""

import json
import math
import sys
from collections import defaultdict

from common import COVERAGE, NE_COUNTRIES, SITE, UPSTREAM, publish, today

THRESHOLD_KM = 300       # raja laitokseen, joka voi olla missä maassa tahansa
SAME_COUNTRY_KM = 600    # raja saman maan laitokseen
STEP = 0.1  # aste
LAT_MIN, LAT_MAX, LON_MIN, LON_MAX = 34.0, 72.0, -25.0, 45.0  # Eurooppa; sulkee pois mm. Guyanan ja Huippuvuoret
R = 6371.0088
KM_PER_DEG_LAT = math.pi * R / 180


def haversine(lat1, lon1, lat2, lon2):
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi, dl = p2 - p1, math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


def ring_bbox(ring):
    xs = [p[0] for p in ring]
    ys = [p[1] for p in ring]
    return min(xs), min(ys), max(xs), max(ys)


def in_ring(x, y, ring):
    inside = False
    j = len(ring) - 1
    for i in range(len(ring)):
        xi, yi = ring[i][0], ring[i][1]
        xj, yj = ring[j][0], ring[j][1]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi) + xi:
            inside = not inside
        j = i
    return inside


def ring_area_km2(ring):
    """Likimääräinen pinta-ala: pallonpinnan kaava (Chamberlain-Duquette), kelpaa pienille alueille."""
    s = 0.0
    for i in range(len(ring) - 1):
        (x1, y1), (x2, y2) = ring[i][:2], ring[i + 1][:2]
        s += math.radians(x2 - x1) * (2 + math.sin(math.radians(y1)) + math.sin(math.radians(y2)))
    return abs(s * R * R / 2)


def load_countries():
    """[(iso2, [polygon: (bbox, outer_ring, [holes])])] ECHE-listan maille, vain tutkimusalueella."""
    eche = {r["countryCodeIso"] for r in json.loads(UPSTREAM.read_text(encoding="utf-8")) if r.get("countryCodeIso")}
    out = defaultdict(list)
    names = {}
    for ft in json.loads(NE_COUNTRIES.read_text(encoding="utf-8"))["features"]:
        iso = ft["properties"]["ISO_A2_EH"]
        if iso not in eche:
            continue
        names[iso] = ft["properties"]["NAME"]
        geom = ft["geometry"]
        polys = geom["coordinates"] if geom["type"] == "MultiPolygon" else [geom["coordinates"]]
        for poly in polys:
            bx = ring_bbox(poly[0])
            if bx[2] < LON_MIN or bx[0] > LON_MAX or bx[3] < LAT_MIN or bx[1] > LAT_MAX:
                continue  # kokonaan tutkimusalueen ulkopuolella (esim. Guyana, Huippuvuoret)
            out[iso].append((bx, poly[0], poly[1:]))
    return out, names, eche


def on_land(x, y, polys):
    for bx, outer, holes in polys:
        if bx[0] <= x <= bx[2] and bx[1] <= y <= bx[3] and in_ring(x, y, outer) and not any(in_ring(x, y, h) for h in holes):
            return True
    return False


class Runs:
    """Kerää peräkkäiset ruudut riveiksi [lat, lon_alku, lon_loppu]."""

    def __init__(self):
        self.runs = []
        self.start = self.end = None

    def add(self, lon):
        if self.start is None:
            self.start = lon
        self.end = lon

    def flush(self, lat):
        if self.start is not None:
            self.runs.append([round(lat, 2), round(self.start, 2), round(self.end, 2)])
            self.start = None


def main():
    insts = [(i["lat"], i["lon"], i["country_code"])
             for i in json.loads(SITE.read_text(encoding="utf-8"))["institutions"] if i.get("lat") is not None]
    by_country_insts = defaultdict(list)
    for la, lo, cc in insts:
        by_country_insts[cc].append((la, lo))
    countries, names, eche = load_countries()
    lat_band = THRESHOLD_KM / KM_PER_DEG_LAT
    n_rows = int(round((LAT_MAX - LAT_MIN) / STEP))
    n_cols = int(round((LON_MAX - LON_MIN) / STEP))

    counted, same_country = Runs(), Runs()  # katve ja "yli 300 km, mutta samassa maassa kuin lähin laitos"
    gap_area = defaultdict(float)     # lasketaan katveeksi
    exempt_area = defaultdict(float)  # yli 300 km, mutta samassa maassa kuin lähin laitos: ei lasketa
    for r in range(n_rows):
        lat = LAT_MIN + STEP * (r + 0.5)
        near = [p for p in insts if abs(p[0] - lat) <= lat_band]  # muut ovat varmasti yli rajan
        cell_km2 = (STEP * KM_PER_DEG_LAT) ** 2 * math.cos(math.radians(lat))
        for c in range(n_cols):
            lon = LON_MIN + STEP * (c + 0.5)
            if any(haversine(lat, lon, la, lo) <= THRESHOLD_KM for la, lo, _ in near):
                counted.flush(lat)
                same_country.flush(lat)
                continue
            iso = next((k for k, polys in countries.items() if on_land(lon, lat, polys)), None)
            if iso is None:
                counted.flush(lat)
                same_country.flush(lat)
                continue
            if any(haversine(lat, lon, la, lo) <= SAME_COUNTRY_KM for la, lo in by_country_insts.get(iso, ())):
                # Samassa maassa on laitos enintään SAME_COUNTRY_KM päässä (ja yli THRESHOLD_KM): ei lasketa katveeksi
                exempt_area[iso] += cell_km2
                same_country.add(lon)
                counted.flush(lat)
            else:
                gap_area[iso] += cell_km2
                counted.add(lon)
                same_country.flush(lat)
        counted.flush(lat)
        same_country.flush(lat)

    area = {k: sum(ring_area_km2(o) - sum(ring_area_km2(h) for h in hs) for _, o, hs in polys) for k, polys in countries.items()}
    touched = set(gap_area) | set(exempt_area)
    by_country = {
        k: {
            "name": names[k],
            "gap_km2": round(gap_area[k]),
            "same_country_km2": round(exempt_area[k]),
            "area_km2": round(area[k]),
            "share": round(gap_area[k] / area[k], 4),
            "far_share": round((gap_area[k] + exempt_area[k]) / area[k], 4),
        }
        for k in sorted(touched, key=lambda k: (-gap_area[k] / area[k], -exempt_area[k] / area[k]))
    }
    total_gap, total_exempt, total_area = sum(gap_area.values()), sum(exempt_area.values()), sum(area.values())
    out = {
        "meta": {
            "threshold_km": THRESHOLD_KM,
            "grid_deg": STEP,
            "institutions": len(insts),
            "computed": today(),
            "extent": {"lat": [LAT_MIN, LAT_MAX], "lon": [LON_MIN, LON_MAX]},
            "same_country_km": SAME_COUNTRY_KM,
            "distance": "great-circle (haversine) to an included institution",
            "rule": "An area counts as uncovered when no institution in any country is within threshold_km and no institution in the "
                    "same country is within same_country_km. Areas more than threshold_km from every institution but within "
                    "same_country_km of one in their own country are listed separately (runs_same_country) and not counted.",
            "area_covered": "land area of the countries on the ECHE list, within the extent",
            "gap_km2": round(total_gap),
            "same_country_km2": round(total_exempt),
            "area_km2": round(total_area),
            "gap_share": round(total_gap / total_area, 4),
            "far_share": round((total_gap + total_exempt) / total_area, 4),
            "by_country": by_country,
        },
        "runs": counted.runs,
        "runs_same_country": same_country.runs,
    }
    COVERAGE.write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    publish(COVERAGE)
    print(f"Laitoksia {len(insts)}, ruudukko {STEP}° ({n_rows}x{n_cols}), rivejä: katve {len(counted.runs)}, sama maa {len(same_country.runs)}, {COVERAGE.stat().st_size // 1024} kt")
    print(f"Yli {THRESHOLD_KM} km yhteensä {(total_gap + total_exempt) / 1e6:.2f} milj. km² = {100 * (total_gap + total_exempt) / total_area:.1f} % ECHE-maiden pinta-alasta (ennen rajausta)")
    print(f"  josta lasketaan katveeksi {total_gap / 1e6:.2f} milj. km² = {100 * total_gap / total_area:.1f} %; samassa maassa laitos {THRESHOLD_KM}-{SAME_COUNTRY_KM} km:n päässä (ei lasketa) {total_exempt / 1e6:.2f} milj. km² = {100 * total_exempt / total_area:.1f} %")
    print(f"{'Maa':22} {'ennen':>7} {'nyt':>7}   ({'katve':>8} + {'sama maa':>8} km²)")
    for k, v in by_country.items():
        print(f"  {v['name']:20} {100 * v['far_share']:6.1f}% {100 * v['share']:6.1f}%   ({v['gap_km2']:>8,} + {v['same_country_km2']:>8,})")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
