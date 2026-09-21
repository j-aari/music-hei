# European Music Institutions with an Erasmus Charter

A static web page that lists music institutions in Europe that hold an Erasmus Charter for Higher Education (ECHE). It answers three questions: which music institutions exist, where are they, and which of them are exchange partners.

The page has a list view and a map view that always show the same filtered set, filters for country, institution type, language of instruction and partner status, a text search on name and city, a details panel for each institution, and a CSV export of whatever is currently shown. Two further sections at the end of the page show the number of institutions per country relative to population, and the areas with no institution within 300 km (or within 600 km in the same country). There is no server, no database, no login, no cookies and no analytics.

This is an informal compilation of public data. It is not an official publication of the European Commission or of any of the institutions listed.

## What is included

- **Scope: ECHE holders.** Only institutions on the European Commission's list of ECHE holders are considered. An ECHE is awarded to institutions that are recognised as higher education institutions by their national authorities, so this project does not assess an institution's status. The only question is whether it belongs to music.
- **Level 1: independent music institution** (a conservatoire, a *Musikhochschule*, an academy of music).
- **Level 2: music unit of an arts university** (for example a music department inside a university of the arts).
- **Level 3 is not included yet:** music departments inside general universities. This is planned as a separate round.
- **The tier follows the parent organisation, not the country.** If the parent is an arts institution, the level is 2; if it is a multidisciplinary general university, the level is 3.
- **United Kingdom and Switzerland.** Both associate to Erasmus+ on 1 January 2027 and will only appear once their institutions have been awarded an ECHE. The classification search already knows common UK and Swiss name forms (Royal College of Music, *Haute école de musique*, and so on), so new institutions are picked up in an update.

The scope statement on the page is generated from the data and includes the date the list was retrieved.

Currently: **186 institutions** (167 at level 1, 19 at level 2) in 24 countries.

## Where the data comes from

