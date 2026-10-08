# Erä 2: Bosnia ja Hertsegovina – Viro (aja: python scripts/programmes/b02.py, sitten python scripts/add_programmes.py data/programmes_batches/02.json). Apufunktio R(alat, tasot, nimi, url, huom) laajentaa rivit.
import json
import os
from auto import A, T
I = {}
def R(code, discs, levels, name, url, note=None):
    for d in discs.split():
        for lv in (levels.split() if levels else [None]):
            I.setdefault(code, []).append([d, lv, name, url] + ([note] if note else []))

# --- laitokset ---

c = "BA BANJA02"; U = "https://au.unibl.org/index.php/muzicka-umjetnost/"
R(c, "composition conducting musicology music-theory music-education vocal-opera piano accordion guitar woodwind brass strings", "BA MA",
  "Музичка умјетност: Композиција, Дириговање, Етномузикологија, Музичка теорија и педагогија, Соло пјевање, Инструменти са диркама, Трзалачки, Дувачки, Гудачки инструменти", U + "o-programu")
R(c, "chamber-music", "BA MA Doc", "Камерна музика (мастер и докторске студије из области камерне музике)", U + "o-programu")

c = "BA SARAJEV01"; M = "http://www.mas.unsa.ba/"
R(c, "conducting", "BA MA", "Odsjek za dirigovanje (I i II ciklus)", M + "odsjek-za-dirigovanje")
R(c, "woodwind brass accordion", "BA MA", "Odsjek za duvačke instrumente i harmoniku", M + "odsjek-za-duva%C4%8Dke-instrumente-i-harmoniku")
R(c, "strings guitar", "BA MA", "Odsjek za gudačke instrumente i gitaru", M + "odsjek-za-guda%C4%8Dke-instrumente-i-gitaru")
R(c, "piano percussion harp", "BA MA", "Odsjek za klavir, udaraljke, harfu i srodne instrumente", M + "odsjek-za-klavir-udaraljke-harfu-i-srodne-instrumente")
R(c, "composition", "BA MA", "Odsjek za kompoziciju", M + "odsjek-za-kompoziciju")
R(c, "musicology", "BA MA", "Odsjek za muzikologiju i etnomuzikologiju", M + "odsjek-za-muzikologiju-i-etnomuzikologiju")
R(c, "music-theory music-education", "BA MA", "Odsjek za muzičku teoriju i pedagogiju", M + "odsjek-za-muzi%C4%8Dku-teoriju-i-pedagogiju")
R(c, "vocal-opera", "BA MA", "Odsjek za solo pjevanje", M + "odsjek-za-solo-pjevanje")

c = "BG PLOVDIV07"; P = "http://www.artacademyplovdiv.com/specialnosti/"
R(c, "piano accordion vocal-opera", "BA MA", "Изпълнителско изкуство (класически инструмент или класическо пеене); катедра Пиано и акордеон", P + "all.html")
R(c, "jazz popular-music", "BA MA", "Изпълнителско изкуство (поп и джаз)", P + "IIPD.html")
R(c, "folk", "BA MA", "Изпълнителско изкуство (народен инструмент или народно пеене)", P + "IIF.html")
R(c, "conducting", "BA", "Дирижиране на народни състави", P + "DNS.html")
R(c, "conducting", "MA", "Дирижиране (хорово и оркестрово)", P + "DIR.html")
R(c, "composition", "MA", "Композиция", P + "KOM.html")
R(c, "musicology", "MA", "Музикознание; Музикознание - Етномузикознание", P + "all.html")
R(c, "music-education", "BA MA", "Педагогика на обучението по музика", P + "POM.html")
R(c, "music-production", "MA", "Музикално продуцентство", P + "MP.html")
R(c, "music-technology", "MA", "Тонрежисура", P + "TON.html")
R(c, "music-therapy", "MA", "Музикотерапия", P + "MT.html")
R(c, "arts-management", "MA", "Артмениджмънт", P + "ArtM.html")

