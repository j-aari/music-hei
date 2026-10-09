# Erä 16: Italian odottaneet konservatoriot ja Alicante (aja: python scripts/programmes/b16.py, sitten python scripts/add_programmes.py data/programmes_batches/16.json). Apufunktio R(alat, tasot, nimi, url, huom) laajentaa rivit.
# L(I, code, "nimi, nimi, ...", url, taso): ohjelmalista koottu laitoksen omasta lähteestä (sivu, bando/manifesti-PDF tai oman verkkotunnuksen hakutulos).
import json
import os
from auto import A, T, IT, L, DC, SM
I = {}
def R(code, discs, levels, name, url, note=None):
    for d in discs.split():
        for lv in (levels.split() if levels else [None]):
            I.setdefault(code, []).append([d, lv, name, url] + ([note] if note else []))

CL = "strings woodwind brass percussion piano vocal-opera"; CLN = "Classical music programme; the page does not list the instruments, which are recorded as the usual orchestral instruments, piano and voice"
PARTIAL = "Partial list: the institution's pages found list only some of its programmes"

# --- laitokset ---
AQ = "https://www.consaq.it/offerta-formativa/corsi-di-studio/"
for u, lv in [(AQ + "accademici-i-livello.html", "BA"), (AQ + "accademici-ii-livello.html", "MA")]:
    IT(I, "I  L-AQUIL04", u, lv, extra_drop=r"settimana|costruzione|teoria, ritmica|^—")

c = "I  PALERMO04"
L(I, c, "Arpa, Arpa rinascimentale e barocca, Basso elettrico, Basso tuba, Batteria e percussioni jazz, Canto, Canto jazz, Canto rinascimentale barocco, Chitarra, Chitarra jazz, Clarinetto, Clarinetto jazz, Clarinetto storico, Clavicembalo e tastiere storiche, Composizione, Contrabbasso, Contrabbasso jazz, Cornetto, Corno, Corno naturale, Didattica della musica, Direzione di coro e composizione corale, Direzione d'orchestra, Discipline storiche critiche analitiche della musica, Eufonio, Fagotto, Fagotto barocco, Fisarmonica, Flauto, Flauto dolce, Flauto traversiere, Liuto, Mandolino, Musica elettronica, Musica vocale da camera, Oboe, Oboe barocco e classico, Organo, Pianoforte, Pianoforte jazz, Sassofono, Sassofono jazz, Strumentazione per orchestra di fiati, Strumenti a percussione, Tastiere elettroniche, Tromba, Tromba jazz, Tromba rinascimentale e barocca, Trombone, Trombone jazz, Trombone rinascimentale e barocco, Viola, Viola da gamba, Violino, Violino barocco, Violino jazz, Violoncello, Violoncello barocco",
  "https://conservatoriopalermo.it/wp-content/uploads/2024/06/Bando-ammissione-Triennio-accademico-di-I-livello-per-2024.2025-1.pdf", "BA")

c = "I  BOLZANO02"; BZ = "https://cons.bz.it/en/study/fields-of-study/level-one-academic-courses/"
L(I, c, "Harp, Guitar, Double bass, Viola, Violin, Cello, Clarinet, Horn, Flute, Singing, Lied and Oratorio in German, Piano, Organ, Percussion, Composition, Orchestra conducting, Music teaching, Electronic music, Early music (baroque violin, historical keyboards)", BZ, "BA")
R(c, "strings woodwind brass percussion piano organ harp guitar vocal-opera composition", "MA", "Level II academic courses (DCSL) by department: string instruments, wind instruments, keyboard and percussion, singing and music theatre, composition", "https://cons.bz.it/en/study/fields-of-study/level-two-academic-courses/")
R(c, "chamber-music", None, "1st level Master's in String Quartet Studies", BZ, "Post-graduate master (Master di I livello)")

