# Erä 17: osittaisten täydennys (aja: python scripts/programmes/b17.py, sitten python scripts/add_programmes.py data/programmes_batches/17.json).
# add_programmes.py korvaa laitoksen rivit, joten KEEP(code) lataa ensin nykyiset rivit (paitsi "Partial list" -rivit, jos drop_partial).
import json
import os
from auto import A, T, IT, L, DC, SM
ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
I = {}
def R(code, discs, levels, name, url, note=None):
    for d in discs.split():
        for lv in (levels.split() if levels else [None]):
            I.setdefault(code, []).append([d, lv, name, url] + ([note] if note else []))
_OLD = json.load(open(os.path.join(ROOT, "data", "programmes.json"), encoding="utf-8"))["programmes"]
def KEEP(code, drop_partial=True, drop_url=None):
    for p in _OLD:
        if p["erasmus_code"] != code: continue
        for e in p["evidence"]:
            if drop_partial and (e.get("note") or "").startswith("Partial list"): continue
            if drop_url and drop_url in e["url"]: continue
            I.setdefault(code, []).append([p["discipline"], e["level"], e["programme_name"], e["url"]] + ([e["note"]] if e.get("note") else []))

CL = "strings woodwind brass percussion piano vocal-opera"; CLN = "Classical music programme; the page does not list the instruments, which are recorded as the usual orchestral instruments, piano and voice"
PARTIAL = "Partial list: the institution's pages found list only some of its programmes"

# --- laitokset ---
c = "I  MILANO09"; MI = "https://www.consmi.it/offerta-formativa/insegnamenti/"  # uusi sivusto; vanhan consmilano.it-listan rivit korvataan
for area, names, lv in [
    ("archi-corde-e-strumenti-a-pizzico", "Arpa, Chitarra, Contrabbasso, Liuto, Mandolino, Viola, Viola da gamba, Violino, Violino barocco, Violoncello", "BA MA"),
    ("canto-e-musica-vocale-da-camera", "Canto, Canto rinascimentale barocco, Musica vocale da camera", "BA MA"),
    ("direzione-dorchestra-direzione-di-coro-e-composizione-corale", "Direzione di coro e composizione corale, Direzione d'orchestra", "BA MA"),
    ("fiati", "Basso tuba, Clarinetto, Clarinetto basso, Corno, Eufonio, Fagotto, Flauto, Oboe, Saxofono, Tromba", "BA MA"),
    ("musica-elettronica", "Musica elettronica, Tecnico del suono", "BA MA"),
    ("musiche-tradizionali", "Musiche tradizionali dell'India", "BA"),
    ("popular-music", "Basso pop rock, Batteria pop rock, Canto pop rock, Chitarra pop rock, Composizione pop rock, Pianoforte pop rock", "BA MA"),
    ("strumenti-a-tastiera-e-percussione-organo", "Fisarmonica, Organo, Pianoforte, Pianoforte storico, Strumenti a percussione", "BA MA"),
    ("didattica-della-musica", "Didattica della musica", "BA MA"),
    ("jazz", "Basso elettrico jazz, Batteria e percussioni Jazz, Canto Jazz, Chitarra Jazz, Clarinetto Jazz, Composizione Jazz, Contrabbasso Jazz, Flauto Jazz, Pianoforte Jazz, Saxofono Jazz, Tromba Jazz, Trombone Jazz", "BA MA"),
    ("musica-antica", "Musica antica (IMA, Istituto di Musica Antica)", "BA MA"),
    ("composizione", "Composizione, Discipline storiche critiche e analitiche della musica", "BA MA")]:
    for lv1 in lv.split(): L(I, c, names, MI + area + "/", lv1)
L(I, c, "Musica d'insieme", MI + "musica-dinsieme/", "MA")
L(I, c, "Maestro collaboratore (pianoforte)", MI + "maestro-collaboratore/", "MA")