c = "BG SOFIA13"; N = "https://nma.bg/priem/"; B, M, MS = N + "bakalavar/", N + "magistar-sled-bakalavar/", N + "magistar-sled-sredno-obrazovanie/"
R(c, "piano accordion guitar harp strings woodwind brass percussion vocal-opera", "BA", "Бакалавър: Пиано, Акордеон, Класическа китара, Арфа, Цигулка, Виола, Виолончело, Контрабас, духови и ударни инструменти, Класическо пеене", B)
R(c, "piano accordion guitar harp strings woodwind brass percussion vocal-opera", "MA", "Магистър след бакалавър: инструменти и Класическо пеене", M)
R(c, "jazz popular-music", "BA MA", "Поп и джаз (пеене, пиано, китара, бас, контрабас, саксофон, тромпет, цугтромбон, флейта, ударни)", B)
R(c, "folk", "BA MA", "Фолклорно пеене; Гайда, Гъдулка, Кавал, Тамбура", B)
R(c, "music-technology", "BA MA", "Звукорежисура, звуков и медиен дизайн; Звукорежисура и звуков дизайн за игри", B)
R(c, "conducting composition musicology music-theory", "MA", "Магистър след средно образование: Дирижиране, Композиция, Музикознание, Теория на музиката", MS)
R(c, "chamber-music", "MA", "Камерна музика", M)
R(c, "early-music", "MA", "Чембало", M)
R(c, "organ", "MA", "Орган", M)
R(c, "music-education", "MA", "Педагогика на обучението по музика; Инструментална педагогика – пиано; Вокална педагогика", M)
R(c, "arts-management", "MA", "Мениджмънт на музикалните индустрии", M)
R(c, "music-therapy", "MA", "Музикотерапия", M)

c = "HR PULA01"; P = "https://mapu.unipu.hr/mapu/studijski_programi/"
R(c, "music-education piano accordion vocal-opera", "BA", "Prijediplomski studij: Glazbena pedagogija, Klavir, Klasična harmonika, Solo pjevanje", P + "prijediplomski")
R(c, "music-education piano accordion vocal-opera", "MA", "Diplomski studij: Glazbena pedagogija, Klavir, Klasična harmonika, Solo pjevanje", P + "diplomski")

c = "HR ZAGREB01"; Z = "http://www.muza.unizg.hr/"; ZN = "Integrated university study (integrirani sveučilišni studij) leading to a Master's degree"
R(c, "conducting harp percussion", "MA", "Odsjek za dirigiranje, harfu i udaraljke", Z + "3-odsjek-za-dirigiranje-harfu-i-udaraljke/", ZN)
R(c, "woodwind brass", "MA", "Odsjek za duhačke instrumente", Z + "7-odsjek-za-duhacke-instrumente/", ZN)
R(c, "strings guitar", "MA", "Odsjek za gudačke instrumente i gitaru", Z + "6-odsjek-za-gudacke-instrumente-i-gitaru/", ZN)
R(c, "piano organ early-music", "MA", "Odsjek za klavir, orgulje i čembalo", Z + "5-odsjek-za-klavir-cembalo-i-orgulje/", ZN)
R(c, "composition music-theory", "MA", "Odsjek za kompoziciju i teoriju glazbe", Z + "1-odsjek-za-kompoziciju-i-teoriju-glazbe/", ZN)
R(c, "musicology", "MA", "Muzikologija", Z + "studiji/muzikologija/", ZN)
R(c, "vocal-opera", "MA", "Pjevanje", Z + "studiji/integrirani-sveucilisni-studij-pjevanje/", ZN)
R(c, "music-education", "MA", "Glazbena pedagogija", Z + "studiji/integrirani-sveucilisni-studij-glazbena-pedagogija/", ZN)
R(c, "folk", "MA", "Odsjek za glazbenu pedagogiju i tambure (tambura)", Z + "8-odsjek-za-glazbenu-pedagogiju/", ZN)

