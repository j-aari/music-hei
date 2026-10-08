# Erä 1: Itävalta + Belgia (aja: python scripts/programmes/b01.py, sitten python scripts/add_programmes.py data/programmes_batches/01.json). Apufunktio R(alat, tasot, nimi, url, huom) laajentaa rivit.
import json
import os
from auto import A, T
I = {}
def R(code, discs, levels, name, url, note=None):
    for d in discs.split():
        for lv in (levels.split() if levels else [None]):
            I.setdefault(code, []).append([d, lv, name, url] + ([note] if note else []))

c = "A  LINZ17"; B = "https://www.bruckneruni.ac.at/de/studieren/studienangebot/studien/"
R(c, "early-music", "BA MA", "Alte Musik und Historische Aufführungspraxis – KBA / KMA", B + "alte-musik")
R(c, "brass percussion", "BA MA", "Blechblasinstrumente und Schlagwerk – KBA / KMA", B + "blechblasinstrumente-und-schlagwerk")
R(c, "vocal-opera", "BA MA", "Gesang und Musiktheater – KBA / KMA", B + "gesang")
R(c, "woodwind", "BA MA", "Holzblasinstrumente – KBA / KMA", B + "holzblasinstrumente")
R(c, "conducting", "BA", "Künstlerisches Bachelorstudium Dirigieren", B + "komposition-dirigieren")
R(c, "composition", "BA MA", "Künstlerisches Bachelor-/Masterstudium Komposition", B + "komposition-dirigieren")
R(c, "jazz", "BA MA", "Jazz und Improvisierte Musik – KBA / KMA", B + "jazz-und-improvisierte-musik")
R(c, "music-education", "BA MA", "Elementare Musikpädagogik; Lehramt Musik Sekundarstufe (BEd/MEd)", B + "musik/musikpaedagogik")
R(c, "strings guitar harp", "BA MA", "Saiteninstrumente – KBA / KMA", B + "saiteninstrumente")
R(c, "piano accordion organ", "BA MA", "Tasteninstrumente – KBA / KMA", B + "tasteninstrumente")

c = "A  WIEN77"; G = "https://gulda-school-of-music.com/academics/"
DN = "State-recognised diploma programme (Diplomstudium, 8 semesters), not a BA/MA degree"
for d, slug, nm in [("jazz popular-music", "jazz-popular-music/gitarre-kuenstlerisches-hauptfach", "Jazz & Popular Music (all instruments, voice, ensemble leading)"),
                    ("piano", "klassik/klavier-kuenstlerisches-hauptfach", "Klassik – Klavier"), ("accordion", "klassik/akkordeon-kuenstlerisches-hauptfach", "Klassik – Akkordeon"),
                    ("organ", "klassik/orgel-kuenstlerisches-hauptfach", "Klassik – Orgel"), ("guitar", "klassik/gitarre-kuenstlerisches-hauptfach", "Klassik – Gitarre"),
                    ("harp", "klassik/harfe-kuenstlerisches-hauptfach", "Klassik – Harfe"), ("strings", "klassik/violine-kuenstlerisches-hauptfach", "Klassik – Violine, Viola, Violoncello, Kontrabass"),
                    ("woodwind", "klassik/floete-kuenstlerisches-hauptfach", "Klassik – Blockflöte, Flöte, Oboe, Klarinette, Fagott, Saxophon"),
                    ("brass", "klassik/trompete-kuenstlerisches-hauptfach", "Klassik – Horn, Trompete, Posaune, Tuba"), ("percussion", "klassik/schlaginstrumente-kuenstlerisches-hauptfach", "Klassik – Schlaginstrumente"),
                    ("vocal-opera", "klassik/gesang-kuenstlerisches-hauptfach", "Klassik – Gesang"), ("conducting", "all-programs", "Klassik – Dirigieren & Ensembleleitung"),
                    ("composition music-theory", "all-programs", "Komposition, Arrangement und Musiktheorie"), ("music-education", "all-programs", "Instrumental(Gesangs)pädagogik (IGP), all majors")]:
    R(c, d, None, nm, G + "all-programs", DN)