c = "I  REGGIO03"; CI = "https://www.conservatoriocilea.it/index.php/offerta-formativa"
L(I, c, "Arpa, Basso tuba, Batteria e percussioni jazz, Canto, Canto jazz, Chitarra, Chitarra jazz, Clarinetto, Composizione, Composizione a indirizzo musicologico, Contrabbasso, Contrabbasso jazz, Corno, Didattica della musica, Discipline storiche critiche e analitiche della musica, Fagotto, Fisarmonica, Flauto, Maestro collaboratore, Oboe, Organo, Pianoforte, Pianoforte jazz", CI, "BA")
L(I, c, "Arpa, Basso tuba, Canto, Chitarra, Clarinetto, Composizione, Contrabbasso, Corno, Didattica della musica e dello strumento, Discipline storiche critiche e analitiche della musica, Fagotto, Flauto e Ottavino, Musica da camera, Oboe, Organo, Pianoforte, Pianoforte jazz, Saxofono", CI, "MA")
R(c, "strings", "BA MA", "Violino, Viola, Violoncello (list on the offerta formativa page continues beyond the excerpt)", CI, PARTIAL)

c = "I  COSENZA03"; CS = "http://portale.conservatoriodicosenza.it/didattica/1triennio.html"
L(I, c, "Basso elettrico Pop/Rock, Batteria e Percussioni Jazz, Canto Jazz, Canto Pop/Rock, Canto rinascimentale e barocco, Chitarra Jazz, Chitarra Pop/Rock, Clavicembalo e Tastiere storiche, Composizione, Composizione Jazz, Corno, Didattica della musica, Direzione di coro e Composizione corale, Direzione d'Orchestra, Eufonio, Pianoforte e Tastiere Pop/Rock, Strumentazione per orchestra di fiati, Strumenti a percussione, Tromba rinascimentale e barocca, Trombone, Trombone Jazz", CS, "BA")
L(I, c, "Basso Elettrico Pop/Rock, Basso tuba, Tastiere Elettroniche, Tromba", "http://portale.conservatoriodicosenza.it/didattica/biennio/ordinamentale.html", "MA")

c = "I  PIACENZ01"; PC = "https://www.conservatorionicolini.it/offerta-formativa/biennio"
L(I, c, "Arpa, Violoncello, Contrabbasso, Pianoforte, Canto, Composizione, Organo, Musica elettronica, Tecnico del suono, Pianoforte jazz, Saxofono jazz, Chitarra jazz", PC, "MA")

c = "I  MILANO09"; MI = "http://www.consmilano.it/it/didattica/corsi-triennio/corsi-accademici-di-i-livello-triennio-ordinamentale-da-a-a-2016-17/corsi-accademici-di-i-livello-triennio-ordinamentale-da-a-a-10-11-fino-a-a-a-15-16"
L(I, c, "Arpa, Basso tuba, Canto, Canto rinascimentale e barocco, Chitarra, Clarinetto, Corno, Didattica della musica, Direzione d'orchestra, Fagotto, Fisarmonica, Flauto, Jazz, Organo, Percussioni, Pianoforte, Violino", MI, "BA")
L(I, c, "Didattica della musica (nuove tecnologie; educazione musicale di base), Fisarmonica digitale, Arpa rinascimentale e barocca, Musica applicata, Popular music (composizione; strumenti e canto)", "https://www.consmilano.it/it/conservatorio/storia-e-mission/perche-studiare-da-noi", "BA")
R(c, CL, "MA", "59 corsi di diploma accademico di II livello", "https://www.consmilano.it/it/conservatorio/storia-e-mission/perche-studiare-da-noi", CLN)

c = "I  PAVIA02"
R(c, "jazz", "BA MA", "Triennio e Biennio Jazz (Pianoforte jazz, Canto jazz, Violino jazz ...)", "https://conspv.it/corsi-accademici/pianoforte-jazz/")
R(c, "popular-music", "BA", "Pianoforte pop rock", "https://conspv.it/i-nostri-corsi/dipartimento-di-nuove-tecnologie-e-linguaggi-musicali/pianoforte-pop-rock/")

