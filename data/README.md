# Data

The files in this folder are licensed under [CC BY 4.0](LICENSE).

Suggested attribution:

> Jyri Aarila, *European Music Institutions with an Erasmus Charter* (data), CC BY 4.0. Contains data from the European Commission's list of holders of the Erasmus Charter for Higher Education.

## What is in here

| File | Content |
|---|---|
| `upstream.json`, `upstream.meta.json` | The ECHE list as retrieved (by the European Commission, via the ECHE List API of the European University Foundation), and the retrieval date |
| `annotations.json` | Our classification of institutions (level, type, notes, display names). Hand-edited |
| `excluded.json` | Institutions that matched the name search but were excluded, with the reason |
| `geo.json` | Geocoded coordinates (Nominatim / OpenStreetMap data) |
| `population.json` | Population on 1 January per country, from Eurostat (table tps00001), with the year and retrieval date |
| `coverage.json` | Areas more than 300 km from the nearest institution, calculated from the coordinates (0.1° grid), with per-country shares |
| `reference/` | Natural Earth 1:110m country outlines (public domain) used only for the coverage calculation |
| `site.json` | Generated merge of the above, loaded by the page |
| `candidates_name.json`, `diacritics_todo.txt` | Generated working lists |

## Provenance

The original ECHE data (institution names, addresses, Erasmus codes, OIDs, websites) comes from the **European Commission**. `population.json` contains population figures published by **Eurostat**, which may be reused with acknowledgement of the source. `reference/` is third-party data (Natural Earth, public domain) and is not covered by the licence above. The licence above applies to our own contribution: the classification, the annotations, the exclusion decisions, the geocoding and the compiled files. It does not change the terms under which the Commission published the original list. Geographic coordinates are derived from OpenStreetMap data, which is available under the ODbL; see <https://www.openstreetmap.org/copyright>.
