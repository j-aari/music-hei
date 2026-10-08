# Erä 13: Portugali, Romania, Serbia, Slovakia, Slovenia, Ruotsi, Turkki (aja: python scripts/programmes/b13.py, sitten python scripts/add_programmes.py data/programmes_batches/13.json). Apufunktio R(alat, tasot, nimi, url, huom) laajentaa rivit.
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

c = "P  LISBOA05"; EL = "https://www.esml.ipl.pt/"
R(c, "vocal-opera guitar strings woodwind brass percussion organ piano", "BA", "Licenciatura em Música – Execução: Canto, Cordas Dedilhadas, Instrumentos de Arco, Sopro e Percussão, Órgão, Piano", EL + "cursos/licenciaturas/licenciatura-em-musica/59-ensinoformacao")
R(c, "early-music", "BA MA", "Execução – Música Antiga; Mestrado em Música – Música Antiga", EL + "cursos/mestrados/mestrado-em-musica")
R(c, "composition conducting music-theory", "BA", "Licenciatura em Música – Composição, Direção e Formação Musical", EL + "cursos/licenciaturas/licenciatura-em-musica/67-ensinoformacao/licenciatura-em-musica/72-composicao")
R(c, "jazz", "BA MA", "Licenciatura em Música – Jazz; Mestrado em Música – Jazz", EL + "index.php/cursos/licenciaturas/licenciatura-em-musica/67-ensinoformacao/licenciatura-em-musica/176-jazz")
R(c, "music-technology", "BA", "Licenciatura em Tecnologias da Música", EL + "cursos/licenciaturas/licenciatura-em-musica/59-ensinoformacao")
R(c, CL + " composition conducting chamber-music", "MA", "Mestrado em Música: Canto, Composição, Direção Coral, Direção de Orquestra, Instrumento, Música de Câmara", EL + "cursos/mestrados/mestrado-em-musica", CLN)
R(c, "music-education", "MA", "Mestrado em Ensino de Música", EL + "cursos/mestrados/mestrado-em-ensino-de-musica")
c = "P  PORTO05"; EP = "https://www.esmae.ipp.pt/"
R(c, "composition", "BA MA", "Licenciatura em Música – Composição; Mestrado em Composição", EP + "cursos/licenciatura")
R(c, "jazz", "BA MA", "Licenciatura em Música – Jazz; Mestrado Música – Interpretação Artística (Jazz)", EP + "cursos/licenciatura/1017")
R(c, "music-technology music-production", "BA MA", "Licenciatura – Produção e Tecnologias da Música; Mestrado em Artes e Tecnologias do Som", EP + "cursos/licenciatura/1015")
R(c, CL, "MA", "Mestrado em Música – Interpretação Artística", EP + "departamentos/dep-musica", CLN)
R(c, "music-education", "MA", "Mestrado em Ensino de Música", EP + "departamentos/dep-musica")
c = "P  AVEIRO01"; AV = "https://www.ua.pt/deca"
R(c, CL + " jazz", "BA MA", "Licenciatura em Música; Mestrado em Música (incl. Performance Jazz)", AV, CLN)
R(c, "music-education", "MA", "Mestrado em Ensino de Música", "https://www.ua.pt/pt/c/184/p")
c = "SK BRATISL05"; VS = "https://htf.vsmu.sk/studium/"
R(c, "church-music", "BA MA", "Cirkevná hudba", VS)
R(c, "accordion piano organ", "BA MA", "Klávesové nástroje (akordeón, klavír, organ)", VS)
R(c, "chamber-music", "MA", "Komorná hra", VS)
R(c, "composition conducting", "BA MA", "Skladba a dirigovanie (skladba, dirigovanie orchestra, dirigovanie zboru)", VS)
R(c, "vocal-opera", "BA MA", "Spev", VS)
R(c, "strings guitar harp woodwind brass", "BA MA", "Strunové a dychové nástroje", VS)
R(c, "music-theory arts-management", "BA MA", "Teória a dramaturgia hudby (teória hudby, dramaturgia a manažment hudby)", VS)
c = "SI LJUBLJA01"; AG = "https://www.ag.uni-lj.si/"
R(c, "strings harp guitar piano organ accordion woodwind brass percussion vocal-opera conducting composition church-music", "BA MA", "Glasbena umetnost (26 smeri, I. in II. stopnja)", AG + "studij/predstavitev-studija")
R(c, "early-music", "BA MA", "Glasbena umetnost – čembalo, kljunasta flavta", AG + "studij/oddelki-in-katedre-1")
R(c, "music-education", "BA MA", "Glasbena pedagogika; Instrumentalna in pevska pedagogika (II. stopnja)", AG + "studij/podiplomski-studij-ii-stopnje")

