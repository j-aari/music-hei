# Erä 15: odottaneet (Saksa, Italia, Alicante) (aja: python scripts/programmes/b15.py, sitten python scripts/add_programmes.py data/programmes_batches/15.json). Apufunktio R(alat, tasot, nimi, url, huom) laajentaa rivit.
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
]
for code, ba, ma in IT_PAGES:
    if ma: IT(I, code, ba, "BA"); IT(I, code, ma, "MA")
    else: IT(I, code, ba, None)

CL = "strings woodwind brass percussion piano vocal-opera"; CLN = "Classical music programme; the page does not list the instruments, which are recorded as the usual orchestral instruments, piano and voice"

PI = "strings woodwind brass percussion piano organ guitar harp accordion"

for code, url, lv in [("I  AOSTA03", "https://www.consaosta.it/corsi-accademici-primo-livello-triennio/", "BA"), ("I  AOSTA03", "https://www.consaosta.it/corsi-accademici-di-secondo-livello-biennio/", "MA"),
                      ("I  TERAMO02", "https://www.conservatoriobraga.it/contents.asp?id=522", "BA"), ("I  TERAMO02", "https://www.conservatoriobraga.it/contents.asp?id=511", "MA"),
                      ("I  CUNEO01", "https://www.conservatoriocuneo.it/corsi-accademici-di-i-livello-programmi/", "BA"), ("I  CUNEO01", "https://www.conservatoriocuneo.it/corsi-accademici-di-ii-livello-programmi/", "MA"),
                      ("I  SIENA05", "https://www.sienajazz.it/university/corsi-accademici-di-i-livello/", "BA"), ("I  SIENA05", "https://www.sienajazz.it/university/corsi-accademici-di-ii-livello/", "MA")]:
    IT(I, code, url, lv)
I["I  CUNEO01"] = [r for r in I["I  CUNEO01"] if r[2].isupper()]  # sivulla myös oppiaineiden ohjelmat; ohjelmanimet versaalilla
A(I, "I  FIRENZE07", "https://www.scuolamusicafiesole.it", r"corsi-accademici-(primo|secondo)-livello", quiet=True)
A(I, "I  MILANO24", "https://www.cpm.it", r"cpm\.it/corsi/.*(triennio|biennio|canto-classico|canto-pop-rock)", quiet=True)
R("I  MILANO24", "popular-music", "BA MA", "Corsi accademici pop/rock (CPM Music Institute)", "https://www.cpm.it/corsi/basso-elettrico-pop-rock-triennio/")

