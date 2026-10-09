"""pf.py URL... : hae sivut rinnakkain curlilla välimuistiin (max 40 s/sivu); PDF muunnetaan tekstiksi. Tulostaa koon."""
import sys, os, hashlib, subprocess
from concurrent.futures import ThreadPoolExecutor
from f import C, UA
def one(u):
    p = os.path.join(C, hashlib.md5(u.encode()).hexdigest())
    if os.path.exists(p): return u, os.path.getsize(p)
    b = subprocess.run(["curl", "-skL", "--max-time", "40", "-A", UA["User-Agent"], u], capture_output=True).stdout
    if b[:4] == b"%PDF":  # PDF -> teksti, rivit <br>-eroteltuina, jotta text()/IT() toimivat
        b = subprocess.run(["pdftotext", "-enc", "UTF-8", "-layout", "-", "-"], input=b, capture_output=True).stdout
        b = b.replace(b"\n", b"<br>\n")
    t = b.decode("utf-8", "replace")
    if len(t) > 500: open(p, "w", encoding="utf-8").write(t)
    return u, len(t)
with ThreadPoolExecutor(12) as ex:
    for u, n in ex.map(one, sys.argv[1:]): print(n, u)
