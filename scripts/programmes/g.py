"""g.py REGEX URL...  : hae sivut ja tulosta pääsisällön rivit, jotka osuvat regexiin (tiivis)."""
import sys, re
from f import get, text
sys.stdout.reconfigure(encoding="utf-8")
pat = re.compile(sys.argv[1], re.I)
for u in sys.argv[2:]:
    print("##", u)
    try: t = text(get(u))
    except Exception as e: print("ERR", e); continue
    seen = set()
    for l in t.splitlines():
        l = l.strip()
        if 3 < len(l) < 200 and pat.search(l) and l not in seen:
            seen.add(l); print("  ", l)