c = "D  MUNCHEN03"; MU = "https://website.hmtm.de/de/studium/studienangebot/studiengaenge"
R(c, PI + " vocal-opera", "BA MA", "Studiengänge: Akkordeon, Blasinstrumente, Gesang, Gitarre, Harfe, Klavier, Orgel, Pauke-Schlagzeug, Streichinstrumente", MU)
R(c, "early-music", "BA MA", "Blockflöte, Cembalo, Historische Aufführungspraxis", MU)
R(c, "folk", "BA", "Volksmusik; Hackbrett; Zither", "https://hmtm.de/en/courses/folk-music-bm-ps/")
R(c, "jazz", "BA MA", "Jazz (Bachelor, Master); Jazz Education (Master)", "https://hmtm.de/en/courses/jazz-bm-en/")
R(c, "conducting", "BA MA", "Chordirigieren", MU)
R(c, "music-education", "BA MA", "Elementare Musikpädagogik; Instrumental- und Gesangspädagogik; Musikvermittlung (Master)", "https://hmtm.de/en/courses/music-mediation-ma/")
R(c, "composition", "MA", "Contemporary Music (Master)", MU)
c = "D  BERLIN03"; UK = "https://www.udk-berlin.de/universitaet/fakultaet-musik/studium/kuenstlerische-ausbildung-1/"
R(c, "strings woodwind brass percussion harp guitar piano conducting composition church-music music-technology", "BA MA", "Künstlerische Studiengänge: Orchesterinstrumente (incl. Gitarre, Saxophon, Blockflöte), Klavier, Dirigieren, Komposition, Kirchenmusik, Tonmeister", UK)
R(c, "early-music", "BA MA", "Alte Musik (u. a. Cembalo, Laute)", UK)
R(c, "jazz", "BA MA", "Jazz-Institut Berlin: Bachelor Jazz; Master Jazz Arrangement/Composition", UK)
R(c, "vocal-opera", "BA MA", "Gesang / Musiktheater", "https://www.udk-berlin.de/en/courses/voiceopera/")
R(c, "music-education music-theory conducting", "BA MA", "Künstlerisch-Pädagogische Ausbildung (Musiktheorie, Chor-/Ensembleleitung, EMP); Lehramt Musik", "https://www.udk-berlin.de/studium/kuenstlerisch-paedagogische-ausbildung/studium/master/")
c = "D  LUBECK02"; LB = "https://www.mh-luebeck.de/studium/studiengaenge/"
R(c, "woodwind brass percussion strings harp guitar piano organ vocal-opera composition music-theory church-music", "BA MA", "Musikpraxis (Bachelor/Master of Music): Blasinstrumente, Schlagzeug, Streichinstrumente, Harfe, Gitarre, Tasteninstrumente, Orgel, Gesang, Komposition, Musiktheorie, Kirchenmusik", LB + "master-of-music/")
R(c, "chamber-music", "MA", "Master of Music – Kammermusik", LB + "master-of-music/")
R(c, "music-education", "BA MA", "Instrumentale und Elementare Musikpädagogik; Musik Vermitteln (B.A.); Master of Education; IGP", LB + "bachelor-of-music-instrumentale-und-elementare-musikpaedagogik/")
c = "D  BREMEN03"; BR = "https://altemusik.hfk-bremen.de/en/courses-of-study/"
R(c, "early-music", "BA MA", "Alte Musik (B.Mus., M.Mus.)", BR)
R(c, "church-music", "MA", "Master historische Kirchenmusik", BR)
R(c, "music-education music-theory", "BA MA", "Künstlerisch-Pädagogische Ausbildung (IGP, EMP, Musiktheorie)", "https://www.hfk-bremen.de/de/kuenstlerisch-paedagogische-ausbildung-kpa")
c = "D  SAARBRU08"; SA = "http://www.hfm.saarland.de/en/studies/study-offer/"
R(c, PI + " vocal-opera", "BA MA", "Bachelor / Master Instrument; Tasteninstrumente und Gitarre; Gesang", SA + "bachelor-studiengaenge/")
R(c, "jazz popular-music", "BA MA", "Jazz und aktuelle Musik (B.Mus.); Master of Music Jazz", SA + "master-programmes/")
R(c, "church-music", "BA MA", "Kirchenmusik", SA + "master-programmes/")
R(c, "chamber-music composition conducting music-theory arts-management", "MA", "Master: Kammermusik, Komposition, Dirigieren, Musiktheorie, Kulturmanagement", SA + "master-programmes/")
R(c, "music-education", "BA MA", "Lehramt Musik", SA + "bachelor-studiengaenge/")
c = "D  MAINZ01"; MZ = "https://www.musik.uni-mainz.de/studium/studienangebot/"
R(c, "jazz popular-music", "BA MA", "Jazz und Populäre Musik (B.Mus., M.Mus.)", MZ + "jazz-pop-musik-b-mus/")
R(c, "strings woodwind brass percussion harp guitar piano", "BA MA", "Orchesterinstrumente (incl. Gitarre); Klavier", MZ)
R(c, "church-music organ", "BA MA", "Kirchenmusik (B.Mus., M.Mus.)", MZ)
R(c, "music-education", "BA", "Elementare Musikpädagogik (B.Mus.)", MZ + "emp-b-mus/")

c = "D  FRANKFU02"; FR = "https://www.hfmdk-frankfurt.de/studiengang/"
R(c, "strings woodwind brass percussion piano guitar organ conducting", "BA MA", "Künstlerische Ausbildung Musik (KAM): Orchesterinstrumente, Klavier/Gitarre, Orgel, Dirigieren", FR + "kuenstlerische-ausbildung-musik-kam-bachelor")
R(c, "early-music", "BA MA", "Künstlerische Ausbildung Musik (KAM): Historische Instrumente", FR + "kuenstlerische-ausbildung-musik-kam-bachelor")
R(c, "music-education", "BA MA", "Instrumentalpädagogik", "https://www.hfmdk-frankfurt.de/thema/instrumentalpaedagogik")
R(c, "jazz composition conducting", "MA", "Master Bigband (Instrumentalists, Composers and Conductors)", "https://www.hfmdk-frankfurt.de/en/studiengang/bigband-instrumentalists-composers-and-conductors-master")
c = "D  OSNABRU02"; OS = "https://www.hs-osnabrueck.de/studium/studienangebot/bachelor/"
R(c, "popular-music music-education", "BA", "Musikerziehung (B.A.) – Pop", OS + "musikerziehung-ba-pop/")
R(c, "jazz", "BA", "Musikerziehung (B.A.) – Jazz", OS + "musikerziehung-ba-jazz/")
R(c, "vocal-opera music-education", "BA", "Musikerziehung (B.A.) – Musical", OS + "musikerziehung-ba-musical/")
R(c, CL + " composition music-theory", "BA", "Musikerziehung (B.A.) – Klassik (Instrument, Gesang, Komposition, Musiktheorie)", "https://www.hs-osnabrueck.de/wir/fakultaeten/ifm/klassik/", CLN)

METHOD = "Field-level collection as in batch 1; where a site lists programmes only via JavaScript, the programme pages were located with a web search restricted to the institution's own domain (raw HTML of each institution's own programme pages, PDFs where the list was only there; names mapped to disciplines.json by keyword and checked by hand)."
NOTES = {}

# ErÃ¤tiedosto add_programmes.py:lle
BATCH = {"collected": "2026-10-08", "method": METHOD, "institutions": I, "notes": NOTES}
out = os.path.join(os.path.dirname(__file__), "..", "..", "data", "programmes_batches", "15.json")
json.dump(BATCH, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print({k: len(v) for k, v in I.items()})
