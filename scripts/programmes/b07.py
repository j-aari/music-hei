# Erä 7: Kreikka – Irlanti, Italia alkaa (aja: python scripts/programmes/b07.py, sitten python scripts/add_programmes.py data/programmes_batches/07.json). Apufunktio R(alat, tasot, nimi, url, huom) laajentaa rivit.
import json
import os
from auto import A, T, IT
I = {}
def R(code, discs, levels, name, url, note=None):
    for d in discs.split():
        for lv in (levels.split() if levels else [None]):
            I.setdefault(code, []).append([d, lv, name, url] + ([note] if note else []))

# --- laitokset ---

c = "IRLDUBLIN22"; RI = "https://www.riam.ie/"
R(c, "woodwind brass percussion", "BA", "BMus Performance – Woodwind, Brass & Percussion faculty", RI + "sites/default/files/media/file-uploads/2024-09/BMus%20WBP%20Handbook%202024-2025.pdf")
R(c, "composition", "BA", "Bachelor in Music Composition", RI + "sites/default/files/media/file-uploads/2025-09/BMus%20Composition%20Handbook%202025-2026.pdf")
R(c, "piano strings vocal-opera woodwind brass percussion", "MA", "MMus in Music Performance – Keyboard, Strings, Vocal Studies, Woodwind, Brass & Percussion", RI + "degrees-programmes/full-time/mmusperf")
R(c, "music-education", "BA", "Bachelor in Music Education (with TU Dublin and Trinity College Dublin)", "https://www.tudublin.ie/explore/faculties-and-schools/arts-humanities/schools/conservatoire/study-with-us/undergraduate/bachelor-in-music-education---tu964-tr009/")
c = "IRLDUBLIN44"; TU = "https://www.tudublin.ie/explore/faculties-and-schools/arts-humanities/schools/conservatoire/study-with-us/"
R(c, "composition musicology", "BA", "Bachelor of Music (TU963): performance, composition, musicology", TU + "undergraduate/bachelor-of-music---tu963/")
R(c, "music-education", "BA", "Bachelor in Music Education (TU964/TR009)", TU + "undergraduate/bachelor-in-music-education---tu964-tr009/")
R(c, "jazz", "MA", "Master of Music in Jazz Performance", TU + "departments/jazz/")
R(c, "composition", "MA", "MMus in Composition", TU + "music/programmes-courses/")
c = "IRLMUNST01"; CS = "https://csm.mtu.ie/"
R(c, "early-music conducting composition", "BA", "Bachelor of Music (performance; aural, conducting, composition, early music performance)", CS + "bmus-bachelor-of-music")
R(c, "popular-music", "BA", "BA (Hons) in Popular Music (electric guitar, bass, keyboard, drums, voice)", CS + "bapm")
R(c, "music-technology", "MA", "Taught MA/MSc in Music and Technology", CS + "music-and-technology")
R(c, "conducting composition jazz popular-music folk", "MA", "Taught MA in Music (Performance, Conducting or Composition; classical, jazz, popular and Irish traditional strands)", CS + "masters-in-music-_ma")
c = "IS REYKJAV06"; LH = "https://www.lhi.is/"
R(c, "music-education", "BA", "Instrumental / Vocal Education (B.Mus.Ed)", LH + "en/instrumental-vocal-education")
R(c, "composition", "BA MA", "Composition (BA); Music Composition MA/M.Mus", LH + "namsleid/tonsmidar-ma/")
R(c, "music-education", "MA", "MMus for New Audiences and Innovative Practice (NAIP)", LH + "namsleid/mmus-for-new-audiences-and-innovative-practice-naip/")
R(c, "music-technology", "BA", "Music, Innovation and Technology (B.Mus)", LH + "en/music-department/")