c = "RO CLUJNAP02"; CJ = "https://anmgd.ro/oferta-educationala/master/"
R(c, "vocal-opera strings woodwind brass percussion", "MA", "Masterat Interpretare muzicală: Canto, Instrumente cu coarde, Instrumente de suflat și percuție", CJ + "facultatea-de-interpretare-muzicala/")
R(c, "music-education composition musicology conducting", "MA", "Pedagogie muzicală / Artă muzicală; Compoziţie, Muzicologie, Dirijat", CJ + "facultatea-teoretica/")
c = "RO IASI01"; IA = "https://www.arteiasi.ro/facultatea-de-interpretare-compozitie-si-studii-muzicale-teoretice/"
R(c, "piano strings woodwind brass percussion accordion", "BA MA", "Interpretare muzicală – Instrumente", IA + "studii-de-licenta/interpretare-muzicala-instrumente/")
R(c, "vocal-opera", "BA MA", "Interpretare muzicală – Canto", IA + "studii-de-licenta/interpretare-muzicala-canto/")
R(c, "composition", "BA MA", "Compoziție muzicală (clasică)", IA + "studii-de-licenta/compozitie-muzicala-compozitie-clasica-compozitie-muzica-usoara-jazz/")
R(c, "jazz popular-music", "BA", "Compoziție muzicală – muzică ușoară și jazz", IA + "studii-de-licenta/compozitie-muzicala-compozitie-clasica-compozitie-muzica-usoara-jazz/")
R(c, "conducting musicology church-music", "BA MA", "Dirijat; Muzicologie; Muzică religioasă", IA + "studii-masterat/")
R(c, "music-education", "BA", "Muzică; Pedagogie muzicală", IA)
c = "RO TARGU01"
R(c, "music-education", "BA MA", "Muzică (licență); Educație muzicală contemporană (master)", "https://www.uat.ro/facultati-si-programe-de-studiu")
R(c, "composition", "BA", "Concepții muzicale contemporane", "https://www.uat.ro/facultati-si-programe-de-studiu")
c = "RS BELGRAD01"; BG = "https://www.fmu.bg.ac.rs/about-us/structure/departments/"
R(c, "piano strings woodwind brass vocal-opera composition conducting music-theory musicology chamber-music", "BA MA", "Departments: Piano, String Instruments, Wind Instruments, Vocal Studies, Composition, Conducting, Music Theory, Musicology, Chamber Music", "https://www.fmu.bg.ac.rs/studies/study-programs/")
R(c, "jazz popular-music", "BA MA", "Department of Jazz and Popular Music", "https://www.fmu.bg.ac.rs/studies/study-programs/")
R(c, "music-education", "BA MA", "Solfeggio and Music Pedagogy Department", "https://www.fmu.bg.ac.rs/studies/study-programs/")
R(c, "folk", "BA MA", "Department of Ethnomusicology", BG + "department-of-ethnomusicology/")
c = "RS NOVISAD02"; NS = "https://akademija.uns.ac.rs/"
R(c, "piano strings woodwind brass guitar harp organ percussion vocal-opera", "BA MA", "Izvođačke umetnosti: klavir, gudački, duvački, gitara, harfa, orgulje, udaraljke, solo pevanje", NS + "departman-muzicke-umetnosti-3/")
R(c, "composition music-education musicology", "BA MA", "Kompozicija; Muzička pedagogija; Muzikologija i etnomuzikologija", NS + "studijski-programi/")
R(c, "music-technology", "MA", "Muzika i mediji (master)", NS + "master-studije-muzika-i-mediji/")