c = "I  LA-SPEZ01"; SP = "https://conssp.it/didattica/triennio-di-i-livello/"
L(I, c, "Arpa, Basso Elettrico, Batteria e Percussioni Jazz, Canto, Canto Jazz, Chitarra, Chitarra Jazz, Clarinetto, Clarinetto Jazz, Clavicembalo e Tastiere storiche, Fisarmonica, Organo, Pianoforte, Pianoforte Maestro Collaboratore, Composizione, Discipline Storiche critiche e analitiche della musica, Musica Elettronica – Tecnico del Suono", SP, "BA")
L(I, c, "Arpa, Basso elettrico jazz, Batteria e percussioni jazz", "https://conssp.it/didattica/biennio-di-ii-livello/", "MA")

c = "I  SALERNO02"
DC(I, c, "https://www.consalerno.it/programmi-di-ammissione-i-livello")
R(c, "jazz popular-music", "MA", "Programmi di ammissione II livello (jazz; pop)", "https://www.consalerno.it/programmi-di-ammissione-ii-livello")

c = "I  SIENA04"; SI = "https://conservatoriosiena.it/corsi/"
A(I, c, SI + "corsi-accademici-di-i-livello/", r"corsi-accademici-di-i-livello/scuola-di", default_level="BA")
A(I, c, SI + "corsi-accademici-di-ii-livello/", r"corsi-accademici-di-ii-livello/scuola-di", default_level="MA")

c = "I  REGGIO05"
L(I, c, "Arpa, Canto, Chitarra, Clarinetto, Composizione, Contrabbasso, Corno, Didattica della Musica, Fagotto, Fisarmonica, Flauto, Maestro Collaboratore, Oboe, Organo, Pianoforte, Strumenti a Percussione, Tromba, Trombone, Viola, Violino, Violoncello", "https://peri-merulo.it/index.php?option=com_content&view=article&id=190&Itemid=3026", "BA")
L(I, c, "Arpa, Canto, Chitarra, Clarinetto, Composizione, Contrabbasso, Corno, Fagotto, Fisarmonica, Flauto, Musica da Camera, Oboe, Organo, Pianoforte, Strumenti a Percussione, Tromba, Trombone, Viola, Violino, Violoncello", "https://peri-merulo.it/index.php?Itemid=3433&id=523&option=com_content&view=article", "MA")

IT(I, "I  VERONA02", "https://www.conservatorioverona.it/it/corsi/", None, extra_drop=r"2° strumento|bibliografia|basso continuo|ritmica|regia|PNR|teoria dell|(?-i:^[A-Z ,']+$)")
IT(I, "I  VARESE05", "https://issmpuccinigallarate.it/triennio/", "BA", extra_drop=r"decreto|apri menu")
IT(I, "I  VARESE05", "https://issmpuccinigallarate.it/biennio/", "MA", extra_drop=r"decreto|apri menu")
R("I  VARESE05", "music-education", "BA MA", "Didattica", "https://issmpuccinigallarate.it/triennio/")

c = "I  ROMA30"; SL = "https://saintlouis.eu/"
R(c, "jazz popular-music", "BA MA", "Accademico I/II livello: Basso Elettrico, Canto, Chitarra, Contrabbasso, Piano e Tastiere, Pianoforte, Sassofono, Tromba, Trombone, Violino; Songwriting", SL + "didattica-accademico-i-livello/")
R(c, "composition", "BA MA", "Composizione e Film Scoring; Composizione e Musica Applicata; Composizione e Arrangiamento Jazz (II livello)", SL + "accademico-ii-livello/")
R(c, "music-production", "BA MA", "Music Production", SL + "accademico-ii-livello/")
R(c, "music-technology", "BA MA", "Musica Elettronica; Tecnico del Suono; Sound Design (II livello)", SL + "accademico-ii-livello/")
R(c, "arts-management", "BA MA", "Music Management", SL + "didattica-accademico-i-livello/")

c = "I  FERRARA02"; FE = "https://www.conservatorioferrara.it/index.php/features/corsi-docenti/"
R(c, "jazz", "BA MA", "Trienni / Bienni Jazz ordinamentali", FE + "corsi-accademici-di-i-livello", PARTIAL)
R(c, "music-technology", "BA", "Triennio Tecnico del Suono", FE + "corsi-accademici-di-i-livello")
R(c, "music-therapy", "MA", "Biennio di Musicoterapia", FE + "corsi-accademici-di-ii-livello")