c = "HU BUDAPES25"; LZ = "https://uni.lisztacademy.hu/admission-requirements"
R(c, "strings woodwind brass percussion piano organ accordion guitar harp", "BA MA", "BA / MA: violin, viola, cello, double bass, flute, oboe, clarinet, bassoon, saxophone, horn, trumpet, trombone, tuba, percussion, piano, organ, accordion, guitar, harp", LZ)
R(c, "folk", "BA MA", "BA / MA cimbalom", LZ)
R(c, "early-music", "BA MA", "BA / MA harpsichord; MA baroque flute, baroque violin, baroque oboe, fortepiano", LZ)
R(c, "vocal-opera", "BA MA", "BA classical singing; MA oratorio & lied singing; MA opera singing", LZ)
R(c, "composition", "BA MA", "BA composition; BA composing for theatre and motion picture; MA composition", LZ)
R(c, "music-technology", "BA", "BA electronic music media", LZ)
R(c, "conducting", "BA MA", "BA / MA choir conducting; BA / MA orchestral conducting", LZ)
R(c, "jazz", None, "Jazz main subjects: bass guitar, double bass, drums, guitar, piano, saxophone, trumpet, trombone, voice", LZ, "Jazz Department; the page lists the main subjects but not the degree levels")
R(c, "musicology music-theory music-education church-music folk", None, "Musicology, Music Theory, Teacher Education, Church Music and Folk Music departments", "https://uni.lisztacademy.hu/departments", "Departments listed; degree levels not stated on the pages read")
c = "HU GYOR01"; SZ = "https://muk.sze.hu/"
R(c, "strings percussion vocal-opera", "BA", "Előadó-művészet BA (klasszikus szakirányok, pl. gordonka, ütőhangszerek, ének)", SZ + "kovetelmenyek-ba")
R(c, "music-education", "MA", "Osztatlan zenetanár; Tanári (zeneművész-tanár, zenetanár) MA", SZ + "kovetelmenyek-ma")
R(c, "conducting", "MA", "Karmester MA", "https://felveteli.sze.hu/karmester-ma")
c = "G  THESSAL02"; UM = "https://www.uom.gr/en/"
R(c, "music-education early-music folk", "MA", "Master in Musical Arts: Didactics of Musical Instruments; Early Music and modal musical traditions of the Mediterranean", UM + "musart")
R(c, "composition conducting chamber-music", "MA", "Master in Musical Arts: Music Performance / Music Creation (incl. chamber music, composition, ensemble conducting)", UM + "musart")
R(c, "musicology", "MA", "Master in Music Science and Arts; Master in Music & Society", UM + "postgraduate")

# Italia: triennio (BA) ja biennio (MA) -sivut, IT() poimii lyhyet rivit ja linkkitekstit
for code, ba, ma in [
    ("I  ADRIA01", "https://conservatorioadria.it/offerta-formativa/diploma-accademico-di-1-livello/", "https://conservatorioadria.it/offerta-formativa/diploma-accademico-di-2-livello-biennio/"),
    ("I  COMO04", "https://conservatoriocomo.it/corsi-accademici-di-primo-livello/", "https://conservatoriocomo.it/corsi-accademici-di-secondo-livello/"),
    ("I  PARMA02", "http://aule.conservatorio.pr.it/cgi-scripts/ordinamenti.exe?azione=corsi&idordinamento=1&idannoaccademico=5&ordinamento=Triennio%20ord.%20/%20Bachelor", "http://aule.conservatorio.pr.it/cgi-scripts/ordinamenti.exe?azione=corsi&idordinamento=3&idannoaccademico=5&ordinamento=Biennio%20/%20Master%20degree%20"),
    ("I  MESSINA04", "https://www.consme.it/index.php?option=com_content&view=article&id=3557&Itemid=178", "https://www.consme.it/index.php?option=com_content&view=article&id=300&Itemid=549"),
    ("I  AGRIGEN02", "https://www.conservatoriotoscanini.it/corsi-afam/", None),
    ("I  ALESSAN01", "https://www.conservatoriovivaldi.it/corsi-accademici-tutte-le-scuole/", None)]:
    if ma: IT(I, code, ba, "BA"); IT(I, code, ma, "MA")
    else: IT(I, code, ba, None)

METHOD = "Field-level collection as in batch 1; where a site lists programmes only via JavaScript, the programme pages were located with a web search restricted to the institution's own domain (raw HTML of each institution's own programme pages, PDFs where the list was only there; names mapped to disciplines.json by keyword and checked by hand)."
NOTES = {}  # L'Aquila (consaq.it) ja Vicenza (consvi.it): ohjelmalista ei näy ilman selainta, odottaa

# ErÃ¤tiedosto add_programmes.py:lle
BATCH = {"collected": "2026-10-08", "method": METHOD, "institutions": I, "notes": NOTES}
out = os.path.join(os.path.dirname(__file__), "..", "..", "data", "programmes_batches", "07.json")
json.dump(BATCH, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print({k: len(v) for k, v in I.items()})
