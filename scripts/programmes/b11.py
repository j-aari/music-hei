# Erä 11: Baltia, Luxemburg, Montenegro, Alankomaat (aja: python scripts/programmes/b11.py, sitten python scripts/add_programmes.py data/programmes_batches/11.json). Apufunktio R(alat, tasot, nimi, url, huom) laajentaa rivit.
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

for lv in ("BA", "MA"):
    A(I, "LV RIGA05", "https://www.jvlma.lv", r"studijas/studiju-nozares/", drop=r"Horeogr", default_level=lv, quiet=True)
    A(I, "LT VILNIUS05", "https://old.lmta.lt/en/fakultetas/muzikos-fakultetas/", r"muzikos-fakultetas/.+katedra|klaipedos-fakultetas/muzikos-katedra", drop=r"Accompaniment|Dance|Acting|Theatre|History|Staff|Events|Competition|ensemble|Orchestra|Dėstytojai|Opera Studio", default_level=lv, quiet=True)
R("LT VILNIUS05", "woodwind brass percussion", "BA MA", "Department of Wind and Percussion Instruments", "https://old.lmta.lt/en/fakultetas/muzikos-fakultetas/")
R("LT VILNIUS05", "vocal-opera", "MA", "Opera Studio", "https://old.lmta.lt/en/fakultetas/muzikos-fakultetas/")
R("LV RIGA05", "strings woodwind brass piano organ percussion guitar harp accordion", "BA MA", "Instrumentālā mūzika", "https://www.jvlma.lv/studijas/studiju-nozares/instrumentala-muzika")

c = "LT KAUNAS01"; VD = "https://ma.vdu.lt/studijos/studiju-programos"
R(c, "accordion piano vocal-opera conducting strings guitar harp", "BA MA", "Atlikimo menas: akordeonas, fortepijonas, dainavimas, dirigavimas, styginiai instrumentai (gitara, altas, arfa, kontrabosas, smuikas, violončelė)", VD)
R(c, "early-music", "BA MA", "Atlikimo menas (styginiai instrumentai – autentiškas muzikos atlikimas)", VD)
R(c, "jazz", "BA MA", "Atlikimo menas (džiazas)", VD)
R(c, "popular-music", "BA MA", "Atlikimo menas (populiarioji muzika)", VD)
R(c, "woodwind brass percussion", "BA MA", "Atlikimo menas (pučiamieji ir mušamieji instrumentai)", VD)
R(c, "chamber-music", "MA", "Atlikimo menas (kamerinis)", VD)
R(c, "music-production", "BA", "Music Production (Faculty of Arts)", "https://www.vdu.lt/en/studiju-programa/music-production-2/")
R(c, "music-education", "BA MA", "Mokomojo dalyko pedagogika: muzikos pedagogika; Muzikos edukologija", "https://www.vdu.lt/lt/studiju-programa/muzikos-edukologija/")
c = "LT VILNIUS10"
R(c, "popular-music", "BA", "Populiarioji muzika (also in English), professional bachelor", "https://www.viko.lt/vilniaus-kolegijos-menu-ir-kurybiniu-technologiju-fakulteto-stojamieji-egzaminai/")
R(c, "vocal-opera", "BA", "Muzikinis teatras (professional bachelor)", "https://www.viko.lt/studentams/studiju-programos-lietuviskai/muzikinis-teatras/")
c = "LUXLUX-VIL01"
R(c, "music-education", "BA", "Bachelor en Enseignement musical (instrumental/vocal teaching, formation musicale, éveil musical)", "https://www.uni.lu/fhse-en/study-programs/bachelor-en-enseignement-musical/")
c = "ME PODGORI02"; UC = "https://ucg.ac.me/skladiste/blog_616703/objava_198608/fajlovi/UCG%20studijski%20programi%202025-26%20_interaktiv_.pdf"
R(c, "music-education", "BA MA", "Opšta muzička pedagogija", UC)
R(c, "composition", "MA", "Kompozicija (magistarske studije)", UC)

