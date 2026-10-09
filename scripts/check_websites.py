"""Tarkista site.json-verkko-osoitteet: kuolleet, kaapatut (kasino-/vedonlyöntimainokset, myytävä verkkotunnus) ja oletussivut.

Käyttö: python scripts/check_websites.py

Tulostaa vain epäilyttävät. "HTTP 000" voi olla myös hidas tai bottiesto; tarkista selaimella.
Korjaus: data/annotations.json -> website_override (itsenäinen laitos) tai unit_website (yliopiston yksikkö).
"""

import json
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

from common import SITE

BAD = re.compile(r"casino|scommesse|betting|sportwetten|apuestas|online slot|kasyno|bukmacher|paris sportifs"
                 r"|domain (is )?for sale|buy this domain|parked|domain default page|web site not found", re.I)
MUSIC = re.compile(r"musi|conserv|hochschule|akadem|academ|muzik|zene|glazb|hudob|universit", re.I)
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126 Safari/537.36"


def check(inst):
    r = subprocess.run(["curl", "-skL", "--max-time", "40", "-A", UA, "-w", "\n@@%{http_code} %{url_effective}", inst["website"]],
                       capture_output=True)
    body, _, tail = r.stdout.decode("utf-8", "replace").rpartition("\n@@")
    code, _, final = tail.partition(" ")
    title = (re.search(r"(?is)<title[^>]*>(.*?)</title>", body) or [None, ""])[1].strip()[:70]
    flags = []
    if code == "000" or code[:1] in "45":
        flags.append(f"HTTP {code or '000'}")
    m = BAD.search(body[:200000]) or BAD.search(title)
    if m:
        flags.append(f"sisältö: {m.group(0)}")
    if body and not MUSIC.search(body[:300000]):
        flags.append("ei musiikkisanaa")
    return inst["erasmus_code"], inst["website"], final, title, flags


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    insts = json.loads(SITE.read_text(encoding="utf-8"))["institutions"]
    with ThreadPoolExecutor(4) as ex:  # enemmän rinnakkaisuutta antaa vääriä aikakatkaisuja
        for code, url, final, title, flags in ex.map(check, insts):
            if flags:
                print(f"{code} | {url} -> {final} | {title!r} | {', '.join(flags)}")


if __name__ == "__main__":
    main()
