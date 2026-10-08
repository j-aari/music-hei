# Erä 4: Saksa 1/2 (aja: python scripts/programmes/b04.py, sitten python scripts/add_programmes.py data/programmes_batches/04.json). Apufunktio R(alat, tasot, nimi, url, huom) laajentaa rivit.
import json
import os
from auto import A, T
I = {}
def R(code, discs, levels, name, url, note=None):
    for d in discs.split():
        for lv in (levels.split() if levels else [None]):
            I.setdefault(code, []).append([d, lv, name, url] + ([note] if note else []))

# --- laitokset ---

c = "D  HALLE04"; EH = "https://www.ehk-halle.de/studiengaenge"
R(c, "church-music organ", "BA MA", "Bachelorstudium Kirchenmusik; Masterstudium Kirchenmusik", EH)
R(c, "music-education", "BA", "Kombistudium Bachelor Kirchenmusik / Lehramt Musik an Gymnasien", EH)
R(c, "conducting", "MA", "Masterstudium Chor- und Orchesterleitung", EH)
R(c, "popular-music", "MA", "Masterstudium Kirchliche Popularmusik", EH)
R(c, "vocal-opera", "MA", "Masterstudium Konzert- und Oratoriengesang", EH)
R(c, "organ", "MA", "Masterstudium Künstlerisches Orgelspiel", EH)
c = "D  REGENSB03"; RG = "https://www.hfkm-regensburg.de/studium/"
for lst in ("bachelor-studiengaenge/", "master-studiengaenge/"):
    A(I, c, RG + lst, r"studium/(bachelor|master)-studiengaenge/.", quiet=True)
R(c, "church-music", "BA MA", "Katholische Kirchenmusik", RG + "bachelor-studiengaenge/katholische-kirchenmusik/")
R(c, "music-education", "BA MA", "Musikpädagogik (künstlerisches Kernfach); Schulmusik/Lehramt Gymnasium", RG + "bachelor-studiengaenge/")
R(c, "composition", "MA", "Kirchliche Komposition", RG + "master-studiengaenge/kirchliche-komposition/")
R(c, "popular-music", "MA", "Neue Geistliche Musik", RG + "master-studiengaenge/neue-geistliche-musik/")
c = "D  BERLIN16"; HE = "https://www.hfm-berlin.de/studium/studienfaecher/"
for lv in ("BA", "MA"):
    A(I, c, HE, r"studium/studienfaecher/.", drop=r"regie|dramaturgie|korrepetition|tonsatz|kammermusik", default_level=lv, quiet=True)
R(c, "music-theory", "BA MA", "Historischer und Zeitgenössischer Tonsatz", HE + "historischer-und-zeitgenoessischer-tonsatz/")
R(c, "chamber-music", "MA", "Kammermusik", HE + "kammermusik/")

c = "D  ESSEN02"; FW = "https://www.folkwang-uni.de/home/musik/studiengaenge/"
R(c, "accordion guitar piano organ harp strings woodwind brass percussion", "BA", "Instrumentalausbildung – Bachelor of Music", FW + "instrumentalausbildung-bmus/basisinfos-bewerbung")
R(c, "accordion guitar piano organ harp strings woodwind brass percussion", "MA", "Instrumentalausbildung – Master of Music; Instrumentale Spezialisierung; Orchesterspiel", FW + "instrumentalausbildung-mmus-2")
R(c, "early-music", "BA MA", "Instrumentalausbildung: Barockvioline, -viola, -cello, Blockflöte, Cembalo, historische Tasteninstrumente, Traversflöte; Musik des Mittelalters (M.Mus.)", FW + "instrumentalausbildung-bmus/basisinfos-bewerbung")
R(c, "composition", "BA MA", "Integrative Komposition (B.Mus., M.Mus.)", FW + "integrative-komposition-bmus")
R(c, "jazz", "BA MA", "Jazz | Performing Artist (B.Mus.); Jazz | Improvising Artist; Jazz | Artistic Producer", FW + "jazz-performing-artist")
R(c, "popular-music", "MA", "Populäre Musik (M.Mus.)", FW + "populaere-musik")
R(c, "music-production", "MA", "Professional Media Creation – Master of Arts", FW + "professional-media-creation")
R(c, "conducting", "MA", "Leitung vokaler Ensembles", FW + "leitung-vokaler-ensembles")
R(c, "vocal-opera", "BA MA", "Gesang | Musiktheater (B.Mus., M.Mus.)", "https://www.folkwang-uni.de/home/theater/studiengaenge/gesang-musiktheater-bmus")
R(c, "music-education", "MA", "Singen mit Kindern und Jugendlichen", FW + "singen-mit-kindern-und-jugendlichen")

c = "D  KARLSRU03"; KA = "https://www.hfm-karlsruhe.de/studieren/faecher-und-instrumente"
for lv in ("BA", "MA"):
    A(I, c, KA, r"faecher-und-instrumente/.", drop=r"kammermusik|regie|journalismus|liedgestaltung|zeitgenössische", default_level=lv, quiet=True)
R(c, "chamber-music", "MA", "Bläser-, Harfe-, Klavier-, Streicher- und Ensemble-Kammermusik", KA)
R(c, "music-education", "BA", "Künstlerisches Lehramt an Gymnasien (Schulmusik); BA Musikpädagogik", "https://www.hfm-karlsruhe.de/studieren/studienangebote/kuenstlerisches-lehramt-gymnasien")

