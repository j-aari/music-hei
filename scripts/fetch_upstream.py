"""Vaihe 1: hae ECHE-lista rajapinnasta, kirjoita data/upstream.json ja tulosta yhteenveto.

Kentät on otettu OpenAPI-specistä (https://eche-list.erasmuswithoutpaper.eu/static/redoc/dist.yaml).
upstream.json ylikirjoitetaan kokonaan; omat merkinnät kuuluvat annotations.json-tiedostoon.
Haun päivä kirjataan data/upstream.meta.json-tiedostoon (site.json:n hakupäivä tulee sieltä).
"""

import json
import sys
import urllib.request
from collections import Counter

from common import UPSTREAM, UPSTREAM_META, today

API = "https://eche-list.erasmuswithoutpaper.eu/api/?_verified=all"
USER_AGENT = "music-hei-eche-fetch/0.1"


def fetch():
    """Hakee koko listan muistiin kirjoittamatta mitään."""
    req = urllib.request.Request(API, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        print(f"HTTP {resp.status}, X-Rate-Limit: {resp.headers.get('X-Rate-Limit')}")
        return json.load(resp)


def write(rows):
    """Ylikirjoittaa upstream.json:n ja metatiedoston."""
    UPSTREAM.parent.mkdir(exist_ok=True)
    UPSTREAM.write_text(json.dumps(rows, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    UPSTREAM_META.write_text(
        json.dumps({"source": API, "fetched": today(), "rows": len(rows)}, ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8",
    )


def main():
    rows = fetch()
    write(rows)

    print(f"Rivejä: {len(rows)}  ->  {UPSTREAM}")

    keys = Counter(k for r in rows for k in r)
    vkeys = Counter(k for r in rows for k in (r.get("_verified") or {}))
    print("\nKentät (täytettyjä / rivejä):")
    for k, _ in keys.items():
        filled = sum(1 for r in rows if r.get(k) not in (None, ""))
        print(f"  {k:28} {filled:5} / {len(rows)}")
    print("\n_verified-kentät:")
    for k in vkeys:
        filled = sum(1 for r in rows if (r.get("_verified") or {}).get(k) not in (None, ""))
        print(f"  {k:28} {filled:5} / {len(rows)}")

    codes = [r["erasmusCode"] for r in rows]
    oids = [r["oid"] for r in rows if r.get("oid")]
    print(f"\nErasmus-koodeja uniikkeja: {len(set(codes))} / {len(codes)}")
    print(f"OID:eja uniikkeja: {len(set(oids))} / {len(oids)} (null: {len(rows) - len(oids)})")

    print("\nMaat (top 10):")
    for c, n in Counter(r["countryName"] for r in rows).most_common(10):
        print(f"  {c:28} {n}")

    print("\nEsimerkkirivi:")
    print(json.dumps(rows[0], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
