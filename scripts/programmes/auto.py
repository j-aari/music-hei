"""Automaattinen rivitys linkkilistauksesta: A(I, code, url, link_regex, drop_regex) -> rivit I[code]:een."""
import re, sys
from f import get, links
from mp import classify
LV = [("Doc", r"\bdoktor|\bphd\b|doctor|doctorat|dottorato|doctorado|tohtori"), ("MA", r"\bmaster|\bma\b|\bm\.?mus|\bmed\b|magist|laurea magistrale|biennio|\bii°? livello|secondo livello|2° livello|accademico ii\b|2nd cycle|2e cycle|2ème cycle|deuxième cycle|segundo ciclo"),
      ("BA", r"\bbachelier|\bbachelor|\bba\b|\bb\.?mus|\bbed\b|bakalau|bachiller|grado|licence|triennio|\bi°? livello|primo livello|1° livello|1st cycle|1er cycle|premier cycle|primer ciclo|kandidat")]
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

NOISE = re.compile(r"esam|orari|appell|bando|graduator|news|notizi|docent|prof\.|m°|maestr[oa] |concert|masterclass|evento|seminar|calendar|iscrizion|ammission|regolament|piano di studi|tasse|contribut|segreteri|biblioteca|orchestra|coro del|ensemble|festival|premio|concorso|\d{4}|perfezionament|^didattica$|^produzione$|cerca|esplora|risorse|operativ|pagopa|^direzione$|^strumenti$|scuola di|dipartiment|programm|education\b|attività|week|prenotazion|aule|huayitong|corsi afam|ministerio|homologa|^ciclo de|teachers and students|stagioni|^sito |compimento|rivista|previgente|produzione|interpretazione scenica|compositivo|^la didattica", re.I)
def IT(I, code, url, lv, extra_drop=None):
    """Italialainen triennio/biennio-sivu: lyhyet rivit ja linkkitekstit, jotka luokittuvat aloiksi."""
    h = get(url); seen = set()
    cands = [t for t, _ in links(url, h)] + [l.strip() for l in text(h).splitlines()]
    for c in cands:
        c = re.sub(r"\s+", " ", c).strip(" -–•:")
        if not (3 < len(c) < 80) or c in seen or NOISE.search(c) or (extra_drop and re.search(extra_drop, c, re.I)): continue
        seen.add(c)
        for d in classify(c): I.setdefault(code, []).append([d, lv, c, url])
def L(I, code, names, url, lv):
    """Käsin koottu ohjelmalista (pilkuilla tai |:lla eroteltu, esim. bandon/manifestin PDF:stä) -> rivit."""
    unc = []
    for c in (x.strip() for x in re.split(r"[|;,]\s*(?![^()]*\))", names)):
        ds = classify(c)
        if not ds: unc.append(c)
        for d in ds: I.setdefault(code, []).append([d, lv, c, url])
    if unc: print(f"[{code}] luokittelematta: {unc}", file=sys.stderr)
def DC(I, code, url, maxlen=90):
    """Italian sivu/PDF, jossa ohjelmat ministeriön koodein (DCPL = triennio/BA, DCSL = biennio/MA)."""
    seen = set()
    for l in text(get(url)).splitlines():
        l = re.sub(r"\s+", " ", l).strip(" -–•:")
        m = re.search(r"DC([PS])L ?\d+", l)
        if not m or len(l) > maxlen or l in seen: continue
        seen.add(l)
        for d in classify(l): I.setdefault(code, []).append([d, "BA" if m.group(1) == "P" else "MA", l, url])
def SM(I, code, sm_url, pat, ba=r"triennio|i-livello|primo-livello", ma=r"biennio|ii-livello|secondo-livello", drop=None):
    """Ohjelmasivut sivuston XML-sivukartasta (WordPress tms.): nimi osoitteen viimeisestä osasta, taso osoitteesta."""
    import subprocess, os, hashlib
    from f import C
    p = os.path.join(C, hashlib.md5(sm_url.encode()).hexdigest())
    if os.path.exists(p): x = open(p, encoding="utf-8").read()
    else:
        x = subprocess.run(["curl", "-skL", "--max-time", "60", "-A", "Mozilla/5.0", sm_url], capture_output=True).stdout.decode("utf-8", "replace")
        if "<loc>" in x: open(p, "w", encoding="utf-8").write(x)
        else: print(f"[{code}] sivukartta tyhjä: {sm_url}", file=sys.stderr)
    for u in sorted(set(re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", x))):
        if not re.search(pat, u) or (drop and re.search(drop, u)): continue
        lv = "MA" if re.search(ma, u) else "BA" if re.search(ba, u) else None
        slug = re.sub(r"(\.html?|[-_]\d+)+$", "", u.rstrip("/").rsplit("/", 1)[-1])
        name = re.sub(r"[-_]+", " ", re.sub(r"[-_]?(triennio|biennio|accademico)?[-_]?(di[-_])?(i|ii|primo|secondo)[-_]livello.*$", "", slug)).strip()
        if not name: continue
        for d in classify(name): I.setdefault(code, []).append([d, lv, name, u])