c = "I  SALERNO02"; KEEP(c, drop_url="ammissione-ii-livello")
L(I, c, "Arpa, Basso Elettrico Jazz, Basso Tuba, Batteria e Percussioni Jazz, Canto, Canto Jazz, Chitarra, Chitarra Jazz, Clarinetto, Clarinetto Jazz, Clavicembalo e Tastiere Storiche, Composizione Jazz, Composizione Multimediale, Composizione indirizzo Contemporanea, Composizione indirizzo Musica Ambientale, Contrabbasso, Contrabbasso Jazz, Corno, Didattica della Musica, Direzione d'Orchestra, Fagotto, Fisarmonica, Flauto, Musica Elettronica, Musica d'insieme, Oboe, Organo, Pianoforte Jazz, Pianoforte indirizzo Cameristico, Pianoforte indirizzo Solistico, Popular Music indirizzo Basso Pop Rock, Popular Music indirizzo Canto Pop Rock, Popular Music indirizzo Chitarra Pop Rock, Sassofono, Sassofono Jazz, Strumenti a Percussione, Tastiere Elettroniche, Tecnico del suono, Tromba, Tromba Jazz, Trombone, Trombone Jazz, Viola, Violino, Violino Jazz, Violoncello", "https://www.consalerno.it/programmi-di-ammissione-ii-livello", "MA")

c = "I  BOLZANO02"; KEEP(c, drop_url="level-two-academic-courses")  # biennio osastoittain -> soitinkohtaiset opintosuunnitelmat
BZ1 = "https://cons.bz.it/en/study/fields-of-study/level-one-academic-courses/study-plans/"
L(I, c, "Bass tuba, Bassoon, Cello, Clarinet, Double bass, Flute, Guitar, Harp, Horn, Oboe, Percussion instruments, Piano, Recorder, Saxophone, Trombone, Trumpet, Viola, Violin", BZ1, "BA")
for n in "bass-tuba bassoon cello clarinet double-bass flute guitar harp oboe piano recorder saxophone trombone trumpet viola violin composition singing lied-and-oratorio organ".split():
    L(I, c, n.replace("-", " ").capitalize(), "https://cons.bz.it/wp-content/uploads/2020/12/bnn-%s-eng.pdf" % n, "MA")

CS = "https://www.conservatoriocosenza.it/"  # oikea sivusto; conservatoriodicosenza.it on kaapattu (kasinomainoksia)
DC(I, "I  COSENZA03", CS + "corsi-accademici-di-i-livello/")
DC(I, "I  COSENZA03", CS + "corsi-accademici-di-ii-livello/")

def WIX(code, url, lv):
    """Wix-sivu: ohjelmanimet versaalilla lyhyinä tekstisolmuina."""
    import re, html
    from f import get
    names = []
    for x in re.findall(r">([^<>]{3,60})<", get(url)):
        x = re.sub(r"\s+", " ", html.unescape(x)).strip()
        if x.isupper() and x not in names: names.append(x)
    L(I, code, ", ".join(n.replace(",", " ") for n in names), url, lv)
PC = "https://www.conservatorionicolini.com/"  # uusi sivusto; conservatorionicolini.it ei enää ratkea
WIX("I  PIACENZ01", PC + "triennio", "BA")
WIX("I  PIACENZ01", PC + "biennio", "MA")

