# Erä 9: Italia 3 (aja: python scripts/programmes/b09.py, sitten python scripts/add_programmes.py data/programmes_batches/09.json). Apufunktio R(alat, tasot, nimi, url, huom) laajentaa rivit.
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
    ("I  CREMONA01", "https://www.conscremona.it/trienni/", "https://www.conscremona.it/bienni/"),
    ("I  LATINA02", "https://www.conslatina.it/cms.php?cat=6&sub=27", None),
    ("I  LECCE03", "https://www.conservatoriolecce.it/struttura/diploma-accademico-di-i-livello-triennio/", None),
    ("I  MODENA05", "https://www.vecchitonelli.it/triennio-ordinamento-di-i-livello/", "https://www.vecchitonelli.it/biennio-ordinamento-di-ii-livello/"),
    ("I  PERUGIA03", "https://www.conservatorioperugia.it/corsi-di-i-livello/", "https://www.conservatorioperugia.it/corsi-di-ii-livello/"),
]
# Linkkilistat, joissa taso on linkin nimessä tai osoitteessa
A(I, "I  BOLOGNA04", "https://www.consbo.it", r"consbo\.it/insegnamenti/.+-(triennio|biennio)/", quiet=True)
A(I, "I  ROVIGO01", "https://www.conservatoriorovigo.it", r"conservatoriorovigo\.it/insegnamenti/.+-(triennio|biennio)/", quiet=True)
A(I, "I  TRAPANI02", "https://www.constp.it", r"constp\.it/\?indirizzo=", quiet=True)
for code, ba, ma in IT_PAGES:
    if ma: IT(I, code, ba, "BA"); IT(I, code, ma, "MA")
    else: IT(I, code, ba, None)

METHOD = "Field-level collection as in batch 1; where a site lists programmes only via JavaScript, the programme pages were located with a web search restricted to the institution's own domain (raw HTML of each institution's own programme pages, PDFs where the list was only there; names mapped to disciplines.json by keyword and checked by hand)."
NOTES = {}

# ErÃ¤tiedosto add_programmes.py:lle
BATCH = {"collected": "2026-10-08", "method": METHOD, "institutions": I, "notes": NOTES}
out = os.path.join(os.path.dirname(__file__), "..", "..", "data", "programmes_batches", "09.json")
json.dump(BATCH, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print({k: len(v) for k, v in I.items()})