c = "S  GOTEBOR01"; GU = "https://www.gu.se/studera/hitta-utbildning/"
R(c, "church-music organ", "BA", "Konstnärligt kandidatprogram i musik, inriktning Kyrkomusik", GU + "konstnarligt-kandidatprogram-i-musik-inriktning-kyrkomusik-k1kyr")
R(c, "music-production composition", "BA", "Konstnärligt kandidatprogram i musik, inriktning Musik- och ljudproduktion", GU + "konstnarligt-kandidatprogram-i-musik-inriktning-musik-och-ljudproduktion-k1mlp")
R(c, "composition", "BA MA", "Kandidatprogram, inriktning Komposition; Masterprogram Experimental Composition and Creation", GU + "konstnarligt-kandidatprogram-i-musik-inriktning-komposition-k1kmp")
R(c, "jazz global-music", "MA", "Masterprogram i musik: Improvisation or World Music", "https://www.gu.se/en/study-gothenburg/improvisation-or-world-music-k2miv")
c = "S  LUND01"; MH = "https://www.mhm.lu.se/utbildning/"
R(c, "strings woodwind brass percussion harp", "BA MA", "Musikerutbildning – Symfoniorkesterinstrument (kandidat, master)", MH + "musikerutbildningar/symfoniorkesterinstrument-0")
R(c, "vocal-opera", "MA", "Konstnärligt masterprogram i musik – Sång", MH + "antagning/antagning-musiker-och-kyrkomusikerutbildningar/antagning-till-konstnarligt-masterprogram-i-musik/antagning-till-sang-master")
R(c, "folk global-music", "BA", "Konstnärligt kandidatprogram i musik – Folk- och världsmusik", MH + "musikerutbildningar/folk-och-varldsmusik")
R(c, "church-music composition", "MA", "Konstnärligt masterprogram i kyrkomusik, Arrangering och komposition", "https://www.lu.se/lubas/i-uoh-lu-KAKYM-ARKO/18750")
R(c, "composition", "MA", "Konstnärligt masterprogram i musik, Komposition – Musik för film och media", "https://www.lu.se/lubas/i-uoh-lu-KAMUS-KOFM")
R(c, "music-education jazz", "BA MA", "Ämneslärarutbildning i musik för gymnasieskolan (incl. jazz)", MH + "program-och-kurser/amneslararutbildning-i-musik-for-gymnasieskolan-gy/folk-och-0")
c = "S  KARLSTA01"; KS = "https://www.kau.se/musikhogskolan-ingesund/utbildning/"
R(c, "strings piano vocal-opera guitar woodwind", "BA", "Konstnärlig kandidat musiker (violin, viola, cello, kontrabas, piano, sång, gitarr, flöjt, klarinett)", KS + "program/konstnarlig-kandidat-musiker-180-hp/om-konstnarlig")
R(c, "music-education jazz folk", "BA MA", "Musiklärarprogrammet 300 hp (folkmusik, klassisk, jazz)", KS + "program/musiklararprogrammet-300-hp/om-musiklararprogrammet")
R(c, "music-production", "BA", "Musikproduktionsprogrammet 180 hp", KS + "program")
c = "S  LULEA01"; LT = "https://www.ltu.se/en/education/programme/"
R(c, CL + " jazz popular-music composition music-production church-music", "BA", "Bachelor Programme in Music: Jazz, Classical, Composition, Music Production and Songwriting, Rock, Studio, Church Musician", LT + "kkmug-bachelor-programme-in-music", CLN)
R(c, CL + " composition conducting", "MA", "Master Programme in Music Performance: musician, composition, conducting", LT + "kmmga-master-programme-in-music-performance", CLN)
c = "S  OREBRO01"; OR = "https://www.oru.se/utbildning/program/"
R(c, "jazz popular-music", "BA", "Konstnärligt kandidatprogram i musikalisk gestaltning, inriktning Jazz och pop", OR + "konstnarligt-kandidatprogram-i-musikalisk-gestaltning-inriktning-jazz-och-pop/")
R(c, "chamber-music composition music-production", "BA", "Konstnärligt kandidatprogram: Kammarmusik, Komposition, Musikproduktion och songwriting", "https://www.oru.se/institutioner/musikhogskolan/utbildning/program/")
R(c, "music-education", "BA MA", "Ämneslärarprogrammet Musik", "https://www.oru.se/institutioner/musikhogskolan/utbildning/program/")
c = "S  STOCKHO15"; SM = "https://smi.se/pdf/blankett/smiUtbKat2024.pdf"
R(c, "music-education", "BA", "Kandidatexamen i musikpedagogik (Instrument/Sång, Musikskapande)", SM)
R(c, "accordion brass guitar piano percussion strings vocal-opera woodwind", "BA", "Musikpedagogik – profiler: dragspel, bleckblås, bas, elgitarr, gitarr, piano, slagverk, stråk, sång, träblås", "https://smi.se/utbildningar/programutbildning/instrument-sang/index.html")
R(c, "composition music-production", "BA", "Musikpedagogik – Musikskapande (låtskrivande, musikproduktion, komposition)", SM)
c = "S  STOCKHO27"; UA = "https://www.uniarts.se/utbildningar/"
R(c, "vocal-opera", "BA", "Kandidatprogram i opera med inriktning sång", UA + "kandidatprogram/kandidatprogram-i-opera-med-inriktning-sang/")
R(c, "vocal-opera", "MA", "Magisterprogram i opera med inriktning sång", UA + "magister-masterprogram/magisterprogram-i-opera-med-inriktning-sang/")