c = "S  GOTEBOR01"; GU = "https://www.gu.se/en/study-gothenburg/"  # lista: https://www.gu.se/en/music-drama/study-here/music
R(c, "church-music organ", "BA", "Church Music (Bachelor)", GU + "ba-church-music")
R(c, CL, "BA", "Bachelor's Programme in Music, Classical Performance", GU + "bachelors-programme-in-music-with-a-specialization-in-classical-performance-k1kla", CLN)
R(c, "strings woodwind brass percussion", "MA", "Master of Fine Arts in Music, Symphonic Orchestra Performance", GU + "master-of-fine-arts-in-music-with-specialisation-in-symphonic-orchestra-performance-k2ork")
R(c, "organ", "MA", "Master of Fine Arts in Music, Organ and Related Keyboard Instruments", GU + "master-of-fine-arts-in-music-with-specialisation-in-organ-and-related-keyboard-instruments-k2org")
R(c, "composition", "BA", "Composition (Bachelor)", GU + "ba-composition")
R(c, "composition", "MA", "Master of Fine Arts in Music, Experimental Composition and Creation", GU + "master-of-fine-arts-in-music-with-specialisation-in-composition-k2kmp")
R(c, "folk", "BA", "Bachelor of Fine Arts in Contemporary Traditions in Music", GU + "bachelor-of-fine-arts-in-contemporary-traditions-in-music-k1tra")
R(c, "jazz", "BA", "Bachelor's Programme in Music, Improvisation Performance", GU + "bachelors-programme-in-music-with-a-specialization-in-improvisation-performance-k1imp")
R(c, "jazz global-music", "MA", "Master of Fine Arts in Music, Improvisation and World Music Performance", GU + "master-of-fine-arts-in-music-with-specialisation-in-improvisation-and-world-music-performance-k2miv")
R(c, "jazz composition", "MA", "Master of Fine Arts in Music, The Composing Musician", GU + "master-of-fine-arts-in-music-with-specialisation-the-composing-musician-k2com")
R(c, "music-production music-technology", "BA", "Music and Sound Production (Bachelor)", GU + "ba-music-and-sound-production")
R(c, "vocal-opera", "BA", "Bachelor of Fine Arts in Opera", GU + "bachelor-of-fine-arts-in-opera-k1ope")
R(c, "vocal-opera", "MA", "Master of Fine Arts in Opera", GU + "master-of-fine-arts-in-opera-k2mdg")
R(c, "conducting", "MA", "One-year MFA in Choral Conducting", "https://www.gu.se/en/music-drama/study-here/music/one-year-mfa-in-choral-conducting")
R(c, "music-education", None, "Teacher education in music", GU + "teacher-education-in-music", "Teacher education programme; level not stated on the page")

c = "PL GDANSK04"; KEEP(c); GW = "https://www.amuz.gda.pl/wydzialy/"
GI = GW + "wydzial-ii-instrumentalny/kierunki-i-specjalnosci,669"
R(c, "accordion strings woodwind piano guitar harp organ percussion brass", "BA", "Instrumentalistyka: akordeon, altówka, carillon, fagot, flet, fortepian, gitara, harfa, klarnet, kontrabas, obój, organy, perkusja, puzon, saksofon, skrzypce, trąbka, tuba, waltornia, wiolonczela", GI)
R(c, "accordion strings woodwind piano guitar harp organ percussion brass", "MA", "Instrumentalistyka: akordeon, altówka, fagot, flet, fortepian, gitara, harfa, klarnet, kontrabas, obój, organy, perkusja, puzon, saksofon, skrzypce, trąbka, tuba, waltornia, wiolonczela", GI)
R(c, "early-music", "BA", "Instrumentalistyka: fagot historyczny, flety historyczne, klawesyn, skrzypce historyczne, trąbka historyczna, wiolonczela historyczna", GI)
R(c, "early-music", "MA", "Instrumentalistyka: klawesyn", GI)
R(c, "chamber-music", "MA", "Kameralistyka – gra w zespole kameralnym", GI)
R(c, "vocal-opera", "BA MA", "Wokalistyka: śpiew solowy, musical", GW + "wydzial-iii-wokalno-aktorski/kierunek-i-specjalnosci,674")

c = "IRLDUBLIN22"; KEEP(c)
R(c, "piano strings vocal-opera", "BA", "BMus (Keyboard) / BMus (Strings) / BMus (Vocal)", "https://www.riam.ie/degrees-programmes/full-time")
c = "D  MUNSTER01"; KEEP(c)
R(c, CL, "BA MA", "Bachelor / Master of Music – Instrument / Gesang (klassische Ausbildung)", "https://www.uni-muenster.de/Musikhochschule/Studieninteressierte/Bewerbung.html", CLN)

