# Erä 8: Italia 2 (aja: python scripts/programmes/b08.py, sitten python scripts/add_programmes.py data/programmes_batches/08.json). Apufunktio R(alat, tasot, nimi, url, huom) laajentaa rivit.
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
    ("I  VENEZIA04", "https://www.conservatoriovenezia.eu/triennio-di-primo-livello/", "https://www.conservatoriovenezia.eu/biennio-di-secondo-livello/"),
    ("I  MATERA01", "https://www.conservatoriomatera.it/didattica/offerta-formativa/", None),
    ("I  TRENTO02", "https://conservatorio.tn.it/triennio/", "https://conservatorio.tn.it/biennio/"),
    ("I  VIBO-VA01", "https://consvv.it/corsi-accademici-di-primo-livello", "https://consvv.it/corsi-accademici-di-secondo-livello"),
    ("I  POTENZA03", "https://www.conservatoriopotenza.it/corsi/", None),
    ("I  FROSINO02", "https://www.conservatorio-frosinone.it/didattica/corsi-afam/piani-di-studio-diplomi-accademici-trienni-in-vigore-dallaa-20202021.html", "https://www.conservatorio-frosinone.it/didattica/corsi-afam/piani-di-studio-bienni-ordinamentali-da-aa202122.html"),
    ("I  MANTOVA01", "https://www.conservatoriomantova.com/it//corsi_accademici_di_i_livello", None),
    ("I  LUCCA03", "https://www.boccherini.it/corsi/corsi-accademici-i-livello/", "https://www.boccherini.it/corsi/corsi-accademici-ii-livello/"),
    ("I  FIRENZE04", "https://www.consfi.it/corsi/", None),
    ("I  BARI03", "https://www.consba.it/it/7/offerta-formativa", None),
    ("I  MONOPOL02", "https://conservatoriodimonopoli.org/offerta-formativa/", None),
    ("I  ROMA09", "https://conservatoriosantacecilia.it/triennio-piani-di-studio-e-ammissione/", "https://conservatoriosantacecilia.it/biennio-piani-di-studio-e-ammissione/"),
]
for code, ba, ma in IT_PAGES:
    if ma: IT(I, code, ba, "BA"); IT(I, code, ma, "MA")
    else: IT(I, code, ba, None)

METHOD = "Field-level collection as in batch 1; where a site lists programmes only via JavaScript, the programme pages were located with a web search restricted to the institution's own domain (raw HTML of each institution's own programme pages, PDFs where the list was only there; names mapped to disciplines.json by keyword and checked by hand)."
NOTES = {}

# ErÃ¤tiedosto add_programmes.py:lle
BATCH = {"collected": "2026-10-08", "method": METHOD, "institutions": I, "notes": NOTES}
out = os.path.join(os.path.dirname(__file__), "..", "..", "data", "programmes_batches", "08.json")
json.dump(BATCH, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print({k: len(v) for k, v in I.items()})