c = "CY NICOSIA24"; E = "https://euc.ac.cy/en/programs/"
R(c, "music-education composition", "MA", "Master in Music (online) – concentrations Music Education and Composition", E + "master-music-online/")
R(c, "church-music", "BA", "Bachelor in Byzantine Music – Psaltic Art (online)", E + "bachelor-byzantine-music-online/")

c = "CZ PRAHA04"; H = "https://www.hamu.cz/cs/katedry-programy/"
for dept, discs, name in [("katedra-bicich-nastroju", "percussion", "Katedra bicích nástrojů"), ("katedra-dechovych-nastroju", "woodwind brass", "Katedra dechových nástrojů"),
                          ("katedra-dirigovani", "conducting", "Katedra dirigování"), ("katedra-hudebni-produkce", "arts-management", "Katedra hudební produkce"),
                          ("katedra-hudebni-teorie", "music-theory", "Katedra hudební teorie"), ("katedra-jazzove-hudby", "jazz", "Katedra jazzové hudby"),
                          ("katedra-klavesovych-nastroju", "piano organ", "Katedra klávesových nástrojů"), ("katedra-skladby", "composition", "Katedra skladby"),
                          ("katedra-strunnych-nastroju", "strings guitar harp", "Katedra strunných nástrojů"), ("katedra-zpevu-a-operni-rezie", "vocal-opera", "Katedra zpěvu a operní režie"),
                          ("katedra-zvukove-tvorby-a-hudebni-rezie", "music-technology", "Katedra zvukové tvorby a hudební režie")]:
    for lv, slug, lname in [("BA", "bakalarske", "bakalářské"), ("MA", "magisterske", "magisterské"), ("Doc", "doktorske", "doktorské")]:
        R(c, discs, lv, f"{name} – {lname} studium", H + f"{dept}/prijimaci-rizeni/{slug}-studium/")
R(c, "chamber-music", "MA", "Oddělení komorní hry – magisterské studium", H + "oddeleni-komorni-hry/prijimaci-rizeni/magisterske-studium/")

c = "CZ BRNO03"; J = "https://hf.jamu.cz/studijni-obory/"
for discs, lv, name, slug in [
    ("conducting", "MA", "Dirigování orchestru; Dirigování sboru (MgA.)", "dirigovani-orchestru-5"),
    ("church-music", "BA", "Duchovní hudba (BcA.)", "duchovni-hudba-3"),
    ("early-music", "BA MA", "Historická interpretace (BcA., MgA.); Historical Performance (MgA.)", "historicka-interpretace-4"),
    ("percussion", "BA MA", "Hra na bicí nástroje", "hra-na-bici-nastroje-4"),
    ("woodwind", "BA MA", "Hra na flétnu, hoboj, klarinet, fagot", "hra-na-fletnu-5"),
    ("brass", "BA MA", "Hra na lesní roh, trubku, trombon, tubu", "hra-na-trubku-4"),
    ("strings", "BA MA", "Hra na housle, violu, violoncello, kontrabas", "hra-na-housle-5"),
    ("guitar", "BA MA", "Hra na kytaru", "hra-na-kytaru-4"),
    ("organ", "BA MA", "Hra na varhany", "hra-na-varhany-4"),
    ("piano", "MA", "Hra na klavír a komorní hra; Hra na klavír a klavírní pedagogika (MgA.)", "hra-na-klavir-a-komorni-hra-2"),
    ("chamber-music", "MA", "Hra na klavír a komorní hra (MgA.)", "hra-na-klavir-a-komorni-hra-2"),
    ("music-education", "BA", "Klavírní pedagogika; Pedagogika klavírní hry (BcA.)", "klavirni-pedagogika-4"),
    ("music-education", "MA", "Hra na klavír a klavírní pedagogika (MgA.)", "hra-na-klavir-a-klavirni-pedagogika-3"),
    ("arts-management", "BA MA", "Hudební produkce (BcA., MgA.)", "hudebni-produkce-6"),
    ("arts-management", "Doc", "Hudební produkce (Ph.D.)", "hudebni-produkce-5"),
    ("jazz", "BA MA", "Jazzová interpretace; Jazzová kompozice a aranžování", "jazzova-interpretace-4"),
    ("composition", "MA", "Kompozice; Kompozice scénické a filmové hudby (MgA.)", "kompozice-4"),
    ("composition", "Doc", "Kompozice a teorie kompozice (Ph.D.)", "kompozice-a-teorie-kompozice-4"),
    ("music-technology", "MA", "Kompozice elektroakustické hudby (MgA.)", "kompozice-elektroakusticke-hudby-2"),
    ("music-technology", "BA MA", "Multimediální tvorba", "multimedialni-tvorba-2"),
    ("vocal-opera", "MA", "Zpěv (MgA.)", "zpev-6")]:
    R(c, discs, lv, name, J + slug + "/")