TPI = "piano harp guitar strings woodwind brass percussion"
c = "TR ANKARA26"; MG = "https://www.mgu.edu.tr/"
R(c, TPI, "BA MA", "Müzik ve Sahne Sanatları Fakültesi – Çalgı Eğitimi Bölümü; Çalgı Eğitimi Ana Sanat Dalı (yüksek lisans)", MG + "muzik-ve-sahne-sanatlari-fakultesi/", CLN)
R(c, "vocal-opera", "BA MA", "Ses Eğitimi Bölümü; Ses Eğitimi Ana Sanat Dalı (yüksek lisans)", MG + "ses-egitimi-bolumu-akademik-kadro/")
R(c, "composition conducting", "BA MA", "Bestecilik / Kompozisyon ve Orkestra Şefliği; Bestecilik tezli yüksek lisans", MG + "muzik-ve-guzel-sanatlar-enstitusu/")
R(c, "jazz popular-music", "BA", "Sahne Sanatları Bölümü – Caz ve Popüler Müzik ASD", MG + "sahne-sanatlari-bolumu/")
R(c, "folk", "BA", "Türk Halk Müziği; Çalgı Eğitimi – saz/bağlama", MG + "calgi-egitimi-bolumu-saz-baglama/")
R(c, "music-technology", "BA MA", "Müzik Bilimleri ve Teknolojileri Fakültesi; Müzik Teknolojileri tezli yüksek lisans", MG + "muzik-ve-guzel-sanatlar-enstitusu-muzik-teknolojileri-tezli-yuksek-lisans-programi/")
c = "TR ISTANBU06"; MS = "https://msgsu.edu.tr/akademik/istanbul-devlet-konservatuvari/bolumler/"
R(c, TPI, "BA MA", "Müzik Bölümü: Piyano-Arp-Gitar, Yaylı Çalgılar, Üflemeli ve Vurmalı Çalgılar", MS + "muzik-bolumu/")
R(c, "composition conducting music-theory", "BA MA", "Bestecilik ve Orkestra Şefliği (bestecilik, orkestra şefliği, müzik teorisi)", MS + "muzik-bolumu/")
R(c, "musicology folk", "BA MA", "Müzikoloji Bölümü (müzikoloji, etnomüzikoloji)", MS + "muzikoloji/")
R(c, "vocal-opera", "BA MA", "Sahne Sanatları Bölümü – Opera", "https://msgsu.edu.tr/akademik/lisansustu-egitim-enstitusu/programlar/")
c = "TR IZMIR01"; DE = "https://tercihrehberi.deu.edu.tr/wp-content/uploads/2022/07/konservatuvar.pdf"
R(c, TPI + " composition", "BA", "Müzik Bölümü: Piyano, Gitar, Arp, Yaylı, Üfleme ve Vurma Çalgılar, Kompozisyon", DE)
R(c, "vocal-opera musicology", "BA", "Sahne Sanatları – Opera; Müzikoloji Bölümü", DE)
R(c, CL + " composition", "MA", "Müzik (Konservatuvar) Yüksek Lisans", "https://gse.deu.edu.tr/en/master-of-music-mmus/", CLN)
R(c, "musicology", "MA", "Müzik Bilimleri Yüksek Lisans", "https://gse.deu.edu.tr/en/master-of-science-msc/")
R(c, "music-technology", "MA", "Müzik Teknolojisi Yüksek Lisans", "https://gse.deu.edu.tr/en/master-of-science/")
c = "TR ISTANBU18"; MT = "https://www.maltepe.edu.tr/konservatuvar"
R(c, TPI + " composition conducting", "BA MA", "Müzik Bölümü: Bestecilik ve Orkestra Şefliği, Piyano-Arp-Gitar, Üflemeli ve Vurmalı Çalgılar, Yaylı Çalgılar (lisans, yüksek lisans)", MT)
R(c, "folk", "BA", "Türk Müziği Bölümü – Türk Halk Müziği", MT)
c = "TR IZMIR05"; YA = "https://music.yasar.edu.tr/"
R(c, "jazz", "BA MA", "Müzik Bölümü – caz alanları (piyano, vokal, gitar, bas, davul); Caz Performans ASD (yüksek lisans)", "https://mssyltezli.yasar.edu.tr/caz-performans-caz-gitar-anasanat-dali/")
R(c, "composition music-technology", "BA MA", "Bestecilik, Elektroakustik Müzik, Müzik Teknolojileri; Müzik ve Sahne Sanatları Yüksek Lisans", YA)