c = "A  WIEN76"; J = "https://www.jammusiclab.com/academics/"
JZ = "JAM MUSIC LAB is a university for jazz and popular music"
R(c, "jazz popular-music", "BA MA", "Bachelor / Master of Arts in Music (jazz and popular music)", J + "all-programs", JZ)
R(c, "piano accordion guitar strings harp woodwind brass percussion vocal-opera", "BA MA", "Bachelor / Master of Arts in Music – instrumental and vocal majors (jazz/pop)", J + "all-programs")
R(c, "composition music-theory", "BA MA", "Bachelor / Master of Arts in Music – Composition and Music Theory", J + "all-programs")
R(c, "music-production", "BA MA", "Media Music: Film Scoring and Music Production", J + "bachelor-arts-music/media-music")
R(c, "music-education", "BA MA", "Bachelor / Master of Arts in Music Education", J + "bachelor-arts-music-education")
R(c, "arts-management", "BA", "Bachelor of Arts – Arts Management", J + "bachelor-arts/arts-management")

c = "A  KLAGENF06"; K = "https://www.gmpu.ac.at/"
R(c, "piano accordion guitar organ strings harp woodwind brass percussion vocal-opera", "BA MA", "Musikalische Aufführungskunst (Klassik, Jazz) – central artistic subjects", K + "files/zkF_BA-MAK.pdf")
R(c, "jazz", "BA MA", "Musikalische Aufführungskunst – Studienrichtung Jazz", K + "studium/ba-mak")
R(c, "conducting composition", "BA MA", "Musikalische Aufführungskunst – Dirigieren, Komposition", K + "files/zkF_MA-MAK.pdf")
R(c, "chamber-music", "MA", "Musikalische Aufführungskunst (Master) – Kammermusik", K + "files/zkF_MA-MAK.pdf")
R(c, "music-education", "BA MA", "Instrumental- und Gesangspädagogik (Bachelor / Master)", K + "studium/ba-igp")
R(c, "popular-music", "BA", "IGP Popmusik (Bachelor)", K + "universitaet/institute/imp/fachbereiche/pop")
R(c, "folk", "BA MA", "Studienrichtung Volksmusik (IGP Bachelor and Master)", K + "universitaet/institute/imp/fachbereiche/vm")

c = "A  EISENST05"; H = "https://www.jhp.ac.at/"
HC = H + "fileadmin-jhp/user_upload/1.3._Curriculum_BAK_Kuenstlerische_Kompetenzen_01.10.2026.pdf"
R(c, "strings woodwind brass guitar piano organ percussion vocal-opera composition", "BA", "Bachelor Künstlerisch (BAK) – instrument-specific curricula", HC)
R(c, "strings woodwind brass guitar piano organ percussion vocal-opera composition", "MA", "Master Künstlerisch (MAK)", H + "studium/studienangebot/masterstudien/")
R(c, "jazz popular-music", "BA MA", "Jazz & Popularmusik im Rahmen der BA- und MA-Studien (E-Gitarre, E-Bass, Klavier, Saxophon, Schlagzeug)", H + "studium/studienangebot/studium-jazz-popularmusik/")
R(c, "music-education", "BA MA", "Bachelor / Master Künstlerisch-Pädagogisch (BAP / MAP)", H + "studium/studienangebot/bachelorstudien/")

c = "A  WIEN52"; M = "https://www.muk.ac.at/bewerbung/studien-termine/"
MA = M + "alle-studien-an-der-muk.html"
R(c, "piano accordion guitar harp strings woodwind brass percussion", "BA MA", "Instrumentalstudien (Bachelor- und Masterstudium)", M + "instrumentalstudien/klavier.html")
R(c, "early-music", "BA MA", "Instrumentalstudien Alte Musik (Cembalo, Fortepiano, historische Instrumente, Laute, Viola da gamba); Gesang (Alte Musik)", MA)
R(c, "jazz", "BA MA", "Jazz-Bass, -Gitarre, -Klavier, -Posaune, -Saxophon, -Schlagzeug, -Trompete, -Gesang; Jazz-Komposition & Arrangement", M + "instrumentalstudien/jazz-gitarre.html")
R(c, "vocal-opera", "BA MA", "Sologesang; Oper; Lied und Oratorium", MA)
R(c, "conducting", "BA MA", "Dirigieren (Bachelor- und Masterstudium)", M + "kuenstlerische-studien/dirigieren.html")
R(c, "composition", "BA MA", "Komposition", MA)
R(c, "organ", "BA", "Orgel (IGP)", MA)
R(c, "music-education", "BA", "Instrumental- und Gesangspädagogische Studien (Bachelorstudium IGP)", M + "instrumentalstudien/klavier.html")
R(c, "music-education", "MA", "Master of Arts Education (MAE)", MA)

