"""Etsi laitosten kansainvälisten asioiden yleisosoitteet niiden omilta sivuilta (data/contacts_candidates.json).

    python scripts/find_contacts.py              # kaikki laitokset, joilta ei vielä ole tarkistettua tietoa
    python scripts/find_contacts.py KOODI ...    # vain annetut Erasmus-koodit (välilyönnit alaviivoina, esim. I__MILANO09)

Lopullinen, käsin tarkistettu tieto on data/contacts.json; tämä skripti tuottaa vain ehdotukset.
Periaatteet (BACKLOG.md): vain toimistojen yleisosoitteet (international@…, erasmus@…), ei henkilöiden nimiä
eikä henkilökohtaisia osoitteita; jokaiselle osoitteelle tallennetaan sivu, jolta se löytyi.

Haku: laitoksen etusivu ja siitä avautuvat saman sivuston sivut, joiden linkkiteksti tai osoite viittaa
kansainvälisiin asioihin (international, erasmus, mobility, relazioni internazionali, …), kaksi tasoa syvälle,
enintään MAX_PAGES sivua laitosta kohden ja yksi pyyntö sekunnissa samalle sivustolle (WORKERS laitosta rinnakkain).
"""

import html
import json
import re
import ssl
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser

from common import DATA, SITE

CANDIDATES = DATA / "contacts_candidates.json"
CONTACTS = DATA / "contacts.json"
MAX_PAGES = 22
WORKERS = 8  # eri laitoksia yhtä aikaa
# Yleisimmät kv-sivujen polut; kokeillaan etusivun lisäksi, koska valikot ovat usein JavaScriptiä
SEED_PATHS = ["international", "en/international", "erasmus", "en/erasmus", "internationales", "international-office",
              "en/international-office", "internazionale", "erasmus-plus", "relazioni-internazionali", "internacional",
              "relations-internationales", "en/study/international", "en/exchange", "exchange"]
UA = "Mozilla/5.0 (compatible; music-hei/1.0; static list of European music institutions; one request per second)"

LINK_WORDS = re.compile(
    r"internation|erasmus|mobilit|exchange|incoming|outgoing|study.abroad|austausch|ausland|relazioni.intern|"
    r"internazional|internacional|relaciones.intern|relacions.intern|relations.intern|echanges|échanges|"
    r"kansainv|internasjonal|internationell|utbytte|utbyte|międzynarod|miedzynarod|zahranič|zahranic|nemzetközi|"
    r"nemzetkozi|rahvusvahel|tarptautin|starptautisk|mednarod|uluslararas|relatii.intern|relații|"
    r"contact|kontakt|contatti|contacto|contacte", re.I)
# Paikallisosan sanat, jotka kertovat toimiston yleisosoitteesta
GENERIC_LOCAL = re.compile(
    r"internation|intl|erasmus|mobil|exchange|incoming|outgoing|io$|^io[._-]|^ri$|^ri[._-]|relint|relaz|relinter|"
    r"inter\b|international|auslands|aaa|ausland|kv|global|abroad|intern$|^intl|relaciones|relacions|relations|ori$|"
    r"^dri|^sri|^isc|^iro|^ico|^oir|exchange|mobility|interoffice|zagranic|zahranic|nemzetkozi|world|europ", re.I)
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links, self.emails, self._href, self._text = [], set(), None, []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "a" and a.get("href"):
            self._href, self._text = a["href"], []
            if a["href"].lower().startswith("mailto:"):
                self.emails.add(urllib.parse.unquote(a["href"][7:].split("?")[0]))
        for k, v in attrs:  # Cloudflaren ja TYPO3:n suojaamat osoitteet
            if k == "data-cfemail" and v:
                self.emails.add(decode_cf(v))
            if k == "data-mailto-token" and v:
                self.emails.add(decode_typo3(v))
            if k == "href" and v and "linkTo_UnCryptMailto" in v:
                m = re.search(r"UnCryptMailto\((?:%27|')([^'%]+(?:%[0-9A-F]{2}[^'%]*)*?)(?:%27|')", v)
                if m:
                    self.emails.add(decode_typo3(urllib.parse.unquote(m.group(1))))
            if k == "href" and v and "/cdn-cgi/l/email-protection#" in v:
                self.emails.add(decode_cf(v.split("#", 1)[1]))

    def handle_data(self, data):
        if self._href is not None:
            self._text.append(data)

    def handle_endtag(self, tag):
        if tag == "a" and self._href is not None:
            self.links.append((self._href, " ".join(self._text).strip()))
            self._href = None


def decode_typo3(token):
    """TYPO3 spamProtectEmailAddresses: merkit siirretty n askelta kolmen merkkialueen sisällä; n selvitetään kokeilemalla."""
    ranges = ((0x2B, 0x3A), (0x40, 0x5A), (0x61, 0x7A))
    for n in range(1, 11):
        out = []
        for ch in token:
            c = ord(ch)
            for lo, hi in ranges:
                if lo <= c <= hi:
                    c -= n
                    if c < lo:
                        c += hi - lo + 1
                    break
            out.append(chr(c))
        t = "".join(out)
        if t.startswith("mailto:"):
            return t[7:].replace("\\", "")
    return ""