c = "D  DETMOLD01"; DT = "https://www.hfm-detmold.de/studium"
for lv in ("BA", "MA"):
    A(I, c, DT, r"studienbereiche(-und-bewerbung)?/[a-z]", drop=r"jungstudierend|gesundheit|orchesterinstrumente|management|akustik|\.p", default_level=lv, quiet=True)
R(c, "strings woodwind brass percussion harp", "BA MA", "Orchesterinstrumente", DT + "/studienbereiche-und-bewerbung/orchesterinstrumente/")
R(c, "music-technology", "BA MA", "Musikübertragung/Tonmeister, Musikregie; Musikalische Akustik", DT + "/studienbereiche-und-bewerbung/musikuebertragung/tonmeister-musikregie/")
R(c, "guitar accordion woodwind", "BA MA", "Gitarre | Akkordeon | Saxophon | Blockflöte", DT + "/studienbereiche-und-bewerbung/gitarre-akkordeon-saxophon/")
R(c, "arts-management", "MA", "Musikmanagement", DT + "/studienbereiche-und-bewerbung/musikmanagement/")

c = "D  WEIMAR02"; WM = "https://www.hfm-weimar.de/bewerben/studienfinder"
for lv in ("BA", "MA"):
    A(I, c, WM, r"studienfinder/detail/", drop=r"korrepetition|liedgestaltung|musikpraxis|kammermusik|management", default_level=lv, quiet=True)
R(c, "chamber-music", "MA", "Kammermusik", WM + "/detail/kammermusik")
R(c, "arts-management", "BA MA", "Kulturmanagement; Interkulturelles Musik- und Veranstaltungsmanagement", WM + "/detail/kulturmanagement")
R(c, "jazz", "BA MA", "Elektrische Gitarre; Improvisierter Gesang (Jazz)", WM + "/detail/elektrische-gitarre")
c = "D  TUBINGE02"; TU = "https://www.kirchenmusikhochschule.de/studieren/"
R(c, "church-music organ", "BA MA", "Ev. Kirchenmusik (Bachelor B, Master A); KA-Aufbaustudiengang Orgel", TU)
R(c, "popular-music", "BA MA", "Ev. Popular-Kirchenmusik; Kirchliche Popularmusik", TU)

c = "D  KOLN03"; KO = "https://www.hfmt-koeln.de/musik/studiengaenge/"
for n in range(1, 8):
    A(I, c, KO + ("" if n == 1 else f"?tx_solr%5Bpage%5D={n}"), r"/studiengaenge/(bachelor|master)[^/]*/.",
      drop=r"Elementare|Instrumental- /|Gender|Mandoline|Opernkorrep|Orchesterspiel|Interpretation Neue", quiet=True)
R(c, "strings woodwind brass guitar piano", "MA", "Master of Music: Streichinstrumente, Blasinstrumente, Gitarre, Klavier", KO + "master-of-music/blasinstrumente-master-of-music/")
R(c, "music-education", "BA", "Elementare Musikpädagogik; Instrumental- / Gesangspädagogik (Bachelor of Music)", KO)
R(c, "global-music", "BA", "Instrumental- / Gesangspädagogik und EMP: Bağlama", KO)

c = "D  FREIBUR03"; FR = "https://www.mh-freiburg.de/studium/studienangebot/"
for lv in ("BA", "MA"):
    A(I, c, FR + "faecher", r"studienangebot/faecher/.", drop=r"Korrepetition|Liedgestaltung|Musikphysiologie|Interpretation|improvisation|Ensemblegesang|Advanced", default_level=lv, quiet=True)
R(c, "church-music", "BA", "Bachelor Kirchenmusik", FR + "bachelor-kirchenmusik")
R(c, "music-technology", "BA MA", "Elektronische Komposition", FR + "faecher/elektronische-komposition")
R(c, "vocal-opera", "MA", "Freiburger Opernstudio", FR + "freiburger-opernstudio")
R(c, "music-education", "BA MA", "Musikpädagogik (alle Instrumente); Lehramt Musik", FR + "faecher")

c = "D  NURNBER04"; NU = "https://www.hfm-nuernberg.de/studium/studienangebot"
for n in range(1, 10):
    T(I, c, NU + ("" if n == 1 else f"?tx_kesearch_pi1%5Bpage%5D={n}"), r"^(BA|MA) ", drop=r"Elementare|Korrepetition|Liedgestaltung|heterogenen|Interdisciplinary|Musikpädagogik", quiet=True)
R(c, "music-education", "BA", "BA Elementare Musikpädagogik (KPA); künstlerisch-pädagogische Bachelorstudiengänge (KPA)", NU)
R(c, "music-education", "MA", "MA Musikpädagogik: Elementare Musikpädagogik / Instrument/Gesang KPA; MA Musizieren in heterogenen Gruppen", NU)

METHOD = "Field-level collection as in batch 1 (raw HTML of each institution's own programme pages, PDFs where the list was only there; names mapped to disciplines.json by keyword and checked by hand)."
NOTES = {}

# ErÃ¤tiedosto add_programmes.py:lle
BATCH = {"collected": "2026-10-08", "method": METHOD, "institutions": I, "notes": NOTES}
out = os.path.join(os.path.dirname(__file__), "..", "..", "data", "programmes_batches", "04.json")
json.dump(BATCH, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print({k: len(v) for k, v in I.items()})