c = "A  FELDKIR03"; S = "https://stella-musikhochschule.ac.at/"
R(c, "piano accordion guitar harp organ strings woodwind brass percussion vocal-opera", "BA", "BA Music Performance – artistic main subjects (admission requirements)", S + "wp-content/uploads/2025/02/Anforderungen-Zulassungspruefung-ZKF-BA-MP_Stand-Februar-2024.pdf")
R(c, "piano accordion guitar harp organ strings woodwind brass percussion vocal-opera", "MA", "MA Music Performance & Career Development", S + "studium/master/music-performance-career-development")
R(c, "music-education", "BA", "BA Music Education & Music Performance", S + "studium/bachelor/music-education-music-performance")
R(c, "music-education", "MA", "MA Music Education & Music Performance", S + "studium/master/ma-music-education-music-performance")

A(I, "A  GRAZ03", "https://www.kug.ac.at/studium/studienangebot/studienfinder", r"studienangebot/studienrichtungen/", drop=r"Kunst und Gestaltung|Technik und Design|Bühnengestaltung|Darstellende Kunst|Doktorat")

c = "A  WIEN74"; V = "https://www.vmi.at/"; VN = "Conservatory programme (180–240 ECTS); the page does not name a BA/MA degree"
R(c, "popular-music", None, "Konzertfach (performance in modern music); Songwriting", V + "konzertfach", VN)
R(c, "composition", None, "Komposition; Medienkomposition", V + "komposition", VN)
R(c, "music-education", None, "IGP – Instrumental- und Gesangspädagogik; Kompositionspädagogik", V + "igp-instrumental-und-gesangspaedagogik", VN)
R(c, "music-technology", None, "Elektronische Musik und Sound Design", V + "elektronische-musik-und-sound-design-studiengang", VN)
R(c, "music-production", None, "Music Production", V + "music-production", VN)
R(c, "arts-management", None, "Music Business", V + "music-business", VN)

c = "B  BRUSSEL43"; L = "https://www.luca-arts.be/nl/"
R(c, "accordion guitar harp organ piano percussion vocal-opera strings brass", "BA MA", "Instrument/Zang (campus Leuven Lemmens)", L + "instrumentzang-master")
R(c, "folk", "BA MA", "Instrument/Zang – Nyckelharpa", L + "instrumentzang-master")
R(c, "composition", "BA MA", "Compositie", L + "compositie-campus-leuven-lemmens-bachelor")
R(c, "conducting", "BA MA", "Directie (incl. koordirectie)", L + "directie-campus-leuven-lemmens-bachelor")
R(c, "jazz", "BA MA", "Jazz", L + "jazz-campus-leuven-lemmens-bachelor")
R(c, "music-education", "BA", "Muziekpedagogie", L + "muziekpedagogie-campus-leuven-lemmens-bachelor")
R(c, "music-education", "MA", "Educatieve Master in muziek en podiumkunsten", L + "educatieve-master-in-muziek-en-podiumkunsten")
R(c, "music-therapy", "BA MA", "Muziektherapie", L + "muziektherapie-campus-leuven-lemmens-bachelor")

c = "B  MONS24"; M = "https://www.artsaucarre.be/musique-conservatoire-royal/sections/"
for lv in ("BA", "MA"):
    A(I, c, "https://www.artsaucarre.be", r"musique-conservatoire-royal/sections/.+/.+/", drop=r"piano-accompagnement|/sections/[a-z-]+/$|cordes/$|vents/$|claviers/$", default_level=lv, quiet=True)
