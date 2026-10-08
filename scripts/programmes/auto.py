"""Automaattinen rivitys linkkilistauksesta: A(I, code, url, link_regex, drop_regex) -> rivit I[code]:een."""
import re, sys
from f import get, links
from mp import classify
LV = [("Doc", r"\bdoktor|\bphd\b|doctor|doctorat|dottorato|doctorado|tohtori"), ("MA", r"\bmaster|\bma\b|\bm\.?mus|\bmed\b|magist|laurea magistrale|biennio|2nd cycle|2e cycle|2ème cycle|deuxième cycle|segundo ciclo"),
      ("BA", r"\bbachelier|\bbachelor|\bba\b|\bb\.?mus|\bbed\b|bakalau|bachiller|grado|licence|triennio|1st cycle|1er cycle|premier cycle|primer ciclo|kandidat")]
def level(s):
    for lv, p in LV:
        if re.search(p, s, re.I): return lv
    return None
def A(I, code, url, pat, drop=None, default_level=None, quiet=False):
    seen = set(); unc = []
    for t, u in links(url, get(url)):
        if not re.search(pat, t + " " + u, re.I) or (drop and re.search(drop, t + " " + u, re.I)) or not t: continue
        if (t, u) in seen: continue
        seen.add((t, u))
        lv = level(t) or level(u) or default_level
        if lv == "Doc": continue  # tohtoritaso kirjataan alalle vain käsin, kun ala mainitaan
        ds = classify(t)
        if not ds: unc.append(t); continue
        for d in ds: I.setdefault(code, []).append([d, lv, t, u])
    if unc and not quiet: print(f"[{code}] luokittelematta: {unc}", file=sys.stderr)
from f import text
def T(I, code, url, pat, drop=None, default_level=None, quiet=False):
    """Kuten A, mutta sivun tekstiriveistä (kun ohjelmat eivät ole linkkejä)."""
    unc = []; seen = set()
    for l in (x.strip() for x in text(get(url)).splitlines()):
        if not l or l in seen or not re.search(pat, l, re.I) or (drop and re.search(drop, l, re.I)): continue
        seen.add(l)
        lv = level(l) or default_level
        if lv == "Doc": continue
        ds = classify(l)
        if not ds: unc.append(l); continue
        for d in ds: I.setdefault(code, []).append([d, lv, l[:150], url])
    if unc and not quiet: print(f"[{code}] luokittelematta: {unc}", file=sys.stderr)