CL = "strings woodwind brass percussion piano vocal-opera"; CLN = "Classical music programme; the page does not list the instruments, which are recorded as the usual orchestral instruments, piano and voice"
c = "NL UTRECHT29"; HK = "https://www.hku.nl/studeren-aan-hku/"
A(I, c, "https://www.hku.nl/opleidingen", r"studeren-aan-hku/(utrechts-conservatorium|muziek-en-technologie)/.", drop=r"Basisopleiding|Minor|Pre-master|Cursus|Klassieke|Musician 3", quiet=True)
R(c, CL + " guitar harp organ", "BA", "Bachelor Klassieke Muziek (Utrechts Conservatorium)", HK + "utrechts-conservatorium/klassieke-muziek", CLN)
R(c, CL, "MA", "Master of Music – Performance", HK + "utrechts-conservatorium/master-of-music", CLN)
R(c, "organ", "BA", "De Nederlandse Beiaardschool (carillon)", HK + "utrechts-conservatorium/de-nederlandse-beiaardschool")
c = "NL ENSCHED04"; AZ = "https://www.artez.nl/opleidingen/"
R(c, "music-education", "BA", "Bachelor Docent Muziek (Enschede, Zwolle)", AZ + "bachelor/docent-muziek-zwolle")
R(c, "jazz popular-music", "BA", "Bachelor Jazz & Pop (Arnhem, Zwolle)", AZ + "bachelor/jazz-pop-arnhem")
R(c, "popular-music", "BA", "Bachelor Popacademie (Enschede)", AZ + "bachelor/popacademie-enschede")
R(c, CL, "BA", "Bachelor Klassieke Muziek (Zwolle)", AZ + "bachelor/klassieke-muziek-zwolle", CLN)
R(c, "composition music-production", "BA", "Bachelor MediaMusic (Enschede)", AZ + "bachelor/mediamusic-enschede")
R(c, "music-therapy", "BA MA", "Muziektherapie (Bachelor, Master)", AZ + "bachelor/muziektherapie-enschede")
R(c, CL + " jazz popular-music", "MA", "Master of Music (Arnhem, Zwolle)", AZ + "master/master-of-music-zwolle", CLN)

c = "NL AMSTERD07"; CV = "https://www.conservatoriumvanamsterdam.nl/studie/"
R(c, CL, "BA MA", "Klassiek", CV + "klassiek/", CLN)
R(c, "jazz", "BA MA", "Jazz", CV + "jazz/")
R(c, "popular-music", "BA", "Pop", CV + "pop/")
R(c, "early-music", "BA MA", "Oude muziek", CV + "oude-muziek/")
R(c, "music-education", "BA", "Docent muziek", CV + "docent-muziek/")
R(c, "music-production music-technology", "BA", "Amsterdam Electronic Music Academy", CV + "aema/")
R(c, "music-technology", "MA", "Focus master Immersive Audio", CV + "focus-masters/immersive-audio/")
c = "NL EINDHOV03"; FO = "https://www.fontys.nl/en/Programmes/Conservatory-of-Music-bachelor-full-time.htm"
R(c, CL, "BA", "Conservatory of Music – Classical", FO, CLN)
R(c, "jazz", "BA", "Conservatory of Music – Jazz & Creative Music", FO)
c = "NL S-GRAVE37"; IH = "https://www.inholland.nl/opleidingen/muziek-voltijd/"
R(c, "popular-music", "BA", "Muziek – richtingen Pop, Creative Artist, E-music", IH)
R(c, "music-production", "BA", "Muziek – richting E-music; Associate degree Electronic Music", IH + "de-opleiding/")
c = "NL HEERLEN14"; CM = "https://www.conservatoriummaastricht.nl/study-here/"
R(c, CL, "BA MA", "Bachelor / Master of Music – Classical (25 main subjects)", CM + "classical/master", CLN)
R(c, "jazz", "BA MA", "Bachelor / Master of Music – Jazz", "https://www.zuyd.nl/en/programmes/music")
R(c, "music-education", "BA", "Bachelor Music in Education (Docent Muziek)", CM + "music-education/bachelor")
R(c, "conducting composition chamber-music", "MA", "Master of Music – Classical: conducting, composition, chamber music", CM + "classical/master")
c = "NL GRONING03"; PC = "https://www.hanze.nl/eng/education/art/prince-claus-conservatoire/programmes/"
R(c, CL, "BA", "Bachelor Classical Music", PC + "bachelor/classical-music", CLN)
R(c, CL, "MA", "Master of Music – Classical Music", PC + "master-of-music/classical-music", CLN)
R(c, "jazz", "BA MA", "Jazz (Bachelor); Master of Music – Jazz", PC + "bachelor/jazz")
R(c, "music-education", "MA", "Master of Music – New Audiences and Innovative Practice", "https://catalogue.hanze.nl/en/Programme/2022/ECTSMUVNAIP20")

METHOD = "Field-level collection as in batch 1; where a site lists programmes only via JavaScript, the programme pages were located with a web search restricted to the institution's own domain (raw HTML of each institution's own programme pages, PDFs where the list was only there; names mapped to disciplines.json by keyword and checked by hand)."
NOTES = {}

# ErÃ¤tiedosto add_programmes.py:lle
BATCH = {"collected": "2026-10-08", "method": METHOD, "institutions": I, "notes": NOTES}
out = os.path.join(os.path.dirname(__file__), "..", "..", "data", "programmes_batches", "11.json")
json.dump(BATCH, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print({k: len(v) for k, v in I.items()})