c = "DK KOBENHA09"; D = "https://www.dkdm.dk/da/"
for lv in ("BA", "MA"):
    A(I, c, D + "uddannelsesretninger", r"/da/education/", drop=r"operaakademiet", default_level=lv)
R(c, "vocal-opera", "MA", "Operaakademiet", D + "education/operaakademiet")
R(c, "music-education", "BA MA", "AM-uddannelsen (Almen Musiklærer)", D + "am-uddannelsen")

c = "DK KOBENHA39"; RM = "https://www.rmc.dk/da/uddannelse/"; RN = "Rhythmic music conservatory: jazz, pop, rock and related styles"
R(c, "jazz popular-music", "BA", "Bachelor Performance – Instrumental / Vokal", RM + "performance-instrumental-vokal", RN)
R(c, "jazz popular-music", "MA", "Kandidat Music Performance; Nordic Master: The Composing Musician", RM + "music-performance", RN)
R(c, "popular-music", "BA", "Bachelor Performance – Sangskrivning", RM + "performance-sangskrivning")
R(c, "composition", "BA", "Bachelor Komposition", RM + "komposition")
R(c, "composition", "MA", "Kandidat Music Creation", RM + "music-creation")
R(c, "music-production", "BA", "Bachelor Musikproduktion", RM + "musikproduktion")
R(c, "arts-management", "BA", "Bachelor Music Management", RM + "music-management")
R(c, "music-education", "MA", "Kandidat Music Education", RM + "music-education")

c = "DK ODENSE22"; SD = "https://www.sdmk.dk/uddannelser/uddannelsesretninger"
R(c, "music-technology", "BA MA", "Elektronisk musik og lydkunst", SD)
R(c, "folk", "BA MA", "Folkemusiker", SD)
R(c, "church-music organ", "BA MA", "Kirkemusiker", SD)
R(c, "piano strings percussion vocal-opera", "BA MA", "Klassisk musiker/sanger (e.g. klaver, violin, slagtøj, sang)", SD)
R(c, "jazz popular-music", "BA MA", "Rytmisk musiker", SD)
R(c, "music-education", "BA MA", "Musiker og musikpædagog", SD)
R(c, "composition", "MA", "Filmkomponist; Rytmisk musiker og komponist", SD)

c = "DK ARHUS05"; AU = "https://musikkons.dk/uddannelser/"
for discs, name, slug in [("guitar", "Guitar", "klassisk/guitar/"), ("piano", "Klaver", "klassisk/klaver/"), ("conducting", "Korledelse; Rytmisk korledelse", "klassisk/korledelse/"),
                          ("brass", "Messingblæsere", "klassisk/messingblaesere/"), ("woodwind", "Træblæsere", "klassisk/traeblaesere/"), ("strings", "Strygeinstrumenter", "klassisk/strygeinstrumenter/"),
                          ("percussion", "Slagtøj", "klassisk/slagtoej/"), ("vocal-opera", "Sang", "klassisk/sang/"), ("organ church-music", "Orgel/Kirkemusik", "klassisk/orgel-kirkemusik/"),
                          ("music-theory", "Musikteori; Hørelære", "klassisk/musikteori/"), ("music-education", "AM – Almen Musikledelse", "klassisk/am-almen-musikledelse/"),
                          ("jazz popular-music", "RM – Rytmisk musik (Aarhus, Aalborg, Holstebro); NOMAZZ", "rytmisk/rm-rytmisk-musik-aarhus/"),
                          ("composition", "Klassisk, rytmisk og elektronisk komposition", "elektronisk/komposition/"),
                          ("popular-music", "Sangskrivning", "elektronisk/sangskrivning/"),
                          ("music-technology music-production", "Elektronisk Musik og Musikproduktion (Aalborg)", "elektronisk/elektronisk-musik-og-musikproduktion-aalborg/")]:
    R(c, discs, "BA MA", name, AU + slug)

