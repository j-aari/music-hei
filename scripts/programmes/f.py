"""f.py URL [link-regex] [-t]  : hae sivu (välimuisti), tulosta linkit (teksti | href) suodatettuna; -t tulostaa tekstin."""
import sys, re, os, hashlib, html, urllib.request, urllib.parse, ssl
sys.stdout.reconfigure(encoding="utf-8")
C = os.path.join(os.path.dirname(__file__), "cache")
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36", "Accept-Language": "en,de;q=0.8"}
def get(url):
    p = os.path.join(C, hashlib.md5(url.encode()).hexdigest())
    if os.path.exists(p): return open(p, encoding="utf-8").read()
    ctx = ssl.create_default_context(); ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
    r = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40, context=ctx)
    t = r.read().decode(r.headers.get_content_charset() or "utf-8", "replace")
    open(p, "w", encoding="utf-8").write(t); return t
def text(h):
    h = re.sub(r"(?is)<(script|style|noscript|svg)[^>]*>.*?</\1>", " ", h)
    h = re.sub(r"(?i)<(br|/p|/li|/h\d|/div|/tr)[^>]*>", "\n", h)
    return re.sub(r"[ \t]+", " ", re.sub(r"\n\s*\n+", "\n", html.unescape(re.sub(r"<[^>]+>", " ", h))))
def links(url, h):
    out = []
    for m in re.finditer(r'(?is)<a\b[^>]*href\s*=\s*["\']([^"\']+)["\'][^>]*>(.*?)</a>', h):
        t = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", m.group(2)))).strip()
        out.append((t, urllib.parse.urljoin(url, html.unescape(m.group(1)))))
    return out
if __name__ == "__main__":
    url = sys.argv[1]; pat = next((a for a in sys.argv[2:] if a != "-t"), None)
    try: h = get(url)
    except Exception as e: print("ERR", e); sys.exit()
    if "-t" in sys.argv: print(text(h)[:int(os.environ.get("N", 6000))]); sys.exit()
    seen = set()
    for t, u in links(url, h):
        if (t, u) in seen: continue
        seen.add((t, u))
        if pat is None or re.search(pat, t + " " + u, re.I): print(f"{t[:90]} | {u}")
