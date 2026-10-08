# Erä 6: Saksa 3/3 (aja: python scripts/programmes/b06.py, sitten python scripts/add_programmes.py data/programmes_batches/06.json). Apufunktio R(alat, tasot, nimi, url, huom) laajentaa rivit.
import json
import os
from auto import A, T
I = {}
def R(code, discs, levels, name, url, note=None):
    for d in discs.split():
        for lv in (levels.split() if levels else [None]):
            I.setdefault(code, []).append([d, lv, name, url] + ([note] if note else []))

# --- laitokset ---

c = "D  LEIPZIG05"; LF = "https://www.hmt-leipzig.de/hochschule/fachrichtungen-institute/"
for d in ["alte-musik", "gesang-musiktheater", "jazz-popularmusik", "kirchenmusik", "klavier-dirigieren", "komposition-tonsatz", "musikpaedagogik", "musikwissenschaft", "streichinstrumente-harfe"]:
    A(I, c, LF + d + "/studieninformationen", r"(bachelor|master)studiengang", drop=r"Doppelfach|Korrepetition|Liedgestaltung|Instrumental-/Gesang|Elementare|Improvisation", quiet=True)
for lv, slug in [("BA", "bachelorstudiengang-blasinstrumente-schlagzeug"), ("MA", "masterstudiengang-blasinstrumente-schlagzeug-konsekutiv-kuenstlerisch")]:
    R(c, "woodwind brass percussion", lv, ("Bachelor" if lv == "BA" else "Master") + " Blasinstrumente | Schlagzeug", LF + "musikpaedagogik/studieninformationen/studiengang-1/" + slug)
R(c, "harp", "BA MA", "Streichinstrumente | Harfe", LF + "streichinstrumente-harfe/studieninformationen/steckbriefe/bachelorstudiengang-streichinstrumente-harfe")
R(c, "music-education", "BA", "Bachelor Instrumental-/Gesangspädagogik, Elementare Musik-/Tanzpädagogik; Doppelfach Schulmusik", LF + "musikpaedagogik")
R(c, "music-education", "MA", "Master Elementare Musik- und Tanzpädagogik; Doppelfach Schulmusik; pädagogisch-künstlerische Master", LF + "musikpaedagogik")
R(c, "composition music-theory", "BA", "Bachelor Komposition | Musiktheorie | Improvisation", LF + "komposition-tonsatz/studieninformationen/steckbriefe/bachelorstudiengang-kompositionmusiktheorieimprovisation")
R(c, "music-technology", "MA", "Master Elektroakustische Musik", LF + "komposition-tonsatz/studieninformationen/steckbriefe/masterstudiengang-elektroakustische-musik-konsekutiv-kuenstlerisch")

c = "D  HAMBURG05"; HH = "https://www.hfmt-hamburg.de/"
R(c, "strings guitar harp woodwind brass percussion piano organ early-music", "BA", "Bachelorstudiengang Instrumentalmusik (Violine … Schlagzeug, Klavier, Orgel, Cembalo, Blockflöte, Traversflöte)", HH + "fileadmin/u/ordnungen/PO_BMus_Instr.pdf")
R(c, "strings guitar harp woodwind brass percussion piano organ", "MA", "Master Instrumentalmusik; Internationaler Master", HH + "studieren/vorlesungsverzeichnis/?tx_hfmtdb_degree%5Bcat%5D=4&tx_hfmtdb_degree%5Baction%5D=list&tx_hfmtdb_degree%5Bcontroller%5D=Degree")
R(c, "jazz", "BA MA", "Jazz (Bachelor, Master)", HH + "musik/studiengaenge/jazz")
R(c, "composition music-technology", "MA", "Multimediale Komposition (Master)", HH + "studieren/vorlesungsverzeichnis/")
R(c, "vocal-opera", "BA MA", "Gesang; Operngesang", HH + "musik/studiengaenge/gesang")
R(c, "conducting", "BA MA", "Dirigieren; Chorleitung", HH + "musik/studiengaenge/dirigieren")
R(c, "church-music", "BA MA", "Kirchenmusik", HH + "musik/studiengaenge/kirchenmusik")
R(c, "music-education", "BA MA", "Instrumentalpädagogik; Lehramt für Sekundarstufe I & II", HH + "en/paedagogik-therapie-wissenschaft/musikpaedagogik/instrumentalpaedagogik")
R(c, "music-therapy", "MA", "Master Musiktherapie", HH + "studieren/vorlesungsverzeichnis/")
R(c, "arts-management", "MA", "Kultur- und Medienmanagement (Fernstudium Master)", HH + "kultur-und-medienmanagement/studiengaenge/fernshystudium-master")

