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