TO = "https://www.conservatoriotorino.eu/formazione/"
DC(I, "I  TORINO05", TO + "corsi-accademici-i-livello/elenco-corsi-di-primo-livello/")
DC(I, "I  TORINO05", TO + "corsi-accademici-ii-livello/elenco-corsi-di-secondo-livello/")
IT(I, "I  PADOVA02", "https://www.conservatoriopollini.it/site/it/didattica-corsi-accademici/", None, extra_drop=r"test di|\(old\)")
IT(I, "I  CATANZA04", "https://conscz.it/?pagina=Documento&Categoria=Triennio+di+I+livello+Piano+di+studi", "BA", extra_drop=r"^audio$|beni immobili|fattura|gestione|insegnamenti|offerta formativa")
R("I  CATANZA04", "folk", "BA", "Musiche tradizionali (DCPL65): Chitarra battente, Fisarmonica diatonica, Fisarmonica tradizionale", "https://conscz.it/?pagina=Documento&Categoria=Triennio+di+I+livello+Piano+di+studi")
IT(I, "I  TERNI01", "https://www.briccialditerni.it/ita/85/programmi-didattici-e-piani-di-studio/", None, extra_drop=r"organi di")
SM(I, "I  PESARO01", "https://www.conservatoriorossini.it/corsi-sitemap.xml", r"/corsi/[^/]+-(triennio|biennio)", drop=r"/en/")
CA = "https://conservatoriocagliari.it/corso-accademico-di-%s-livello/piani-di-studio.html"  # luettelo sivuston sivukartasta (piani di studio -sivut)
L(I, "I  CAGLIAR02", "Arpa, Arpa rinascimentale e barocca, Basso elettrico, Basso tuba, Batteria e percussioni jazz, Canto, Canto jazz, Canto rinascimentale e barocco, Chitarra, Chitarra jazz, Clarinetto, Clarinetto jazz, Clavicembalo e tastiere storiche, Composizione, Composizione ad indirizzo musicologico, Contrabbasso, Contrabbasso jazz, Corno, Didattica della musica, Direzione d'orchestra, Direzione di coro e composizione corale, Discipline storiche critiche e analitiche della musica, Fagotto, Fagotto barocco, Fisarmonica, Flauto, Flauto dolce, Flauto traversiere, Liuto, Maestro collaboratore, Musica elettronica, Musica sacra, Musiche tradizionali ad indirizzo etnomusicologico, Musiche tradizionali ad indirizzo launeddas, Musiche tradizionali indirizzo strumentale bandoneon, Oboe, Oboe barocco, Organo, Pianoforte, Pianoforte jazz, Pianoforte storico, Saxofono, Saxofono jazz, Strumenti a percussione, Tastiere elettroniche jazz, Tromba, Tromba jazz, Tromba rinascimentale e barocca, Trombone, Trombone jazz, Trombone rinascimentale e barocco, Viola, Viola da gamba, Violino, Violino barocco, Violino jazz, Violoncello, Violoncello barocco", CA % "i", "BA")
L(I, "I  CAGLIAR02", "Arpa, Basso elettrico, Batteria e percussioni jazz, Canto, Canto jazz, Chitarra, Chitarra jazz, Clarinetto, Clarinetto jazz, Clavicembalo e tastiere storiche, Composizione, Contrabbasso, Contrabbasso jazz, Corno, Didattica della musica indirizzo generale, Didattica della musica indirizzo strumentale, Direzione d'orchestra, Direzione di coro e composizione corale, Fagotto, Fisarmonica, Flauto, Maestro collaboratore, Musica di insieme, Musica elettronica, Musiche tradizionali indirizzo etnomusicologico, Oboe, Organo, Pianoforte, Pianoforte jazz, Saxofono, Saxofono jazz, Strumenti a percussione, Teorie e tecniche in musicoterapia, Tromba, Tromba jazz, Trombone, Viola, Violino, Violoncello", CA % "ii", "MA")
SM(I, "I  LIVORNO01", "https://www.consli.it/corsi-sitemap.xml", r"/corsi/.", ba=r".")
SM(I, "I  CASTELF01", "https://conscfv.it/corsi-sitemap.xml", r"/corsi/.", ba=r"^$", ma=r"^$")
SM(I, "I  FERMO01", "https://conservatorio.net/wp-sitemap-posts-lp_course-1.xml", r"/courses/.", ba=r"^$", ma=r"^$")
SM(I, "I  PAVIA02", "https://conspv.it/corso-sitemap.xml", r"/corso/.", ba=r"^$", ma=r"^$", drop=r"storia|teoria|lingua|materie|tecnica-della|consapevolezza|informatica|pratica-e-lettura|accompagnamento|insieme")