c = "EE TALLINN03"; O = "https://ois.eamt.ee/oppekava/public?language=en&versioon=2026&aste="
R(c, "piano accordion guitar harp organ strings woodwind brass percussion vocal-opera", "BA MA", "Classical Music Performance (piano, accordion, classical guitar, harp, organ, strings, winds, percussion, vocal)", O + "B")
R(c, "early-music", "BA", "Classical Music Performance – harpsichord", O + "B")
R(c, "early-music", "MA", "Classical Music Performance – early music performance, harpsichord", O + "M")
R(c, "folk", "BA MA", "Classical Music Performance – zither", O + "B")
R(c, "chamber-music", "MA", "Classical Music Performance – chamber ensemble", O + "M")
R(c, "conducting", "BA", "Choral conducting", O + "B")
R(c, "conducting", "MA", "Choral, orchestral and wind orchestra conducting", O + "M")
R(c, "jazz", "BA", "Jazz Studies", O + "B")
R(c, "jazz", "MA", "Jazz and Improvisational Music", O + "M")
R(c, "composition", "BA MA", "Composition and Multimedia / Composition and Music Technology (classical, audio-visual, electroacoustic composition)", O + "B")
R(c, "music-technology music-production", "BA", "Sound Engineering and Music Production; recording arts", O + "B")
R(c, "music-technology", "MA", "Composition and Music Technology – recording arts", O + "M")
R(c, "musicology", "BA MA", "Music Culture (BA); Musicology (MA)", "https://eamt.ee/en/departments/musicology/musicology/")
R(c, "music-education", "BA MA", "Music Pedagogy; Instrumental and Vocal Pedagogy", "https://eamt.ee/en/departments/musicology/instrumental-and-vocal-pedagogy/")
R(c, "arts-management", "MA", "Cultural Management", "https://eamt.ee/en/departments/musicology/cultural-management/")

c = "EE TARTU02"; VB, VM = "https://kultuur.ut.ee/en/content/bachelors", "https://kultuur.ut.ee/en/content/masters"
R(c, "folk", "BA", "Music curriculum – traditional music specialisation", VB)
R(c, "music-education", "BA", "Music curriculum – school music specialisation (incl. musical instrument teacher)", VB)
R(c, "popular-music", "BA", "Music curriculum – rhythm music specialisation", VB)
R(c, "music-production", "BA", "Music curriculum – rhythm music, music producer direction", VB)
R(c, "music-technology", "BA", "Music curriculum – sound engineering specialisation", VB)
R(c, "arts-management", "BA", "Culture Management curriculum", VB)
R(c, "folk", "MA", "Creative Applications of Cultural Heritage – traditional music specialisation", VM)
R(c, "music-education", "MA", "Teacher of Arts and Technology (incl. teacher of a musical instrument)", VM)

METHOD = "Field-level collection as in batch 1 (raw HTML of each institution's own programme pages, PDFs where the list was only there; names mapped to disciplines.json by keyword and checked by hand)."
NOTES = {
    "BG SOFIA02": "The Music Department lists the programmes Musical Performance (in Bulgarian and in English) and Musical, but its pages do not name the instruments, fields or degree levels.",
}

# Erätiedosto add_programmes.py:lle
BATCH = {"collected": "2026-10-08", "method": METHOD, "institutions": I, "notes": NOTES}
out = os.path.join(os.path.dirname(__file__), "..", "..", "data", "programmes_batches", "02.json")
json.dump(BATCH, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print({k: len(v) for k, v in I.items()})
