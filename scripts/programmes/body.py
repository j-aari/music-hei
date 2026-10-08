"""body.py URL [START-REGEX] [N] : tulosta sivun teksti alkaen START-osumasta (oletus: alusta), N riviä, lyhyet rivit."""
import sys, re
from f import get, text
sys.stdout.reconfigure(encoding="utf-8")
u = sys.argv[1]; st = sys.argv[2] if len(sys.argv) > 2 else None; n = int(sys.argv[3]) if len(sys.argv) > 3 else 80
try: lines = [l.strip() for l in text(get(u)).splitlines() if l.strip()]
except Exception as e: print("ERR", e); sys.exit()
i = 0
if st:
    hits = [k for k, l in enumerate(lines) if re.search(st, l, re.I)]
    i = hits[-1] if hits else 0
print("##", u); print("\n".join(l[:180] for l in lines[i:i + n]))
