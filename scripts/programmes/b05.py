# Erä 5: Saksa 2/2 (aja: python scripts/programmes/b05.py, sitten python scripts/add_programmes.py data/programmes_batches/05.json). Apufunktio R(alat, tasot, nimi, url, huom) laajentaa rivit.
import json
import os
from auto import A, T
I = {}
def R(code, discs, levels, name, url, note=None):
    for d in discs.split():
        for lv in (levels.split() if levels else [None]):
            I.setdefault(code, []).append([d, lv, name, url] + ([note] if note else []))

# --- laitokset ---

c = "D  WURZBUR02"; WU = "https://www.hfm-wuerzburg.de/studiengaenge"
for lv in ("BA", "MA"):
    A(I, c, WU, r"studiengaenge/.", drop=r"Musik an |EMP|Inkl\.|Vok\.|Zertifikat|PreCollege|Promotion|Meisterklasse|Überblick|Übersicht|korrepetition|Liedgestaltung|Kammermusik|Performance and Pedagogy|Tasteninstrumente|Doppelrohr|Konzertgesang|Operngesang|Blasorchester|Kirchenmusik", default_level=lv, quiet=True)
R(c, "chamber-music", "MA", "Kammermusik", WU)
R(c, "church-music organ", "BA MA", "Kirchenmusik (ev./kath.)", WU)
R(c, "conducting", "BA MA", "Blasorchesterleitung; Chorleitung; Orchesterleitung", WU)
R(c, "music-education", "BA MA", "Elementare Musikpädagogik (EMP); Inklusive Musikpädagogik / Community Music; Musik an Grundschulen, Mittelschulen, Realschulen, Gymnasien; Master of Music in Performance and Pedagogy", WU)
c = "D  TROSSIN01"; TR = "https://www.mh-trossingen.de/"
R(c, "accordion guitar piano organ strings woodwind brass percussion vocal-opera", "BA MA", "Bachelor / Master Podium und Orchester (Akkordeon, Gitarre, Klavier, Orgel, Streicher, Bläser, Schlagzeug, Gesang)", TR + "studium/uebersicht-studienangebote")
R(c, "early-music", "BA MA", "Alte Musik", TR + "studium/uebersicht-studienangebote")
R(c, "composition", "BA MA", "Komposition", TR + "studium/uebersicht-studienangebote")
R(c, "music-education", "BA MA", "Bachelor / Master Musik-Pädagogik; Gymnasiallehramt; Rhythmik mit EMP", TR + "studium/bachelor-musikpaedagogik")
R(c, "music-production music-technology", "BA", "Bachelor Musikdesign", TR + "bachelor-musikdesign")
R(c, "music-technology", "MA", "Master Audio Experience Design", TR + "master-audio-experience-design")
R(c, "chamber-music", "MA", "Master Kammermusik einschl. Lied(-gestaltung)", TR + "studium/uebersicht-studienangebote")

c = "D  MANNHEI02"; MH = "https://www.muho-mannheim.de/studienangebote/"
R(c, "conducting piano harp strings woodwind brass percussion vocal-opera composition", "BA", "Bachelor Musik (künstlerischer Schwerpunkt): Dirigieren, Klavier, Harfe, Streicher, Bläser, Schlagzeug, Gesang, Komposition", MH + "bachelor-musik/bachelor-musik-kuenstlerischer-schwerpunkt/")
R(c, "music-education", "BA", "Bachelor Musik (künstlerisch-pädagogischer Schwerpunkt); Bachelor Lehramt Musik an Gymnasien", MH + "bachelor-musik/")
R(c, "musicology", "BA", "Bachelor Musik (Schwerpunkt Musikforschung / Medienpraxis)", MH + "bachelor-musik/")
R(c, "jazz popular-music", "BA MA", "Bachelor / Master of Music (Jazz / Popularmusik)", MH)
R(c, "music-education", "MA", "Master Lehramt Musik an Gymnasien", MH)
R(c, "vocal-opera", "MA", "Opernstudio", MH)

c = "D  MANNHEI09"; PO = "https://www.popakademie.de/de/studium/"
R(c, "popular-music", "BA", "Popmusikdesign (B.A.)", PO + "popmusikdesign-ba/")
R(c, "popular-music", "MA", "Popular Music (M.A.)", PO + "popular-music-ma/")
R(c, "global-music", "BA", "Weltmusik / Global Music (B.A.)", PO + "globalmusic-ba/")
R(c, "arts-management", "BA", "Musikbusiness (B.A.)", PO + "musikbusiness-ba/")
R(c, "arts-management", "MA", "Music and Creative Industries (M.A.)", PO + "music-and-creative-industries-ma/")

METHOD = "Field-level collection as in batch 1 (raw HTML of each institution's own programme pages, PDFs where the list was only there; names mapped to disciplines.json by keyword and checked by hand)."
NOTES = {}

# ErÃ¤tiedosto add_programmes.py:lle
BATCH = {"collected": "2026-10-08", "method": METHOD, "institutions": I, "notes": NOTES}
out = os.path.join(os.path.dirname(__file__), "..", "..", "data", "programmes_batches", "05.json")
json.dump(BATCH, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print({k: len(v) for k, v in I.items()})