c = "RS NIS01"; NI = "http://www.artf.ni.ac.rs/lat/"
R(c, "piano strings woodwind brass vocal-opera guitar accordion percussion", "BA MA", "Izvođačke umetnosti: klavir, gudački, duvački instrumenti, solo pevanje, gitara, harmonika, udaraljke", NI + "master-akademske-studije/")
R(c, "music-theory music-education", "BA MA", "Muzička teorija i pedagogija; Muzička pedagogija (master)", NI + "master-akademske-studije/")
c = "RS KRAGUJE01"; KG = "https://www.filum.kg.ac.rs/index.php?Itemid=595&lang=sr"
R(c, "woodwind brass strings accordion piano vocal-opera guitar", "BA MA", "Izvođačke umetnosti (duvački, gudački, harmonika, klavir, solo pevanje, trzački instrumenti)", KG)
R(c, "chamber-music", "MA", "Izvođačke umetnosti – kamerna muzika", KG)
R(c, "music-theory music-education", "BA MA", "Muzička teorija i pedagogija; Muzička pedagogija", KG)
R(c, "music-technology", "BA MA", "Muzika u medijima", KG)
R(c, "accordion", "Doc", "Doktorske akademske studije – Izvođačke umetnosti: harmonika", "https://www.filum.kg.ac.rs/index.php?option=com_content&view=article&id=46&Itemid=110&lang=sr")
c = "P  LISBOA12"
R(c, "jazz popular-music", "BA", "Licenciatura em Jazz e Música Moderna (jazz ou música moderna pop/rock)", "https://www.lis.ulusiada.pt/en-gb/degrees/1314/1stcycle-undergraduatedegreesandintegratedmasters/jazzandmodernmusic.aspx")

METHOD = "Field-level collection as in batch 1; where a site lists programmes only via JavaScript, the programme pages were located with a web search restricted to the institution's own domain (raw HTML of each institution's own programme pages, PDFs where the list was only there; names mapped to disciplines.json by keyword and checked by hand)."
NOTES = {
    "SI LJUBLJA33": "The conservatoire's higher vocational school (Višja baletna šola) teaches only ballet; its music programmes are at basic and secondary level, not degree programmes.",
}

# ErÃ¤tiedosto add_programmes.py:lle
BATCH = {"collected": "2026-10-08", "method": METHOD, "institutions": I, "notes": NOTES}
out = os.path.join(os.path.dirname(__file__), "..", "..", "data", "programmes_batches", "13.json")
json.dump(BATCH, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print({k: len(v) for k, v in I.items()})
