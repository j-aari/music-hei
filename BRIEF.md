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

Sivulla on oltava näkyvissä käytetty rajanveto, esimerkiksi: *"Mukana laitokset,
joissa musiikki on itsenäinen tutkintoa myöntävä yksikkö."* Tämä on väite, joka
pitää pystyä puolustamaan, ja sen näyttäminen tekee sivusta uskottavan.

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
