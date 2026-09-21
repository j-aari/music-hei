# Euroopan musiikkikorkeakoulut — projektibrief

## Mitä rakennetaan

Staattinen verkkosivu, joka listaa Euroopan musiikkialan korkeakoulut, jotka
ovat Erasmus-peruskirjan (ECHE) haltijoita. Sivulla on kartta- ja listanäkymä,
suodattimet ja CSV-vienti. Sivu jaetaan linkillä; ei kirjautumista, ei
käyttäjätilejä.

Kohdeyleisö: korkeakoulujen kansainvälisten asioiden koordinaattorit ja
musiikkialan opiskelijat, jotka etsivät vaihtokohdetta.

Sivun tehtävä yhdellä lauseella: vastata kysymykseen "mitkä musiikkikorkeakoulut
Euroopassa ovat olemassa, missä ne ovat, ja mitkä niistä ovat meidän
partnereitamme".

## Teknologia

- Python-skripti datan hakuun ja käsittelyyn (ajetaan käsin, ei ajastettuna)
- Skripti kirjoittaa yhden staattisen JSON-tiedoston
- Staattinen HTML + vanilla JS + CSS, ei build-työkalua
- Kartta: Leaflet + OpenStreetMap-tiilet (ei API-avainta, ei kustannuksia)
- Julkaisu: Netlify tai GitHub Pages

**Muistutus:** lopputulos on julkinen staattinen verkkosivu, joka avataan
selaimella myös muilta koneilta. Kaikki mikä vaatii paikallista Pythonia kuuluu
rakennusvaiheeseen, ei sivulle: sivu ei saa riippua paikallisista skripteistä,
palvelimesta tai tiedostoista, jotka ovat vain tällä koneella.

**Älä rakenna:** palvelinta, tietokantaa tuotantoon, käyttäjähallintaa,
React/Next.js-sovellusta, ajastettua taustaprosessia. Datajoukko on muutamia
satoja rivejä. Kaikki suodatus tapahtuu selaimessa ladatusta JSON-tiedostosta.

## Datalähteet

| Lähde | Käyttö | Osoite |
|---|---|---|
| ECHE List API | ECHE-haltijoiden perustiedot | `https://eche-list.erasmuswithoutpaper.eu/api` |
| OpenAPI-spec | Kenttien tarkat nimet — **lue tämä ensin** | `https://eche-list.erasmuswithoutpaper.eu/openapi` |
| GitHub-repo | Datan käsittelylogiikan dokumentaatio | `EuropeanUniversityFoundation/eche-api` |
| Nominatim | Geokoodaus (kertaluontoinen) | OpenStreetMap |

Lähdetiedosto rajapinnan takana on komission julkaisema akkreditoitujen
korkeakoulujen lista. Tarkista kenttien nimet spesifikaatiosta äläkä oleta
niitä — erityisesti OID:n kohdalla.

Geokoodaus ajetaan **kerran** ja tulos tallennetaan JSON-tiedostoon. Kunnioita
Nominatimin käyttöehtoja: yksi pyyntö sekunnissa, tunnistautuva User-Agent.
Älä koskaan geokoodaa selaimessa ajonaikana.

## Arkkitehtuuri — tärkein päätös

Data on **kahdessa erillisessä kerroksessa**, jotka yhdistetään vasta
näyttövaiheessa Erasmus-koodin perusteella.

```
data/
  upstream.json     # ECHE-rajapinnasta. YLIKIRJOITETAAN kokonaan päivityksessä.
  annotations.json  # Omat merkinnät. EI KOSKAAN kirjoiteta automaattisesti.
  site.json         # Näiden yhdiste. Generoitu. Tämä ladataan sivulle.
```

`annotations.json` sisältää:

```json
{
  "FI HELSINK59": {
    "is_music_institution": true,
    "classification_note": "Taideyliopiston Sibelius-Akatemia",
    "partner_of_siba": true,
    "languages_of_instruction": ["fi", "sv", "en"],
    "notes": ""
  }
}
```

Päivitysskripti hakee upstreamin uudelleen, vertaa vanhaan ja **raportoi
muutokset** ennen kuin kirjoittaa mitään: uudet laitokset, poistuneet
laitokset, nimenmuutokset. Poistuneiden annotaatioita ei saa hävittää
automaattisesti, vaan ne siirretään `orphaned`-osioon tarkistettavaksi.

Tämä on se kohta, joka menee pieleen jos sen ohittaa. Komission lista päivittyy,
ja ilman tätä erottelua koko luokittelutyö katoaa kerralla.

## Kentät