| Data | Source |
|---|---|
| Institutions, addresses, Erasmus codes, OIDs, websites | The list of ECHE holders published by the **European Commission** ([source list](https://erasmus-plus.ec.europa.eu/document/higher-education-institutions-holding-an-eche-2021-2027)), retrieved through the [ECHE List API](https://eche-list.erasmuswithoutpaper.eu/openapi) of the European University Foundation |
| Which institutions are music institutions, and their level | Our own classification, recorded in `data/annotations.json` (see below) |
| Map positions | Geocoded once with [Nominatim](https://nominatim.openstreetmap.org/) and stored in `data/geo.json`. Some positions are approximate (city centre) and the details panel says so |
| Map tiles | [OpenStreetMap](https://www.openstreetmap.org/copyright), loaded only when a map is about to be seen (the map view, or the coverage map at the end of the page) |
| Population | [Eurostat](https://ec.europa.eu/eurostat/databrowser/view/tps00001/default/table), table tps00001 (population on 1 January), stored in `data/population.json` |
| Country outlines (coverage analysis only) | [Natural Earth](https://www.naturalearthdata.com/) 1:110m countries, public domain, in `data/reference/` |
| Partner status | The exchange-destination list published by the University of the Arts Helsinki. **This field is not filled in yet**, so the partner and language filters are hidden until data exists |

Only public data is used. Partner information should be taken from the institutions' own published exchange-destination lists, not from internal agreement registers.

## How the classification was done

The ECHE list has no subject field, so music institutions had to be identified. The work was done in layers, and every decision is recorded in a file rather than derived at run time:

1. **Name search** (`scripts/find_candidates.py`). A strict list of name forms (*Conservatorio*, *Conservatoire*, *Hochschule für Musik*, *Akademia Muzyczna*, *Academy of Music*, and so on) and a looser list of music-related stems. The looser matches are only candidates for review.
2. **Automatic exclusions** for obvious false positives: the *Conservatoire national des arts et métiers*, drama conservatoires, and dance-only institutions.
3. **Manual review.** Borderline cases, arts universities and institutions whose legal name differs from the name of the school (common in Italy and Spain: *srl*, *SL*, *fundació*) were decided by hand.

**The classification decisions are in two files:**

- **`data/annotations.json`**: every included institution, keyed by its normalised Erasmus code, with its level (`tier`), `institution_type`, a note on why it was classified that way, and optional fields (`public_note`, `display_name`, `partner_of_siba`, `languages_of_instruction`). It is edited by hand. Institutions that disappear from the ECHE list are moved to an `orphaned` section for review, never deleted.
- **`data/excluded.json`**: institutions that matched the name search but were excluded, each with the reason. Automatic rules and manual decisions are both listed here.

## How the data is organised

```
data/
  upstream.json      # the ECHE list as retrieved. Overwritten in full on every update.
  annotations.json   # our classification. Never written automatically, except for the orphaned section.
  geo.json           # coordinates, geocoded once.
  population.json    # Eurostat population per country (fetch_population.py, about once a year)
  coverage.json      # areas more than 300 km from the nearest institution. Generated from the coordinates.
  reference/         # Natural Earth country outlines used for the coverage calculation
  site.json          # the merge of the three above. Generated. This is what the page loads.
  candidates_name.json, excluded.json   # generated by the name search
site/                # the published page (self-contained; site/data/site.json is a copy)
scripts/             # Python, standard library only
```

The two layers are joined only when the page data is built, by the normalised Erasmus code (`erasmusCodeNormalized`, falling back to the raw code). This is the important design decision: the Commission's list changes, and keeping it separate from the classification means an update cannot destroy the classification work.

## Updating

Requires Python 3.11 (the only version it has been tested on). There are no third-party dependencies.

```
python scripts/update.py            # fetch the list and print a change report; writes nothing
python scripts/update.py --apply    # write, then run the whole chain
```

The change report lists new institutions (marking those that match the music name search), removed institutions, name changes, and probable Erasmus-code changes (same OID or PIC, different code). With `--apply` the script:

1. overwrites `upstream.json` and records the retrieval date,
2. moves the annotations of removed institutions to the `orphaned` section of `annotations.json`,
3. regenerates the candidate and exclusion lists,
4. geocodes annotated institutions that have no coordinates yet (at most one Nominatim request per second),
5. rebuilds `data/site.json` and the copy in `site/data/`,
6. recalculates the coverage areas (`data/coverage.json`) from the coordinates.

New institutions do **not** appear on the page until they have been classified by hand in `annotations.json` (or excluded, with a reason, in `MANUAL_EXCLUDE` in `scripts/find_candidates.py`). After editing an annotation, run `python scripts/build_site.py`.

Other useful scripts:

| Script | Purpose |
|---|---|
| `scripts/fetch_upstream.py` | Fetch the ECHE list only |
| `scripts/find_candidates.py` | Name search; writes the candidate and exclusion lists |
| `scripts/find_arts_umbrella.py` | Lists multidisciplinary arts universities that may contain music units |
| `scripts/geocode.py` | Geocode; `--check` verifies existing results, keys re-geocode single institutions |
| `scripts/build_site.py` | Build `site.json` |
| `scripts/fetch_population.py` | Fetch population from Eurostat (`data/population.json`); run about once a year, it is not part of `update.py` |
| `scripts/build_coverage.py` | Calculate the areas more than 300 km from the nearest institution (`data/coverage.json`) |
| `scripts/report_diacritics.py` | Lists names that probably lack diacritics (the source data is often plain ASCII capitals); fix them with `display_name` in `annotations.json` |

## Running the page locally

The page loads its data with `fetch`, so it must be served over HTTP; opening `index.html` from disk will not work.

```
cd site
python -m http.server 8000
```

Then open <http://localhost:8000/>. The `site/` folder is self-contained (data, fonts, Leaflet) and can be published on any static host such as Netlify or GitHub Pages. Its state is stored in the URL hash, so a filtered view can be shared as a link.

## Publishing

The `site/` folder is the whole site. `.github/workflows/pages.yml` publishes it to GitHub Pages whenever `site/` changes on the `main` branch. One-time setup in the repository: Settings > Pages > Build and deployment > Source: **GitHub Actions**. After an update, commit the regenerated files (`data/` and `site/data/site.json`) and push; the page is redeployed automatically.

## Known limitations

- Some institution names lack diacritics because the source list is often plain ASCII capitals (for example "Universitat fur Musik"). The list of affected names is produced by `scripts/report_diacritics.py`.
- City names follow the source and are inconsistent between languages (for example *Wien* and *Vienna*), so a search for one form may miss the other.
- The coverage map gives an institution in the same country a longer reach: an area is uncovered only if no institution is within 300 km and none in its own country is within 600 km. Areas with an institution of their own country 300–600 km away are shown in a lighter tone and not counted. Malta is not assessed because it is missing from the 1:110m country outlines; it is within 300 km of Catania in any case.
- Which institutions count as music institutions is a judgement, not a fact in the data. That is why the decisions are visible in `annotations.json` and `excluded.json`.

## Licence and attribution

| What | Licence |
|---|---|
| Code (`scripts/`, `site/index.html`, `site/css/`, `site/js/`) | [MIT](LICENSE) |
| Data (`data/`) | [CC BY 4.0](data/LICENSE), see [`data/README.md`](data/README.md) for the suggested attribution |
| Original ECHE data | Published by the **European Commission** |

The CC BY 4.0 licence on `data/` applies to our own contribution: the classification, the annotations, the exclusion decisions, the geocoding and the compiled files. The original ECHE data (institution names, addresses, Erasmus codes, OIDs, websites) comes from the European Commission, and the licence does not change the terms under which the Commission published it.

Third-party components keep their own licences: Leaflet (BSD-2-Clause, `site/vendor/leaflet/LICENSE`), the Newsreader and Public Sans fonts (SIL Open Font License 1.1, `site/fonts/`), and the map data and tiles by OpenStreetMap contributors (ODbL; attribution is shown on the map).
