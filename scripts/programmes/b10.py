# Erä 10: Italia 4 (aja: python scripts/programmes/b10.py, sitten python scripts/add_programmes.py data/programmes_batches/10.json). Apufunktio R(alat, tasot, nimi, url, huom) laajentaa rivit.
import json
import os
from auto import A, T, IT
I = {}
def R(code, discs, levels, name, url, note=None):
    for d in discs.split():
        for lv in (levels.split() if levels else [None]):
            I.setdefault(code, []).append([d, lv, name, url] + ([note] if note else []))

# --- laitokset ---
IT_PAGES = [
    ("I  NAPOLI07", "https://www.sanpietroamajella.it/triennio-di-primo-livello/", "https://www.sanpietroamajella.it/biennio-sperimentale/"),
    ("I  UDINE02", "https://www.conservatorio.udine.it/didattica/triennio.html", "https://www.conservatorio.udine.it/didattica/biennio.html"),
    ("I  SASSARI02", "https://www.conservatorio.sassari.it/ScuolaCorsi/DetailTipoCorso?post_name=2&culture=it-IT", "https://www.conservatorio.sassari.it/ScuolaCorsi/DetailTipoCorso?post_name=3&culture=it-IT"),
    ("I  AVELLIN01", "https://conservatoriocimarosa.org/didattica", None),
    ("I  NOVARA01", "https://consno.it/offerta-didattica/corsi/", None),
]
for code, ba, ma in IT_PAGES:
    if ma: IT(I, code, ba, "BA"); IT(I, code, ma, "MA")
    else: IT(I, code, ba, None)

METHOD = "Field-level collection as in batch 1; where a site lists programmes only via JavaScript, the programme pages were located with a web search restricted to the institution's own domain (raw HTML of each institution's own programme pages, PDFs where the list was only there; names mapped to disciplines.json by keyword and checked by hand)."
NOTES = {}

# ErÃ¤tiedosto add_programmes.py:lle
BATCH = {"collected": "2026-10-08", "method": METHOD, "institutions": I, "notes": NOTES}
out = os.path.join(os.path.dirname(__file__), "..", "..", "data", "programmes_batches", "10.json")
json.dump(BATCH, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print({k: len(v) for k, v in I.items()})