c = "D  STUTTGA03"; KEEP(c); ST = "https://www.hmdk-stuttgart.de/studiengang/"
R(c, "strings woodwind brass percussion harp early-music", "MA", "Master Orchesterinstrumente einschließlich historische Instrumente", ST + "master-orchesterinstrumente-einschliesslich-historische-instrumente")
R(c, "piano early-music", "MA", "Master Klavier / historische Klaviere", ST + "master-klavier-historische-klaviere")
R(c, "piano chamber-music", "MA", "Master Klavierkammermusik einschließlich Klavierduo", ST + "master-klavier-kammermusik-einschliesslich-klavierduo")
R(c, "piano", "MA", "Master Korrepetition; Master Künstlerische Klavierimprovisation", ST + "master-korrepetition")
R(c, "early-music", "MA", "Master Blockflöte, Traversflöte, historische Blockflöten; Master Cembalo; Master historische Tasteninstrumente", ST + "master-blockfloete-traversfloete-historische-blockfloeten")
R(c, "vocal-opera", "MA", "Master Konzertgesang; Master Lied", ST + "master-konzertgesang")
R(c, "jazz", "MA", "Master Jazz", ST + "master-jazz")
R(c, "jazz composition", "MA", "Master Jazzkomposition", ST + "master-jazz-komposition")
R(c, "conducting", "MA", "Master Dirigieren", ST + "master-dirigieren")
R(c, "organ", "MA", "Master Orgelimprovisation", ST + "master-orgel-improvisation")

c = "I  FERRARA02"; KEEP(c); FE = "https://www.conservatorioferrara.it/index.php/"
IT(I, c, FE + "trienni-classici-ordinamentali", "BA", extra_drop=r"\(\d+\)$|comunicazioni|enti convenzionati|jazz club")
R(c, "jazz", "BA", "Trienni Jazz ordinamentali", FE + "trienni-jazz-ordinamentali")
R(c, "jazz", "MA", "Bienni Jazz", FE + "bienni-jazz")
IT(I, c, FE + "bienni-classici-ordinamentali", "MA", extra_drop=r"\(\d+\)$|comunicazioni|enti convenzionati|jazz club|approvazione")

RA = "https://www.verdiravenna.it/offerta-formativa/"
DC(I, "I  RAVENNA02", RA + "piani-di-studio-corso-accademico-di-primo-livello-triennio/")
DC(I, "I  RAVENNA02", RA + "piani-di-studio-corso-accademico-di-secondo-livello-biennio/")
c = "E  ALICANT11"; AL = "https://www.csmalicante.com/csma-estudios-informacion-grado-esp/"
R(c, "composition conducting musicology music-education", "BA", "Grado: Composición, Dirección, Musicología, Pedagogía", AL)
R(c, "piano vocal-opera guitar strings woodwind brass percussion", "BA", "Interpretación: Piano, Canto, Guitarra, Instrumentos de la Orquesta Sinfónica (IOS)", AL)
R(c, CL, "MA", "Máster en Enseñanzas Artísticas de Interpretación e Investigación de la Música", "https://www.csmalicante.com/csma-estudios-informacion-master-esp/", CLN)

METHOD = "Supplement to partial records: the institutions' current programme pages (new domains, sitemaps, area pages) were re-read; rows already recorded and still valid were kept."
NOTES = {}

# Erätiedosto add_programmes.py:lle
BATCH = {"collected": "2026-10-09", "method": METHOD, "institutions": I, "notes": NOTES}
out = os.path.join(ROOT, "data", "programmes_batches", "17.json")
json.dump(BATCH, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print({k: len(v) for k, v in I.items()})