Jokaisesta laitoksesta sivulla:

- Nimi (virallinen) ja tarvittaessa englanninkielinen nimi
- Maa ja kaupunki
- Osoite
- Erasmus-koodi
- OID
- Verkkosivu (linkkinä)
- Opetuskieli / -kielet
- Laitostyyppi (itsenäinen konservatorio / taideyliopiston yksikkö / yleisyliopiston laitos)
- Partneristatus
- Koordinaatit (vain kartalle, ei näytetä)

## Musiikkikorkeakoulujen tunnistaminen

ECHE-listassa **ei ole alakenttää**. Suodatus tehdään kolmessa kerroksessa ja
tulos tallennetaan `annotations.json`-tiedostoon, ei johdeta ajonaikana.

1. **Nimihaku.** Conservatorio, Conservatoire, Conservatorium, Konservatorium,
   Musikhochschule, Academy of Music, Muziekhogeschool, Accademia musicale,
   Academia de Música, Muzyczna, Zeneakadémia, Hudební. Nämä ovat lähes aina
   osumia.
2. **Ristiinajo AEC:n jäsenlistaa vasten.** Kattaa valtaosan varsinaisista
   musiikkikorkeakouluista.
3. **Rajatapaukset käsin.** Monialaiset taideyliopistot ja yleisyliopistot,
   joissa on musiikin laitos. Kielimalli voi ehdottaa luokittelua verkkosivun
   perusteella, mutta päätös kirjataan käsin. Tämä on tulkintakysymys, ei
   tekninen ongelma.

### Kolmiportainen luokittelu

Laitokset jaetaan kolmeen tasoon sen mukaan, missä musiikki sijaitsee. Taso
tallennetaan `annotations.json`-tiedostoon laitostyyppinä.

1. **Itsenäinen musiikkikorkeakoulu** (esim. konservatorio, Musikhochschule).
2. **Taideyliopiston musiikkiyksikkö** (esim. Taideyliopisto / Sibelius-Akatemia,
   Folkwang, Hogeschool voor de Kunsten).
3. **Yleisyliopiston musiikkiyksikkö** (musiikin laitos tai osasto
   yleisyliopiston sisällä).

**Tasot 1 ja 2 toteutetaan nyt. Taso 3 tehdään myöhemmin omana kierroksenaan**
eikä kuulu vaiheisiin 2–5. Rajatapaukset, joissa on epäselvää onko musiikki
itsenäinen yksikkö vai osa yleisyliopistoa, merkitään tasolle 3 ja jätetään
toistaiseksi pois.

**Taso määräytyy rakenteesta, ei maasta.** Ratkaisevaa on emo-organisaation
luonne: jos musiikki kuuluu taidekorkeakouluun (taideyliopisto tai muu
taiteisiin keskittynyt korkeakoulu), kyseessä on taso 2; jos emo-organisaatio
on monialainen yleisyliopisto, kyseessä on taso 3. Maa ei koskaan yksin
ratkaise tasoa, vaan jokainen laitos arvioidaan itse.

Esimerkki: Kreikassa kaikki tunnetut musiikkikoulutuksen tapaukset osuvat
tasolle 3, koska musiikki on yleisyliopistojen sisällä. Tämä on havainto
nykyisestä tilanteesta, ei sääntö: jos Kreikassa olisi taidekorkeakoulun
musiikkiyksikkö, se olisi taso 2.

Ankara Music and Fine Arts University ja Mimar Sinan Fine Arts University ovat
tasoa 2: emo-organisaatio on taidekorkeakoulu.

**Laitoksen asemaa ei arvioida.** ECHE-haltijuus tarkoittaa kansallisen
viranomaisen tunnustusta korkeakouluksi, joten sitä, onko laitos oikea
korkeakoulu, ei tarvitse erikseen selvittää. Ainoa kysymys on kuuluuko laitos
musiikkiin.

**Oikeushenkilön nimi voi poiketa oppilaitoksen nimestä**, erityisesti
Italiassa ja Espanjassa (srl, SL, fundació). Esimerkiksi *Saint Louis Music
Center Srl* on Saint Louis College of Music ja *Mussida Music Publishing srl* on
CPM Music Institute. Nimihaku voi siis osua yritysmuotoon tai ohittaa
oppilaitoksen kokonaan: tarkista oppilaitoksen oma nimi ja kirjaa se
`annotations.json`:n `notes`-kenttään, kun se poikkeaa ECHE-listan nimestä.

Tasolla 2 laitoksen musiikkitarjonta voi olla suppea (esim. vain laulu ja
oopperakoulutus). Se kirjataan `classification_note`-kenttään, ja laitos pysyy
silti tasolla 2.

