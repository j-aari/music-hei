# Opintotarjonnan keruu (programmes.json)

Tavoite: jokaisen sivun 256 laitoksen opintotarjonta aloittain `data/programmes.json`-tiedostoon. Sivu näyttää sen
laitospaneelissa ("Study programmes") ja vasemman palkin "Field of study" -suodattimessa.

Tilanne näkyy komennolla:

    python -c "import json;m=json.load(open('data/programmes.json',encoding='utf-8'))['meta'];print(len(m['institutions']))"

## Työnkulku (yksi erä ≈ 15–20 laitosta, maittain site.json-järjestyksessä)

1. Valitse seuraavat keräämättömät laitokset:

       python scripts/programmes/next.py 20

2. Kopioi edellinen eräskripti pohjaksi (`b01.py` → `b02.py`) ja tyhjennä laitosrivit.
3. Jokaiselle laitokselle: etsi oma ohjelmalistaus ja kirjaa rivit.
   - `python scripts/programmes/f.py URL [regex]` – sivun linkit (teksti | osoite), suodatettuna
   - `python scripts/programmes/body.py URL [alku-regex] [rivit]` – sivun teksti
   - `python scripts/programmes/g.py REGEX URL...` – osuvat rivit monelta sivulta
   - PDF: `curl -skL -A Mozilla/5.0 -o x.pdf URL; pdftotext -enc UTF-8 x.pdf -`
   - Sivut tallentuvat välimuistiin `scripts/programmes/cache/` (ei versionhallinnassa).
4. Rivit eräskriptissä:
   - `R(code, "ala1 ala2", "BA MA", "ohjelman nimi sivulla", url, huomautus=None)` – käsin
   - `A(I, code, url, linkki-regex, drop=..., default_level=...)` – automaattisesti linkkilistasta
   - `T(I, code, url, rivi-regex, ...)` – automaattisesti tekstiriveistä
   - A ja T luokittelevat nimet `mp.py`:n avainsanoilla ja tulostavat luokittelemattomat; tarkista ne käsin.
   - `NOTES[code] = "..."` laitoksille, joilta ei löydy kirjattavaa (esim. pelkkä tohtorikoulutus).
5. Aja eräskripti (kirjoittaa `data/programmes_batches/NN.json`) ja yhdistä:

       python scripts/programmes/bNN.py
       python scripts/add_programmes.py data/programmes_batches/NN.json
       .venv/Scripts/python.exe scripts/build_site.py

   `build_site.py` päivittää myös `generated`-päivän site.json-tiedostoihin; palauta ne (`git checkout -- data/site.json site/data/site.json`), jos laitosdata ei muuttunut.
6. Commit per erä.

## Kirjaussäännöt

- Vain laitoksen omilla sivuilla mainittu; ei päätellä muista laitoksista. `verified: false`.
- Aloittain: yksi rivi per ala ja taso riittää (`disciplines.json`-tunnisteet).
- Jazz-, pop- ja vanhan musiikin soitinohjelmat kirjataan tyylisuunnan alle, ei jokaisen soittimen alle.
- Tasot BA/MA/Doc. Tohtoritaso vain, jos tohtorisivu nimeää alan. Diplomi- ja konservatorio-ohjelmat ilman tasoa, huomautuksella.
- Fédération Wallonie-Bruxelles, Flanderi yms.: jos sivusto kertoo rakenteen (Bachelier + Master) yhteisesti, sama taso kaikille sen osastoille.
- Opettajankoulutus, IGP ja pedagogiset maisteriohjelmat → `music-education`.

## Havaintoja keruusta (erät 1–5, 8.10.2026)

- **Aikaraja:** noin 6 sivuhakua per laitos. Jos ohjelmalistaa ei löydy, kirjaa vain löydetty (esim. pelkkä `music-education`) tai `NOTES`-huomautus, ja siirry eteenpäin.
- **Vajaata tietoa ei kirjata isoille konservatorioille.** Jos sivu näyttää vain osan ohjelmista (esim. ei soittimia), jätä laitos odottamaan alla olevaan listaan; muuten suodatin antaa väärän kuvan.
- **Tyylisääntö `mp.classify`:ssa:** jos nimessä on jazz/pop/vanha musiikki, soitinalat pudotetaan. Nimet kuten "Streichinstrumente: Historische …, Violine" menettävät siksi `strings`-alan – lisää se käsin `R(...)`-rivillä.
- **Sivujen haku:** `f.py` kokeilee curlia, jos Python saa 403/406/429. JS-sivuille (hakulomakkeet) etsi sivutus- tai AJAX-osoite (`?page=`, `tx_solr[page]`, `/ajax/...`) tai käytä WebSearchia oikean ohjelmasivun löytämiseen.
- **Tasot:** jos sivu kertoo rakenteen yhteisesti (Saksa: B.Mus./M.Mus., Tanska: bachelor+kandidat, FWB: bachelier+master), sama taso kaikille aloille `default_level`-parametrilla.
- **Verkko-osoite vanhentunut:** korjaa `data/annotations.json`-tiedostoon `website_override` ja perustelu `notes`-kenttään (esim. PESMD Bordeaux → resonances-na.eu).

### Odottaa (sivuilta ei saatu kattavaa listaa ensimmäisellä yrityksellä)

- `D  HAMBURG05` (hfmt-hamburg.de: vain osa ohjelmista linkkeinä; instrumenttiohjelmat puuttuvat)
- `D  FRANKFU02` (hfmdk-frankfurt.de/thema/studiengaenge-von-bis-z on JS-lista)
- `D  SAARBRU08` (hfm.saarland.de ei vastannut)
- `D  MAINZ01` (musik.uni-mainz.de: DNS-virhe; kokeile uni-mainz.de:n kautta)
- `D  LEIPZIG05`, `D  MUNCHEN03`, `D  ROSTOCK02`, `D  HANNOVE04`, `D  DUSSELD06`, `D  STUTTGA03`, `D  DRESDEN05`, `D  LUBECK02` ja muut Saksan jäljellä olevat (next.py listaa ne ensimmäisinä)