IT(I, "I  FOGGIA02", "https://www.conservatoriofoggia.it/bachelor-degree-program/?lang=en", "BA", extra_drop=r"ph\.d|elements of|score reading|organ.aria|^music theory")
IT(I, "I  CAMPOBA03", "https://www.conservatorioperosi.it/cms/it/didattica/trienni.html", "BA", extra_drop=r"level -|fatturazione|gestione|didattica in web")
IT(I, "I  CATANIA06", "https://www.istitutobellini.it/2020/?page_id=4014", None, extra_drop=r"audio|distanza|scorrere")
DC(I, "I  CATANIA06", "https://www.conservatoriocatania.it/?page_id=13247")

GE = "https://www.conspaganini.it/"
IT(I, "I  GENOVA02", GE + "corsi-primo-livello-scheda-corsi/", "BA", extra_drop=r"prova finale|piani|sito_")
IT(I, "I  GENOVA02", GE + "corsi-secondo-livello-scheda-corsi/", "MA", extra_drop=r"prova finale|piani|sito_")
SM(I, "I  CALTANI01", "https://www.conservatoriocaltanissetta.eu/page-sitemap.xml", r"/programmi-dei-corsi-", ba=r".", ma=r"biennio")
SM(I, "I  BRESCIA06", "https://www.consbs.it/corso-sitemap.xml", r"/corso/(tri|bie)-", ba=r"/tri-", ma=r"/bie-")
SM(I, "I  BENEVEN03", "https://www.conservatorio.bn.it/course-sitemap.xml", r"/corsi/.", ba=r"^$", ma=r"dcsl|secondo-livello", drop=r"storia-della-musica")
SM(I, "I  PESCARA01", "https://www.conservatoriope.it/triennio-sitemap.xml", r"/triennio/.", ba=r".")
SM(I, "I  PESCARA01", "https://www.conservatoriope.it/biennio-sitemap.xml", r"/biennio/.", ma=r".")
ML = "https://www.madernalettimi.it/didattica/"
IT(I, "I  CESENA03", ML + "triennio-accademico", "BA")
IT(I, "I  CESENA03", ML + "biennio-accademico", "MA")

RA = "https://www.verdiravenna.it/istituto/manifesto-degli-studi-issm-g-verdi-a-a-2021-2022/"
L(I, "I  RAVENNA02", "Canto, Chitarra, Clarinetto, Composizione, Contrabbasso, Corno, Fagotto, Flauto, Oboe, Pianoforte, Saxofono, Strumenti a Percussione, Tromba, Trombone, Viola, Violino, Violoncello", RA, "BA")
L(I, "I  RAVENNA02", "Canto, Chitarra, Clarinetto, Composizione, Contrabbasso, Corno, Fagotto, Flauto, Oboe, Pianoforte, Saxofono, Tromba, Trombone, Viola, Violino, Violoncello, Musica da Camera", RA, "MA")