c = "D  ROSTOCK02"; RO = "https://www.hmt-rostock.de/studium/studienangebot/"
A(I, c, RO + "musik/", r"studienangebot/musik/.", drop=r"Konzertexamen|Gesangspädagogik|auslaufend", quiet=True)
R(c, "music-education", "BA MA", "Bachelor / Master of Music | Instrumental- und Gesangspädagogik (alle Hauptfächer)", RO + "musik/")
R(c, "music-education", "BA MA", "Lehramt Musik", RO + "lehramt/")
R(c, "musicology", "BA MA", "Musikwissenschaft", RO + "wissenschaft/")

c = "D  DUSSELD06"; DU = "https://www.rsh-duesseldorf.de/studiengaenge"
A(I, c, DU, r"/studiengaenge/(bachelor|master)/[a-z-]+$", drop=r"Modulplan|Liedgestaltung|Musikfilmregie|orchesterinstrumente|musik-und-medien|klang-und-realitaet|kammermusik|musikproduktion|^Bachelor$|^Master$", quiet=True)
R(c, "strings woodwind brass percussion harp", "BA MA", "Orchesterinstrumente (B.Mus., M.Mus.)", DU + "/bachelor/orchesterinstrumente")
R(c, "chamber-music", "MA", "Bläser-, Klavier- und Streicher-Kammermusik (M.Mus.)", DU + "/master/blaeser-kammermusik")
R(c, "music-technology", "BA", "Musik und Medien (Ton- und Bildingenieur)", DU + "/bachelor/musik-und-medien")
R(c, "music-technology", "MA", "Klang und Realität", DU + "/master/klang-und-realitaet")
R(c, "music-production", "MA", "Künstlerische Musikproduktion", DU + "/master/kuenstlerische-musikproduktion")
c = "D  DRESDEN05"; DD = "https://www.hfmdd.de/studieren/"
for lv in ("BA", "MA"):
    A(I, c, "https://www.hfmdd.de", r"hfmdd\.de/studieren/(blasinstrumente|dirigierenkorrepetition|gesang|gitarre|harfe|jazzrockpop|klavier|komposition|musiktheorie|paukeschlagwerk|streichinstrumente|neue-musik)$", default_level=lv, quiet=True)
R(c, "jazz popular-music", "BA MA", "Jazz/Rock/Pop", DD + "jazzrockpop")
R(c, "music-education", "BA MA", "Künstlerisch-Pädagogische Ausbildung; Lehramt Musik", DD + "kuenstlerisch-paedagogische-ausbildung")

c = "D  HANNOVE04"; HA = "https://www.hmtm-hannover.de/de/bewerbung/studienangebote/"
for discs, lv, name, slug in [
    ("conducting", "BA", "Dirigieren | Chor- und Orchesterleitung (B.Mus.)", "dirigieren-bachelor-of-music/"),
    ("conducting", "MA", "Dirigieren | Chor- und Orchesterleitung; Kinder- und Jugendchorleitung (M.Mus.)", "dirigieren-mmus/"),
    ("vocal-opera", "BA", "Gesang (B.Mus.)", "gesang-b-mus/"),
    ("vocal-opera", "MA", "Gesang/Oper; Gesang in freiberuflicher Tätigkeit (M.Mus.)", "gesangoper-mmus/"),
    ("jazz popular-music", "BA", "Jazz und jazzverwandte Musik (B.Mus.)", "jazz-und-jazzverwandte-musik/"),
    ("jazz popular-music", "MA", "JazzRockPop (M.Mus.)", "jazz-rock-pop-studieren-master-of-music/"),
    ("popular-music", "BA", "Popular Music (B.Mus.)", "popular-music-bmus/"),
    ("chamber-music", "MA", "Kammermusik (M.Mus.)", "kammermusik-mmus/"),
    ("church-music organ", "BA", "Kirchenmusik (B.Mus.)", "kirchenmusik-bachelor-of-music/"),
    ("church-music organ", "MA", "Kirchenmusik (M.Mus.)", "kirchenmusik-mmus/"),
    ("piano", "BA", "Klavier (B.Mus.)", "klavier-bmus/"),
    ("piano organ", "MA", "Tasteninstrumente (M.Mus.)", "tasteninstrumente-mmus/"),
    ("composition", "BA", "Komposition (B.Mus.)", "komposition-bmus/"),
    ("composition", "MA", "Komposition (M.Mus.)", "komposition-mmus/"),
    ("music-education", "BA", "Künstlerisch-pädagogische Ausbildung (B.Mus.); Fächerübergreifender Bachelor (Schulmusik)", "kuenstlerisch-paedagogische-ausbildung-bmus/"),
    ("music-education", "MA", "Künstlerisch-pädagogische Ausbildung (M.Mus.); Lehramt an Gymnasien (M.Ed.)", "kuenstlerisch-paedagogische-ausbildung-mmus/"),
    ("strings woodwind brass percussion accordion early-music", "BA", "Künstlerische Ausbildung / Musical Performance (B.Mus.): alle Orchesterinstrumente, Blockflöte, Akkordeon", "kuenstlerische-ausbildung-bmus/"),
    ("strings woodwind brass percussion accordion", "MA", "Künstlerische Ausbildung (M.Mus.)", "kuenstlerische-ausbildung-mmus/"),
    ("music-theory", "MA", "Musiktheorie (M.Mus.)", "musiktheorie-mmus/"),
    ("musicology music-education", "MA", "Musikwissenschaft und Musikvermittlung (M.A.)", "musikforschung-und-musikvermittlung-ma/"),
    ("arts-management", "MA", "Medien und Musik (M.A.)", "medien-und-musik-ma/")]:
    R(c, discs, lv, name, HA + slug)