Sivulla on oltava näkyvissä käytetty rajanveto, esimerkiksi: *"Mukana laitokset,
joissa musiikki on itsenäinen tutkintoa myöntävä yksikkö."* Kun vain tasot 1 ja 2
on tehty, rajanvedon pitää sanoa myös, ettei yleisyliopistojen musiikkiyksiköitä
ole vielä mukana (esim. *"…tai taideyliopiston musiikkiyksikkö. Yleisyliopistojen
musiikin laitokset eivät ole vielä mukana."*). Tämä on väite, joka
pitää pystyä puolustamaan, ja sen näyttäminen tekee sivusta uskottavan.

Rajausteksti on **aikasidonnainen**, ei ikuinen väite. Lista on ECHE-haltijat
tietyllä hakupäivällä, ja Britannia ja Sveitsi assosioituvat Erasmus+
-ohjelmaan 1.1.2027 alkaen ja ilmestyvät listalle vasta, kun ne saavat ECHE:n.
Tekstin pitää siis kertoa hakupäivä ja se, että Britannian ja Sveitsin laitokset
puuttuvat tästä syystä eivätkä siksi, että ne olisi rajattu pois. Esimerkiksi:
*"Tiedot haettu <pvm> Euroopan komission ECHE-listasta. Britannian ja Sveitsin
laitokset lisätään, kun ne ovat saaneet ECHE:n (assosiaatio Erasmus+
-ohjelmaan 1.1.2027 alkaen)."* Hakupäivä kirjoitetaan `site.json`:iin
generointivaiheessa, ei käsin sivulle. Nimihaun sanalistassa on Britannian ja
Sveitsin muodot valmiina, jotta uudet laitokset löytyvät päivityksessä.

## Käyttöliittymä

**Kaksi näkymää, yksi suodatintila.** Kartta ja lista näyttävät aina saman
suodatetun joukon. Vaihto yhdellä napilla. Suodattimen muutos ei nollaa
näkymävalintaa.

**Suodattimet näkyvissä**, eivät pudotusvalikoissa piilossa. Jokaisessa
lukumäärä, jotta käyttäjä näkee heti valinnan koon: maa, opetuskieli,
laitostyyppi, partneristatus.

**Yksityiskohdat sivupaneeliin**, ei uudelle sivulle. Paneeli aukeaa
klikkauksesta kartalla tai listassa.

**CSV-vienti** vie aina sen hetkisen suodatetun joukon, ei koko aineistoa.
Napin teksti kertoo mitä tapahtuu ja montako riviä viedään.

**Tyhjä tulos** on ohje, ei virhe: kerro mikä suodatin rajaa liikaa ja tarjoa
sen poistamista.

Kartta on orientaatiota varten. Kun käyttäjä etsii tarkkaa joukkoa, lista on
oikea työkalu — älä yritä tehdä kartasta ensisijaista käyttöliittymää.

## Visuaalinen suunta

Aihe on eurooppalainen musiikkikoulutus. Sen oma visuaalinen kieli on
konserttiohjelma: hillitty, typografiavetoinen, runsaat marginaalit, laitosten
nimet kannattelevat sivua. Käytä tätä lähtökohtana — älä korkeakoulutilastojen
tai SaaS-dashboardin kieltä.

Yksi periaate, jota kannattaa noudattaa tiukasti: **väri kantaa merkitystä**.
Koko paletti on hillitty, ja ainoa kylläinen väri sivulla merkitsee
partneristatusta. Näin kartalta näkee yhdellä silmäyksellä oman verkoston, ilman
selitettä.

Typografiassa: harkittu leikkaus laitosten nimille ja neutraali groteski
datalle. Älä käytä Interiä. Vältä versaaleja pikkuotsikoita, yhden sanan
korostamista otsikossa ja numeroituja merkkejä (01 / 02) sisällölle joka ei ole
sarja.

Tee ennen koodaamista lyhyt suunnitelma — paletti neljästä kuuteen nimettyä
hex-arvoa, kirjasinvalinnat rooleineen, asettelukonsepti — ja arvioi se
kriittisesti: onko tämä valinta tälle aiheelle vai oletusarvo, jonka tekisit
mille tahansa sivulle. Vasta sen jälkeen koodi.

Perustaso ilman erillistä mainintaa: responsiivinen mobiiliin asti, näkyvä
näppäimistöfokus, `prefers-reduced-motion` huomioitu, riittävät kontrastit.

### Toteutetut päätökset (vaihe 6)

- **Kieli:** sivun tekstit ovat englanniksi, laitosten nimet alkuperäiskielellä. Otsikko:
  *European Music Institutions with an Erasmus Charter*.
- **Paletti:** viileä paperi (Frost `#F0F3F8`, Night Ink `#0F1620`, Slate `#4B545F`, Mist
  `#C8D0DA`, Fog `#E4E9F0`), yksi kylläinen väri, Vermilion `#C2331F`, joka merkitsee vain
  vaihtokumppania. Lämmin kerma + antiikva + punaoranssi on tekoälysivujen oletuspaletti, ja
  viileä tausta erottaa punaisen selvemmin. Taso erotetaan muodolla (täytetty piste / rengas),
  ei värillä. OSM-tiilet harmaasävyistetään CSS-suodattimella, jotta punainen pysyy merkityksellisenä.
  Lisäksi yksi sininen, Link Blue `#1D4ED8`, vain linkeille (verkkosivuosoitteet ja ulkoiset
  linkit); sitä ei käytetä painikkeissa, suodattimissa eikä kartalla.
- **Kirjasimet:** Newsreader (laitosten nimet, otsikot) ja Public Sans (data, käyttöliittymä),
  omalta palvelimelta (`site/fonts/`, OFL). Leaflet on omalta palvelimelta (`site/vendor/`).
- **Partneritieto:** kenttä `partner_of_siba` säilyy, ja sivu kertoo aina lähteen: partneritiedot
  ovat Taideyliopiston julkaisemasta vaihtokohdelistasta. Sivulla on myös vastuulauseke: se ei ole
  virallinen julkaisu. Kielen ja partnerin suodattimet piilotetaan, kunnes dataa on; sivulla on
  siihen asti rehellinen rivi "not recorded yet".
- **Annotaatiokentät sivulle:** `public_note` (englanniksi) näytetään sivulla; `classification_note`
  ja `notes` ovat sisäisiä eikä niitä viedä `site.json`:iin. `display_name` ohittaa siistityn nimen
  (diakriittien korjaus). Lista laitoksista, joiden nimestä puuttuu diakriitteja:
  `python scripts/report_diacritics.py` (tulos `data/diacritics_todo.txt`).
- **Lisäosiot sivun lopussa:** (1) laitosten määrä maittain suhteutettuna väkilukuun (Eurostat, `data/population.json`;
  absoluuttinen määrä ja per miljoona asukasta) ja (2) katvealueet: alueet, joilta on yli 300 km lähimpään laitokseen
  (laskettu koordinaateista, `scripts/build_coverage.py` → `data/coverage.json`). Saman maan sääntö: saman maan
  laitoksella on pidempi kantama. Ruutu on katve, jos yhtäkään laitosta ei ole 300 km:n sisällä eikä saman maan
  laitosta 600 km:n sisällä; jos saman maan laitos on 300–600 km:n päässä, ruutu näytetään vaaleampana eikä sitä
  lasketa. Maakohtainen rajaus valittiin saarikohtaisen sijaan, koska se on yksinkertaisempi. Osiot eivät kuulu pääasialliseen näkymään,
  eivätkä ne käytä uutta väriä: palkit ja katvealueet ovat musteen värisiä (vermilion = partneri, sininen = linkit).
  Vain tasojen 1 ja 2 laitokset lasketaan, joten taso 3 -maat (esim. Kreikka) näkyvät katveena.
- **Julkaistava kansio** on `site/`; `build_site.py` kopioi `site.json`:n sinne (`site/data/`).

## Vaiheistus

1. Lue OpenAPI-spec, hae data, tulosta kenttien nimet ja rivimäärä
2. Nimihaku ja AEC-ristiinajo, tulosta ehdokaslista tarkistettavaksi
3. `annotations.json` ensimmäinen versio, rajatapaukset käsin
4. Geokoodaus kerran, tulos talteen
5. `site.json`-generointi ja muutosraportti
6. Suunnitelma visuaalisesta suunnasta, arviointi, sitten sivu
7. Julkaisu

Älä siirry vaiheeseen 6 ennen kuin data on kunnossa. Käyttöliittymän
rakentaminen puutteellisen datan päälle johtaa siihen, että molempia korjataan
samaan aikaan.

## Rajoitteet

Sivu on käytännössä julkinen, vaikka linkkiä ei jaettaisi laajasti.
**Vain julkista dataa.** Partneritiedot otetaan korkeakoulujen itsensä
julkaisemista vaihtokohdelistoista, ei sisäisistä sopimusrekistereistä.
