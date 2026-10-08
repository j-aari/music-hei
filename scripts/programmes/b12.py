# Erä 12: Norja, Puola (aja: python scripts/programmes/b12.py, sitten python scripts/add_programmes.py data/programmes_batches/12.json). Apufunktio R(alat, tasot, nimi, url, huom) laajentaa rivit.
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

c = "N  OSLO66"; BD = "https://barrattdue.no/studier/hoyere-utdanning/"
R(c, CL, "BA", "Bachelor i utøvende musikk", BD + "bachelor-i-utovende-musikk/", CLN)
R(c, CL, "MA", "Master i utøvende musikk", BD + "master-i-utovende-musikk/", CLN)
c = "N  TRONDHE01"; NT = "https://www.ntnu.edu/studies/"
R(c, CL, "BA MA", "Music Performance Studies (bachelor, classical 4 years); Music Performance (master, classical or jazz)", NT + "bmusp/music-performance-studies-bachelor-s-programme", CLN)
R(c, "jazz", "BA MA", "Music Performance Studies – jazz (bachelor 3 years); Music Performance – jazz (master)", NT + "mmusp/music-performance-studies-master-s-programme")
R(c, "music-technology", "BA MA", "Music Technology (bachelor); Creative Music Technology (master); Music, Communication and Technology (master)", NT + "bmust")
R(c, "musicology", "BA MA", "Musicology (bachelor, master)", NT + "bmusv")
c = "N  KRISTIA01"; UA = "https://www.uia.no/studier/program/"
R(c, "jazz popular-music", "BA", "Utøvende musikk – rytmisk (Bachelor): utøvende rytmisk; låtskriver og artist", UA + "utovende-musikk-rytmisk-bachelor/")
R(c, CL, "BA", "Utøvende musikk – klassisk (Bachelor)", UA + "utovende-musikk-klassisk-bachelor/", CLN)
R(c, CL + " conducting chamber-music", "MA", "Utøvende musikk – klassisk (Master): ensemblesang, orkesterakademi, klaver i samspill, korledelse", UA + "utovende-musikk-klassisk-master-2-ar/", CLN)
R(c, "popular-music music-technology global-music arts-management", "MA", "Rytmisk musikk (Master): Performing Music, Electronic Music, World Music, Songwriting, Music Business and Management", UA + "rytmisk-musikk-master-2-ar/")
c = "N  STAVANG01"; US = "https://www.uis.no/"
R(c, CL + " jazz church-music conducting", "BA", "Bachelor i utøvende musikk: klassisk, jazz/improvisasjon, kirkemusikk, dirigering", US + "nb/studier/utovende-musikk-bachelor", CLN)
R(c, CL + " jazz conducting", "MA", "Master in Music Performance: conducting, classical music, jazz and improvisation", US + "en/studies/master-music-performance", CLN)
c = "N  OSLO07"
R(c, "vocal-opera", "MA", "Master's Programme in Opera", "https://khio.no/en/study-programmes/maop")
c = "N  TROMSO01"; UT = "https://uit.no/utdanning/program/"
R(c, CL + " jazz popular-music", "BA MA", "Musikkutøving (bachelor, master): klassisk og rytmisk sjanger", UT + "280865/musikkutoving_-_bachelor", CLN)
c = "N  BERGEN12"; NL = "https://www.nla.no/studier/studieprogram/"
R(c, "popular-music", "BA MA", "Utøvende rytmisk musikk (bachelor, master)", NL + "master-i-utovende-rytmisk-musikk/")
R(c, "music-production composition", "BA", "Musikkskaping – låtskriving, produksjon og live", NL + "bachelor-i-musikkskaping-latskriving-produksjon-og-live/")
R(c, "church-music conducting", "BA", "Musikk, menighet og ledelse / utøvende musikk", NL + "bachelor-i-musikk-menighet-og-ledelse")
c = "N  OSLO58"
R(c, "popular-music music-production music-technology", "BA", "Bachelor i musikk: Musiker og artist; Låtskriving og produksjon; Konsertlyd og studioproduksjon", "https://www.kristiania.no/studier/bachelor/musikk/")
c = "N  BERGEN01"; GR = "https://www.uib.no/grieg/"
R(c, CL + " jazz folk composition", "BA MA", "Bachelor / Master i utøvende musikk eller komposisjon (klassisk, jazz, folkemusikk, komposisjon)", GR + "24484/master-i-ut%C3%B8vende-musikk-eller-komposisjon", CLN)
R(c, "musicology", "BA", "Bachelor i musikkvitenskap", "https://kmd.uib.no/no/studier/griegakademiet-institutt-for-musikk")
R(c, "music-therapy", "MA", "Integrert masterprogram i musikkterapi", GR + "24761/integrert-masterprogram-i-musikkterapi")
c = "N  KONGSBE02"
R(c, "folk", "BA", "Bachelor i folkemusikk", "https://www.usn.no/studier/bachelor-i-folkemusikk/")
R(c, "folk", "MA", "Master i tradisjonskunst og folkemusikk", "https://www.usn.no/studier/master-i-tradisjonskunst-og-folkemusikk/")