TS = "https://conts.it/media/documents/GUIDA_STUDENTE_MANIFESTO_STUDI_qGBaam0.pdf"  # Manifesto degli Studi, taulukko: propedeutico / I livello / II livello
L(I, "I  TRIESTE02", "Arpa, Chitarra, Contrabbasso, Viola, Violino, Violoncello, Basso Tuba, Clarinetto, Corno, Eufonio, Fagotto, Flauto, Oboe, Saxofono, Tromba, Trombone, Fisarmonica, Organo, Pianoforte, Strumenti a percussione, Canto, Canto rinascimentale e barocco, Clavicembalo e tastiere storiche, Direzione d'orchestra, Direzione di coro, Flauto dolce, Liuto, Viola da gamba, Violino barocco, Violoncello barocco, Composizione, Musica elettronica, Basso elettrico, Batteria e percussioni jazz, Canto jazz, Chitarra jazz, Clarinetto jazz, Contrabbasso jazz, Pianoforte jazz, Saxofono jazz, Tromba jazz, Trombone jazz, Didattica della musica", TS, "BA")
L(I, "I  TRIESTE02", "Arpa, Chitarra, Contrabbasso, Viola, Violino, Violoncello, Basso Tuba, Clarinetto, Corno, Fagotto, Flauto, Oboe, Saxofono, Tromba, Trombone, Pianoforte, Strumenti a percussione, Canto, Canto rinascimentale e barocco, Clavicembalo e tastiere storiche, Direzione d'orchestra, Direzione di coro, Liuto, Viola da gamba, Violino barocco, Violoncello barocco, Organo - ind. musica antica, Musica elettronica, Strumentazione per orchestra di fiati, Basso elettrico, Batteria e percussioni jazz, Clarinetto jazz, Contrabbasso jazz, Pianoforte jazz, Ensemble jazz, Musica da camera", TS, "MA")

c = "E  ALICANT11"; AL = "https://www.csmalicante.com/csma-estudios-acceso-grado-esp/"
R(c, "composition conducting musicology music-education", "BA", "Grado en Enseñanzas Artísticas Superiores de Música: Composición, Dirección, Musicología, Pedagogía", AL)
R(c, "vocal-opera guitar strings woodwind brass percussion", "BA", "Interpretación: itinerarios Canto, Guitarra, Instrumentos de Orquesta Sinfónica", AL, PARTIAL)
R(c, CL, "MA", "Máster en Enseñanzas Artísticas: Interpretación e Investigación de la Música", "http://www.csmalicante.com/files/Master/PUBLI_MASTER_CSMA_1819.pdf", CLN)

c = "I  VICENZA03"
R(c, "early-music", "BA MA", "Dipartimento di Musica Antica: violino e violoncello barocco, viola da gamba, flauto dolce, traversiere, oboe barocco e classico (trienni e bienni)", "https://www.consvi.it/dipma/index.php/docenti", PARTIAL)
R(c, "composition", "BA MA", "Dipartimento di Studi Musicologici e Composizione: triennio e biennio di Composizione", "https://www.consvi.it/dip-composizione/")
R(c, "jazz", "BA MA", "Dipartimento di Musica Jazz: corsi accademici triennali e biennali", "https://www.consvi.it/dip-jazz/site/it/contatti/")
R(c, "global-music", "BA", "Triennio di musiche tradizionali extraeuropee (musica indiana)", "https://www.consvi.it/studenti/site/it/orientamento/")
R(c, "conducting composition", "BA MA", "Direzione di coro e composizione corale (triennio, biennio)", "https://www.consvi.it/studenti/site/it/corsi_accademici/")

METHOD = "Field-level collection as in batch 1. Most Italian conservatory sites list their triennio/biennio courses only via JavaScript menus or in PDFs; the lists were taken from each institution's own pages, admission notices (bando) or study manifestos, located where necessary with a web search restricted to the institution's own domain. Names mapped to disciplines.json by keyword and checked by hand."
NOTES = {}

# Erätiedosto add_programmes.py:lle
BATCH = {"collected": "2026-10-08", "method": METHOD, "institutions": I, "notes": NOTES}
out = os.path.join(os.path.dirname(__file__), "..", "..", "data", "programmes_batches", "16.json")
json.dump(BATCH, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print({k: len(v) for k, v in I.items()})