R(c, "early-music", "BA MA", "Guitare romantique", M + "formation-instrumentale/cordes/guitare-romantique/")
R(c, "composition", "BA MA", "Composition", M + "composition/")
R(c, "composition music-technology", "BA MA", "Composition acousmatique; Musiques appliquées et interactives (sound design, prise de son)", M + "musiques-appliquees/")
R(c, "conducting", "BA MA", "Direction d’orchestre", M + "ecritures-et-theorie-musicale/direction-dorchestre/")
R(c, "music-theory", "BA MA", "Écritures classiques", M + "ecritures-et-theorie-musicale/ecritures-classiques/")
R(c, "music-education", "MA", "Masters en enseignement", "https://www.artsaucarre.be/masters-en-enseignement/")

c = "B  BRUXEL07"; E = "https://www.conservatoire.be/etudes/"; FN = "Bachelier and Master (Fédération Wallonie-Bruxelles conservatoire)"
R(c, "strings guitar harp woodwind brass percussion piano organ vocal-opera composition conducting", "BA MA", "Musique classique et contemporaine (cordes, vents, percussions, claviers, chant, composition, direction)", E + "musique-classique-et-contemporaine/")
R(c, "jazz", "BA MA", "Jazz", E + "jazz/")
R(c, "early-music", "BA MA", "Musique ancienne", E + "musique-ancienne/")
R(c, "music-education", "BA", "Bachelier en Rythmes et Rythmiques (BaRR)", E + "rythmes-et-rythmiques/")
R(c, "music-education", "MA", "Master en enseignement – Musique (Formation musicale; Instrument)", E + "pedagogie/")

c = "B  LIEGE03"; H = "https://horizon.student-crlg.be/programmes/2026-2027"
T(I, c, H, r"^26-27 - (Bachelier en musique|Master en musique) :", drop=r"tradition orale|mandoline|viole d|accompagnement|deuxième instrument|orchestre\)|musique de chambre\)|orchestration|composition mixte", quiet=True)
R(c, "jazz", "BA", "Bachelier en musique : musique improvisée de tradition orale", H)
R(c, "chamber-music", "MA", "Master en musique, à finalité spécialisée (Musique de chambre)", H)
R(c, "early-music", "MA", "Master en musique : chant, à finalité spécialisée (Musique ancienne)", H)
R(c, "music-education", "BA", "Bachelier en enseignement section 3 : musique et éducation culturelle et artistique", H)
R(c, "music-education", "MA", "Master en enseignement Section 4 / Section 5 : Musique", H)

c = "B  NAMUR13"; N = "https://www.imep.be/"
R(c, "piano accordion guitar organ strings woodwind brass percussion vocal-opera", "BA MA", "Formation instrumentale / Chant classique (études par cycles, sections, options)", N + "etudes/")
R(c, "popular-music", "BA MA", "Musique pop (Instruments pop, Claviers pop, Guitare électrique, Chant pop)", N + "departement-musique-pop/")
R(c, "early-music", "BA MA", "Musique Ancienne (clavier, cordes, vents, flûte à bec, violon/violoncelle baroque)", N + "departement-de-musique-ancienne/")
R(c, "conducting", "BA MA", "Direction chorale", N + "etudes/")
R(c, "music-theory music-technology", "BA MA", "Écritures & informatique musicale", N + "section-ecriture-et-theorie-musicale/")
R(c, "music-education", "BA MA", "Musique & Transmission (section pédagogique)", N + "section-pedagogique/")

c = "B  ANTWERP62"; P = "https://www.ap-arts.be/opleiding/"; PN = "Koninklijk Conservatorium Antwerpen; Bachelor and Master in Muziek"
R(c, "piano organ", "BA MA", "Muziek – Toetsinstrumenten (piano, orgel)", P + "toetsinstrumenten", PN)
R(c, "early-music", "BA MA", "Muziek – Toetsinstrumenten (klavecimbel)", P + "toetsinstrumenten")
R(c, "chamber-music", "MA", "Piano – kamermuziek en begeleiding", P + "toetsinstrumenten")
R(c, "guitar harp", "BA MA", "Muziek – Tokkelinstrumenten (gitaar, harp)", P + "tokkelinstrumenten")
R(c, "strings", "BA MA", "Muziek – Strijkinstrumenten", P + "strijkinstrumenten")
R(c, "woodwind", "BA MA", "Muziek – Houtblazers", P + "houtblazers")
R(c, "brass", "BA MA", "Muziek – Koperblazers", P + "koperblazers")
R(c, "percussion", "BA MA", "Muziek – Percussie", P + "percussie")
R(c, "vocal-opera", "BA MA", "Muziek – Zang", P + "zang")
R(c, "jazz", "BA MA", "Muziek – Jazz (instrument/zang)", P + "opleiding-jazz")
R(c, "composition", "BA MA", "Muziek – Compositie", P + "compositie")
R(c, "conducting", "MA", "Directie (master)", P + "directie")
R(c, "music-technology", "MA", "Live Electronics (master)", P + "live-electronics")
R(c, "music-education", "BA", "Educatieve bachelor Leraar Muziek", P + "educatieve-bachelor-leraar-muziek")
R(c, "music-education", "MA", "Educatieve master Muziek", P + "educatieve-master-muziek")

