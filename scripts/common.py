"""Yhteiset polut ja apufunktiot skripteille."""

import json
import os
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = Path(os.environ["MUSIC_HEI_DATA"]) if os.environ.get("MUSIC_HEI_DATA") else ROOT / "data"  # ohitus testejä varten
UPSTREAM = DATA / "upstream.json"
UPSTREAM_META = DATA / "upstream.meta.json"
ANNOTATIONS = DATA / "annotations.json"
GEO = DATA / "geo.json"
SITE = DATA / "site.json"


def key_of(r):
    """Annotaatioiden avain: normalisoitu Erasmus-koodi, muuten raaka koodi."""
    return r["erasmusCodeNormalized"] or r["erasmusCode"]


def load_upstream():
    """Upstream-rivit avaimen mukaan."""
    return {key_of(r): r for r in json.loads(UPSTREAM.read_text(encoding="utf-8"))}


def load_annotations():
    """(aktiiviset annotaatiot, orphaned-osio). Orphaned on annotations.json:n oma osionsa."""
    data = json.loads(ANNOTATIONS.read_text(encoding="utf-8"))
    orphaned = data.pop("orphaned", {})
    return data, orphaned


def save_annotations(active, orphaned):
    """Kirjoittaa annotations.json:n. Kutsutaan vain kun käyttäjä on pyytänyt (orphaned-siirto)."""
    out = dict(sorted(active.items()))
    if orphaned:
        out["orphaned"] = dict(sorted(orphaned.items()))
    ANNOTATIONS.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def today():
    return date.today().isoformat()


# --- nimien siistiminen ---------------------------------------------------------------

# Pienellä kirjoitettavat sanat (ei rivin/tavuviivan alussa)
SMALL = {
    "de", "del", "della", "delle", "dello", "dei", "degli", "di", "da", "do", "dos", "das", "des", "du", "dels",
    "y", "e", "ed", "et", "en", "of", "the", "and", "for", "in", "per", "por", "para", "als",
    "voor", "van", "der", "het", "und", "für", "fur", "fuer", "von", "vom", "zu", "zur", "am", "im",
    "w", "we", "z", "ze", "v", "na", "za", "din", "im.", "og", "och", "ja", "ir",
}
# "i" on pieni vain norjassa/ruotsissa/tanskassa/islannissa (i Oslo) ja espanjassa (katalaani: Mas i Porcel);
# muualla se on isolla (italialainen roomalainen numero: Corso Umberto I)
I_SMALL_COUNTRIES = {"NO", "SE", "DK", "IS", "ES"}
# Artikkelit: pienellä vain prepositiosanan jälkeen ("de la", "de les"), muuten isolla ("La Spezia")
ARTICLES = {"la", "las", "los", "le", "les", "el", "els"}
ARTICLE_PREPS = {"de", "del", "en", "a", "por"}
ACRONYMS = {"SL": "SL", "SRL": "srl", "ONLUS": "ONLUS", "GMBH": "GmbH", "SNC": "SNC", "KHIO": "KHiO", "LUCA": "LUCA",
            "II": "II", "III": "III", "IV": "IV", "VI": "VI"}
# Apostrofin edellä pienellä (ei sanan alussa): yksiselitteiset italialaiset supistumat
APOS_LOWER = {"dell", "dall", "nell", "all", "sull"}
APOS_LOWER_NON_IT = {"d", "l"}  # d'Art, l'Art; italiassa D'Annunzio, L'Aquila isolla

_RUN = re.compile(r"[^\W\d_]+")


def _is_shouty(s):
    letters = [c for c in s if c.isalpha()]
    return len(letters) >= 3 and (all(c.isupper() for c in letters) or all(c.islower() for c in letters))


def nice_case(s, country=None):
    """Siistii pelkkiä versaaleja (tai pelkkiä pieniä kirjaimia) sisältävän nimen luettavaan muotoon.

    Sekakirjaimiset nimet jätetään ennalleen (vain välilyönnit siistitään). Säilyttää olemassa olevat
    erikoismerkit (ø, ł, é...). Ei pysty palauttamaan diakriitteja, jotka upstreamissa puuttuvat
    (UNIVERSITAT ei tule muotoon Universität).
    """
    if not s:
        return s
    s = re.sub(r"\s+", " ", s.strip())
    if not _is_shouty(s):
        return s
    s = s.replace("İ", "i")
    depth, inside = 0, []
    for c in s:
        depth += c == "("
        inside.append(depth > 0)
        depth -= c == ")"
    out, last, prev_word = [], 0, None
    for m in _RUN.finditer(s):
        w, a, b = m.group(), m.start(), m.end()
        pre = s[last:a]
        prev_ch = s[a - 1] if a else ""
        next_ch = s[b] if b < len(s) else ""
        at_start = prev_word is None or re.search(r"(^|\s)[-:;–—]\s*$", pre + "") is not None and (" " in pre)
        low = w.lower()
        if inside[a]:
            new = w
        elif prev_ch.isdigit() and len(w) <= 2:
            new = w.upper()  # 13B
        elif w.upper() in ACRONYMS:
            new = ACRONYMS[w.upper()]
        elif len(w) == 1 and next_ch == ".":
            new = w.upper()  # A.STEFFANI
        elif prev_ch in ("'", "’"):
            new = low.capitalize()
        elif next_ch in ("'", "’") and b + 1 < len(s) and s[b + 1].isalpha():
            if not at_start and (low in APOS_LOWER or (low in APOS_LOWER_NON_IT and country != "IT")):
                new = low
            else:
                new = low.capitalize()
        elif low in ARTICLES:
            new = low if (not at_start and prev_word in ARTICLE_PREPS and " " in pre) else low.capitalize()
        elif low == "i" and not at_start and country in I_SMALL_COUNTRIES:
            new = "i"
        elif low in SMALL and not at_start:
            new = low
        elif country == "IT" and len(w) == 2 and b == len(s) and prev_ch == " " and prev_word and len(prev_word) >= 4:
            new = w.upper()  # provinssikoodi: San Domenico di Fiesole FI
        elif low == "ij" or (country == "NL" and low.startswith("ij")):
            new = "IJ" + low[2:]
        else:
            new = low.capitalize()
        out.append(pre + new)
        last = b
        prev_word = low
    out.append(s[last:])
    return "".join(out)


_SCHEME = re.compile(r"^[a-z][a-z0-9+.-]*://", re.I)


def normalize_url(w):
    """Lisää https:// jos puuttuu; palauttaa None jos osoitetta ei ole tai se ei näytä osoitteelta.

    Ei arvaa osoitteita: arvo, jossa on välilyöntejä tai ei pistettä, hylätään.
    """
    if not w or not w.strip():
        return None
    w = w.strip()
    if _SCHEME.match(w):
        return w
    if re.search(r"\s", w) or "." not in w:
        return None
    return "https://" + w