def decode_cf(hexstr):
    try:
        key = int(hexstr[:2], 16)
        return "".join(chr(int(hexstr[i:i + 2], 16) ^ key) for i in range(2, len(hexstr), 2))
    except ValueError:
        return ""


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "en,*;q=0.5"})
    try:
        return _read(urllib.request.urlopen(req, timeout=20))
    except urllib.error.URLError as e:
        # Some institutions' certificates are broken (wrong host name, missing chain). Public pages are only read, so retry unverified.
        if isinstance(getattr(e, "reason", None), ssl.SSLError):
            return _read(urllib.request.urlopen(req, timeout=20, context=ssl._create_unverified_context()))
        raise


def _read(resp):
    with resp as r:
        if "html" not in r.headers.get("Content-Type", ""):
            return None, r.geturl()
        raw = r.read(3_000_000)
        cs = r.headers.get_content_charset() or "utf-8"
        return raw.decode(cs, "replace"), r.geturl()


def site_root(host):
    parts = host.lower().split(".")
    return ".".join(parts[-3:]) if len(parts) > 2 and len(parts[-2]) <= 3 else ".".join(parts[-2:])


def text_emails(text):
    t = re.sub(r"\s*[\[\(\{]\s*(at|ät|chiocciola|arroba)\s*[\]\)\}]\s*", "@", text, flags=re.I)
    t = re.sub(r"\s*[\[\(\{]\s*(dot|punto|punkt|point)\s*[\]\)\}]\s*", ".", t, flags=re.I)
    return set(EMAIL.findall(t))


def crawl(start):
    """Palauttaa {osoite: ensimmäinen sivu, jolta löytyi} ja luetut sivut."""
    root = site_root(urllib.parse.urlparse(start).hostname or "")
    queue, seen, found, pages = [(start, 0, 10)], set(), {}, []
    seeded = False
    while queue and len(pages) < MAX_PAGES:
        queue.sort(key=lambda x: -x[2])
        url, depth, _ = queue.pop(0)
        if url in seen:
            continue
        seen.add(url)
        try:
            body, final = fetch(url)
        except Exception as e:  # noqa: BLE001 - verkkovirheet vain kirjataan
            pages.append((url, f"error: {e.__class__.__name__}"))
            time.sleep(1)
            continue
        time.sleep(1)
        pages.append((final, "ok"))
        if not seeded:  # after the home page: follow redirects to another domain, add the common paths
            seeded = True
            root = site_root(urllib.parse.urlparse(final).hostname or "") or root
            base = "{0.scheme}://{0.netloc}/".format(urllib.parse.urlparse(final))
            queue += [(base + sp, 1, 3) for sp in SEED_PATHS]
        if body is None:
            continue
        p = Page()
        try:
            p.feed(body)
        except Exception:  # noqa: BLE001
            continue
        for e in p.emails | text_emails(html.unescape(re.sub(r"<[^>]+>", " ", body))):
            e = e.strip().strip(".").lower()
            if "@" in e and not e.endswith((".png", ".jpg", ".gif", ".webp", ".svg")):
                found.setdefault(e, final)
        if depth >= 2:
            continue
        for href, text in p.links:
            u = urllib.parse.urljoin(final, href.split("#")[0])
            host = urllib.parse.urlparse(u).hostname or ""
            if not u.startswith("http") or not host.endswith(root) or u in seen:
                continue
            if re.search(r"\.(pdf|jpg|png|zip|docx?|xlsx?|mp3|mp4)$", u, re.I):
                continue
            hay = f"{text} {urllib.parse.unquote(u)}"
            if LINK_WORDS.search(hay):
                score = 5 if re.search(r"internation|erasmus|mobilit|exchange|relazioni|relaciones|relations|kansainv|ausland", hay, re.I) else 1
                queue.append((u, depth + 1, score - depth))
    return found, pages, root


def classify(email, root):
    local, _, domain = email.partition("@")
    return {
        "email": email,
        "same_site": domain.endswith(root) or root.endswith(domain),
        "generic": bool(GENERIC_LOCAL.search(local)),
    }


def main(codes):
    site = json.loads(SITE.read_text(encoding="utf-8"))["institutions"]
    done = json.loads(CONTACTS.read_text(encoding="utf-8")) if CONTACTS.exists() else {}
    out = json.loads(CANDIDATES.read_text(encoding="utf-8")) if CANDIDATES.exists() else {}
    if codes:
        todo = [i for i in site if i["erasmus_code"] in codes]
    else:  # laitokset, joilta ei ole tarkistettua tietoa eikä vielä ehdotuksia
        todo = [i for i in site if i["erasmus_code"] not in done and i["erasmus_code"] not in out]
    lock = threading.Lock()

    def one(i):
        found, pages, root = crawl(i["website"])
        cands = [dict(classify(e, root), page=u) for e, u in found.items()]
        cands.sort(key=lambda c: (not c["generic"], not c["same_site"], c["email"]))
        with lock:
            out[i["erasmus_code"]] = {"name": i["name"], "website": i["website"], "candidates": cands,
                                      "pages": [u for u, s in pages if s == "ok"], "errors": [f"{u} {s}" for u, s in pages if s != "ok"]}
            CANDIDATES.write_text(json.dumps(dict(sorted(out.items())), ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
            g = [c["email"] for c in cands if c["generic"]]
            print(f"[{len(out)}] {i['erasmus_code']}: {', '.join(g[:3]) or '-'}", flush=True)

    # Rinnakkain eri laitosten sivustoille; kunkin sivuston sisällä edelleen yksi pyyntö sekunnissa
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        list(ex.map(one, todo))


if __name__ == "__main__":
    main({a.replace("_", " ") for a in sys.argv[1:]})