c = "B  BRUSSEL46"; K = "https://www.kcb.be/nl/Opleidingen/Muziek"; KN = "Koninklijk Conservatorium Brussel (Erasmushogeschool Brussel)"
R(c, "piano harp guitar vocal-opera", "BA MA", "Bachelor en master Muziek – Polyfone instrumenten & zang", K + "/Polyfone-Instrumenten-en-Zang", KN)
R(c, "strings woodwind brass percussion", "BA MA", "Bachelor en master Muziek – Orkestinstrumenten", K + "/Orkestinstrumenten")
R(c, "early-music", "BA MA", "Bachelor en master Muziek – Historische instrumenten", K + "/Historische-Instrumenten")
R(c, "jazz", "BA MA", "Bachelor en master Muziek – Jazz", "https://www.kcb.be/Opleidingen/Muziek/Jazz-Lichte-Muziek")
R(c, "composition conducting music-theory", "BA MA", "Compositie, Directie & Muziekschriftuur", "https://www.kcb.be/Opleidingen/Muziek/Compositie-Directie-Muziektheorie-schriftuur")
R(c, "music-education", "MA", "Educatieve Master Muziek en Podiumkunsten", "https://www.kcb.be/nl/opleidingen/educatieve-master-muziek-en-podiumkunsten")

c = "B  GENT25"; G = "https://schoolofartsgent.be/studeren/opleidingen/"
R(c, "strings woodwind brass harp percussion piano organ guitar vocal-opera", "BA MA", "Bachelor + master muziek – Klassieke muziek", G + "klassieke-muziek")
R(c, "jazz popular-music", "BA MA", "Bachelor + master muziek – Jazz & pop", G + "jazz-pop")
R(c, "composition", "BA MA", "Bachelor + master muziek – Compositie", G + "compositie")
R(c, "composition", "MA", "Compositie Media & Video Games; International Master in Composition for Screen", G + "compositie-media-video-games")
R(c, "music-theory", "MA", "Master muziek – Muziektheorie/schriftuur", G + "muziektheorie-schriftuur")
R(c, "music-production", "BA MA", "Bachelor + master muziek – Muziekproductie", G + "muziekproductie")
R(c, "music-education", "MA", "Educatieve master", G + "educatieve-master")

METHOD = "Field-level collection (one row per discipline and level, evidence = the programme name and page that shows it). Read each institution's own programme listing as raw HTML (stdlib urllib, no LLM summarisation), following department pages and, where the listing was only in a PDF (GMPU, JHP, Stella), the official curriculum or admission-requirement PDF. Programme names were mapped to disciplines.json with a keyword list and checked by hand; jazz/pop/early-music instrument programmes are recorded under the style, not under each instrument. Doctoral programmes that do not name a field are not recorded. Gulda (Diplomstudium) and VMI (conservatory programmes) are recorded without a level, with a note."
NOTES = {'B  GENT40': 'The Orpheus Institute offers only doctoral study (docARTES) and research residencies, not degree programmes in named fields.'}

# Erätiedosto add_programmes.py:lle
BATCH = {"collected": "2026-10-08", "method": METHOD, "institutions": I, "notes": NOTES}
out = os.path.join(os.path.dirname(__file__), "..", "..", "data", "programmes_batches", "01.json")
json.dump(BATCH, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print({k: len(v) for k, v in I.items()})