c = "D  STUTTGA03"; ST = "https://www.hmdk-stuttgart.de/studiengang/"
for discs, lv, name, slug in [
    ("strings harp", "BA", "Bachelor Musik – Streichinstrumente, Harfe", "bachelor-musik-streichinstrumente-harfe"),
    ("woodwind brass", "BA", "Bachelor Musik – Blasinstrumente", "bachelor-musik-blasinstrumente"),
    ("organ", "BA", "Bachelor Musik – Orgel", "bachelor-musik-orgel"), ("organ", "MA", "Master Orgel", "master-musik-orgel"),
    ("guitar", "BA", "Bachelor Musik – Gitarre", "bachelor-musik-gitarre"), ("guitar early-music", "MA", "Master Gitarre, Gitarrenduo, historische Saiteninstrumente", "master-musik-gitarre"),
    ("composition", "BA", "Bachelor Musik – Komposition (Instrumentalkomposition, Computermusik)", "bachelor-musik-komposition"), ("composition", "MA", "Master Komposition", "master-musik-komposition"),
    ("music-technology", "BA", "Bachelor Musik – Komposition: Computermusik", "bachelor-musik-komposition"),
    ("conducting", "BA", "Bachelor Musik – Chordirigieren; Orchesterdirigieren", "bachelor-musik-chordirigieren"),
    ("piano", "BA", "Bachelor Musik – Klavier", "bachelor-musik-klavier"),
    ("vocal-opera", "BA", "Bachelor Musik – Gesang", "bachelor-musik-gesang"), ("vocal-opera", "MA", "Master Oper", "master-oper"),
    ("percussion", "BA", "Bachelor Musik – Schlagzeug", "bachelor-musik-schlagzeug"),
    ("accordion", "BA", "Bachelor Musik – Akkordeon", "bachelor-musik-akkordeon"),
    ("jazz popular-music", "BA", "Bachelor Musik – Jazz & Pop", "bachelor-musik-jazz-pop"),
    ("music-education", "BA", "Bachelor Musik – Elementare Musikpädagogik; Bachelor Lehramt", "bachelor-musik-elementare-musikpaedagogik"),
    ("music-education", "MA", "Master Instrumental- & Gesangspädagogik; Master Lehramt", "master-instrumental-gesangspaedagogik"),
    ("music-theory", "BA", "Bachelor Musik – Musiktheorie", "bachelor-musik-musiktheorie"), ("music-theory", "MA", "Master Musiktheorie", "master-musik-musiktheorie"),
    ("church-music", "BA", "Bachelor Kirchenmusik B", "bachelor-kirchenmusik-b"), ("church-music", "MA", "Master Kirchenmusik A", "master-kirchenmusik"),
    ("chamber-music", "MA", "Master Kammermusik", "master-kammermusik"),
    ("musicology", "MA", "Master Musikwissenschaft", "master-musikwissenschaft")]:
    R(c, discs, lv, name, ST + slug)

c = "D  MUNSTER01"; MS = "https://www.uni-muenster.de/Musikhochschule/Studieninteressierte/Bewerbung.html"
R(c, "vocal-opera", "BA MA", "Bachelor / Master of Music – Instrument / Gesang (klassische Ausbildung)", MS)
R(c, "popular-music", "BA", "Bachelor of Music – Popularmusik (Pop-Vocals, Drum-Set, E-Bass, E-Gitarre)", MS)
R(c, "music-production", "BA", "Bachelor of Music – Popularmusik / Keyboards & Music Production", MS)
R(c, "music-education", "BA", "Bachelor of Music – Musik und Vermittlung; Elementare Musikpädagogik", MS)
R(c, "music-education", "MA", "Master of Music – Musikpädagogik", MS)
R(c, "composition", "BA MA", "Bachelor / Master of Music – Musik und Kreativität", MS)

METHOD = "Field-level collection as in batch 1 (raw HTML of each institution's own programme pages, PDFs where the list was only there; names mapped to disciplines.json by keyword and checked by hand)."
NOTES = {}

# ErÃ¤tiedosto add_programmes.py:lle
BATCH = {"collected": "2026-10-08", "method": METHOD, "institutions": I, "notes": NOTES}
out = os.path.join(os.path.dirname(__file__), "..", "..", "data", "programmes_batches", "06.json")
json.dump(BATCH, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print({k: len(v) for k, v in I.items()})
