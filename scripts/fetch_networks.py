"""Hae verkostojen jäsenluettelot (data/raw/networks/) laitosjäsenyyksien tarkistamista varten.

    python scripts/fetch_networks.py

Kartoitetut verkostot ja lähteet:
  - AEC (Association Européenne des Conservatoires): https://aec-music.eu/members/our-members/page-N.
    Sivutus toistaa osan jäsenistä ja jättää osan pois, joten luettelo täydennetään sivuston avainsanahaulla
    jokaisen sivun laitoksen kaupungin nimellä (…/our-members/search?keyword=…).
  - EUA (European University Association): https://www.eua.eu/our-membership/member-directory.html
    (yksi sivu; jäsenillä verkko-osoite, jolla ne yhdistetään laitoksiin).
Tulokset: data/raw/networks/aec_members.json ja eua_members.json (ei versionhallinnassa).
Laitosten jäsenyydet on tarkistettu näiden perusteella käsin tiedostoon data/networks.json
(AEC nimen ja kaupungin, EUA verkko-osoitteen perusteella); tämä skripti ei kirjoita sitä.
"""

import html
import json
import re
import time
import urllib.parse
import urllib.request

from common import ROOT, SITE

OUT = ROOT / "data" / "raw" / "networks"
UA = {"User-Agent": "Mozilla/5.0 (compatible; music-hei/1.0; static list of European music institutions)"}
AEC_CARD = re.compile(r'<li class="member-location">\s*(.*?)\s*</li>.*?<h3>\s*<a href="(https://aec-music.eu/member/[^"]+)">\s*(.*?)\s*</a>')


def get(url):
    return re.sub(r"\s+", " ", urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30).read().decode("utf-8", "replace"))


def aec_cards(page, members):
    n = 0
    for loc, url, name in AEC_CARD.findall(page):
        place, _, cat = html.unescape(loc).rpartition("|")
        if url not in members:
            members[url] = {"name": html.unescape(name).strip(), "url": url, "place": place.strip(), "category": cat.strip()}
            n += 1
    return n


def fetch_aec():
    members = {}
    n = 1
    while True:
        page = get(f"https://aec-music.eu/members/our-members/page-{n}")
        if not AEC_CARD.search(page):
            break
        aec_cards(page, members)
        n += 1
        time.sleep(1)
    site = json.loads(SITE.read_text(encoding="utf-8"))["institutions"]
    for city in sorted({re.split(r"[ (,]", i["city"])[0] for i in site}):
        aec_cards(get("https://aec-music.eu/members/our-members/search?keyword=" + urllib.parse.quote(city)), members)
        time.sleep(1)
    return list(members.values())


def fetch_eua():
    page = get("https://www.eua.eu/our-membership/member-directory.html")
    out = []
    for cls, text, rest in re.findall(r'<div class="member3item ([^"]+)"> <div id="searchContent" class="content" style="display:none;"> (.*?) </div>(.*?)(?=<div class="member3item|$)', page):
        web = re.search(r'href="(http[^"]+)" target="_blank" aria-label="Visit Website', rest)
        out.append({"class": cls, "text": html.unescape(text), "website": web.group(1) if web else None})
    return out


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    aec = fetch_aec()
    (OUT / "aec_members.json").write_text(json.dumps(aec, ensure_ascii=False, indent=1), encoding="utf-8")
    eua = fetch_eua()
    (OUT / "eua_members.json").write_text(json.dumps(eua, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"AEC {len(aec)} jäsentä, EUA {len(eua)} jäsentä -> {OUT}")


if __name__ == "__main__":
    main()