PI = "strings woodwind brass percussion piano organ guitar harp accordion"
c = "PL BYDGOSZ04"; BY = "https://www.amuz.bydgoszcz.pl/"
R(c, PI, "BA MA", "Instrumentalistyka (I i II stopień)", BY + "drugi-nabor-na-studia-i-i-ii-stopnia/")
R(c, "jazz popular-music", "BA MA", "Jazz i muzyka estradowa: instrumentalistyka jazzowa, wokalistyka jazzowa, singer-songwriter", "https://www.rekrutacja.amuz.bydgoszcz.pl/pl/offer/Rekrutacja_2026/programme/SP-JME-W/?from=org-unit%3A40")
R(c, "composition music-theory music-technology", "BA MA", "Kompozycja i teoria muzyki; reżyseria dźwięku", BY + "dla-kandydata/informatoramfn/w4/")
R(c, "music-education conducting church-music", "BA MA", "Edukacja artystyczna w zakresie sztuki muzycznej (dyrygentura chóralna, muzyka kościelna)", BY + "dla-kandydata/informatoramfn/w4/")
R(c, "vocal-opera", "BA MA", "Wokalistyka (Wydział Wokalno-Aktorski)", "https://www.usosweb.amuz.bydgoszcz.pl/kontroler.php?_action=katalog2/programy/pokazProgram&prg_kod=SP-W")
c = "PL LODZ04"; LO = "https://www.amuz.lodz.pl/index.php/pl/"
R(c, "jazz popular-music", "BA MA", "Jazz i muzyka estradowa: instrumenty jazzowe, wokalistyka jazzowa i estradowa", LO + "home/oferta-dydaktyczna/instytut-wokalistyki-jazzowej-i-estradowej/wokalistyka-jazzowa")
R(c, PI, "BA MA", "Instrumentalistyka", "http://www.amuz.lodz.pl/en/14-dla-kandydata/149721-instrumentalistyka-studia-stacjonarne-ii-stopnia-1")
R(c, "vocal-opera", "BA MA", "Wokalistyka", "http://www.amuz.lodz.pl/en/14-dla-kandydata/149732-wokalistyka-studia-stacjonarne-ii-stopnia-1")
c = "PL POZNAN06"; PZ = "https://amuz.edu.pl/wp-content/uploads/informator-PL-2025-2026.pdf"
R(c, PI, "BA MA", "Instrumentalistyka (fortepian, organy, akordeon, dęte, smyczkowe, harfa, gitara)", PZ)
R(c, "early-music", "BA MA", "Wykonawstwo historyczne", "https://amuz.edu.pl/nowa-struktura-uczelni/wydzial-instrumentalistyki-jazzu-i-muzyki-estradowej/charakterystyka-wydzialu/instytut-instrumentalistyki/")
R(c, "jazz", "BA MA", "Jazz i muzyka estradowa (instrumenty, wokalistyka jazzowa, kompozycja z aranżacją)", PZ)
R(c, "composition music-theory music-technology", "BA MA", "Kompozycja i teoria muzyki (muzyka filmowa i teatralna, kompozycja elektroakustyczna)", PZ)
R(c, "conducting", "BA MA", "Dyrygentura (symfoniczna, operowa, chóralna, orkiestr dętych)", PZ)
R(c, "vocal-opera", "BA MA", "Wokalistyka (śpiew solowy, śpiew musicalowy)", PZ)
R(c, "music-education", "BA MA", "Edukacja artystyczna w zakresie sztuki muzycznej", PZ)
c = "PL WROCLAW06"; WR = "https://amuz.wroc.pl/"
R(c, PI + " early-music", "BA MA", "Instrumentalistyka (klawiszowe, smyczkowe, dęte, dawne, gitara, harfa, akordeon, perkusja)", WR + "dla-kandydata/slowo-jm-rektora/studiuj-u-nas-1/kierunki-studiow/instrumentalistyka/klarnet")
R(c, "jazz", "BA MA", "Jazz i muzyka estradowa", WR + "uczelnia/struktura/wydzialy-1/wydzial-muzyki-jazzowej-1")
R(c, "vocal-opera", "BA MA", "Wokalistyka", WR + "zakresy-egzaminow-wstepnych-5530")
R(c, "composition music-theory music-therapy", "BA MA", "Kompozycja i teoria muzyki (kompozycja, teoria muzyki, muzykoterapia)", WR + "kompozycja-4086")
c = "PL KATOWIC04"; KA = "https://am.katowice.pl/"
R(c, "jazz popular-music", "BA MA", "Jazz i muzyka estradowa: instrumentalistyka jazzowa, wokalistyka jazzowa i estradowa, kompozycja i aranżacja", KA + "informacje/informacje-o-kierunkach-struktura-przedmiotu-1224")
KL = KA + "informacje/informacja-o-instytucji-lista-oferowanych-kierunkow-1208"
R(c, PI, "BA MA", "Instrumentalistyka", KL)
R(c, "vocal-opera", "BA MA", "Wokalistyka", KL)
R(c, "composition conducting music-theory", "BA MA", "Kompozycja, dyrygentura i teoria muzyki (dyrygentura chóralna, symfoniczno-operowa)", KL)
R(c, "music-education", "BA MA", "Edukacja artystyczna w zakresie sztuki muzycznej", KL)
R(c, "music-technology", "BA", "Realizacja nagłośnienia (studia niestacjonarne)", KA + "akademia/informacje/wydzial-jazzu-i-muzyki-rozrywkowej-149")
c = "PL KRAKOW09"; KR = "https://www.amuz.krakow.pl/en/kandydaci/rekrutacja/"
R(c, PI + " early-music chamber-music", "BA MA", "Instrumentalistyka (piano, organ, early music instruments, guitar, harp, strings, winds, accordion, brass, percussion, chamber music)", KR)
R(c, "jazz", "BA MA", "Jazz i muzyka improwizowana", KR + "jazz-i-muzyka-improwizowana/")
R(c, "composition music-theory", "BA MA", "Kompozycja i teoria muzyki", KR)
R(c, "conducting", "BA MA", "Dyrygentura (chóralna, orkiestr dętych)", KR)
R(c, "music-education church-music vocal-opera", "BA MA", "Edukacja artystyczna; Muzyka kościelna; Wokalistyka", KR)
c = "PL GDANSK04"; GD = "https://amuz.gda.pl/"
R(c, "jazz popular-music", "BA MA", "Jazz i muzyka estradowa: wokalistyka jazzowa, instrumentalistyka jazzowa, kompozycja i aranżacja jazzowa", GD + "wydzialy/wydzial-iv-dyrygentury-choralnej-muzyki-koscielnej-edukacji-artystycznej-rytmiki-i-jazzu/kierunki-i-specjalnosci,680")
R(c, "composition music-theory", "BA MA", "Kompozycja i teoria muzyki (kompozycja klasyczna, muzyka filmowa, gier i mediów, teoria muzyki)", GD + "rekrutacja-2021-2022/o-wydzialach/wydzial-iv/kierunki-i-specjalnosci/kompozycja-i-aranzacja-jazzowa,748")
R(c, "conducting church-music music-education", "BA MA", "Wydział IV: dyrygentura chóralna, muzyka kościelna, edukacja artystyczna, rytmika", GD + "wydzialy/wydzial-iv-dyrygentury-choralnej-muzyki-koscielnej-edukacji-artystycznej-rytmiki-i-jazzu/kierunki-i-specjalnosci,680")
c = "PL WARSZAW09"; CH = "https://usosweb.chopin.edu.pl/kontroler.php?_action=katalog2%2Fprogramy%2FwszystkieKierunki"
R(c, PI, "BA MA", "Instrumentalistyka", CH)
R(c, "early-music", "BA MA", "Instrumentalistyka – muzyka dawna (traverso, viola da gamba, teorba, trąbka naturalna, skrzypce historyczne)", CH)
R(c, "jazz global-music", "BA MA", "Jazz i muzyka estradowa: jazz; jazz i world music", CH)
R(c, "music-technology", "BA MA", "Reżyseria dźwięku (film i telewizja, reżyseria muzyczna, multimedia)", "https://usosweb.chopin.edu.pl/kontroler.php?_action=katalog2%2Fprogramy%2FpokazProgram&prg_kod=RD-RM-SM")

METHOD = "Field-level collection as in batch 1; where a site lists programmes only via JavaScript, the programme pages were located with a web search restricted to the institution's own domain (raw HTML of each institution's own programme pages, PDFs where the list was only there; names mapped to disciplines.json by keyword and checked by hand)."
NOTES = {}

# ErÃ¤tiedosto add_programmes.py:lle
BATCH = {"collected": "2026-10-08", "method": METHOD, "institutions": I, "notes": NOTES}
out = os.path.join(os.path.dirname(__file__), "..", "..", "data", "programmes_batches", "12.json")
json.dump(BATCH, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print({k: len(v) for k, v in I.items()})
