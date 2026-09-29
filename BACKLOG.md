# Backlog and decisions

Things that were deliberately deferred or scoped down, and why, so the reasoning does not have to be reconstructed later.

## Strategy documents: selected countries only, not all 186 institutions

Strategy/internationalisation-strategy/annual-report links (`data/strategies.json`) are collected for a chosen subset of countries (starting with the pilot 10, then Italy, then Germany), not for all 186 institutions.

**Why:** the publication rate is low even when searching primarily for the Erasmus Policy Statement, which is a mandatory ECHE annex and therefore exists for every institution in principle. In Italy (73 institutions), only 30% had a publicly linkable document; a further 34% could be shown to exist (referenced on the institution's own site) without a working link, and 36% surfaced nothing at all. Germany (26 institutions) showed a similar pattern (23% published, 23% mentioned without a link, 54% not found).

At this hit rate, extending the search to all 186 institutions would mostly measure which institutions keep a tidy, well-indexed website rather than which institutions have a strategy. The `not_found` category is dominated by generic Erasmus/mobility administration pages with no EPS-specific document or mention (the same pattern in both countries checked so far) — i.e. absence of evidence, not evidence of absence.

**How to apply:** keep strategy data scoped to countries picked one at a time by explicit request, each with its own status distribution reported before moving on. If coverage is ever extended further, say so explicitly on the page (the coverage line already does this: "Strategy data covers N of 186 institutions") rather than implying full coverage.

## Removed: "Institutions relative to population" section

The section showing institution counts per country relative to population (absolute and per million inhabitants) was removed from the page (`site/index.html`, `site/js/app.js`, `site/css/style.css`).

**Why:** the per-million-inhabitants ratio didn't answer any question a reader of this page actually has, and it was misleading because it treats very different kinds of institutions as equivalent. It made Finland's single, large university-of-the-arts music unit look sparse next to Italy's many small, separate conservatoires, when the difference is how music education is organised in each country, not how much of it there is.

**How to apply:** `data/population.json` and `scripts/fetch_population.py` are kept in the repository (not deleted) because population data may be useful later for a different, better-justified ratio — for example Erasmus+ mobility funding per capita. Don't re-add an institutions-per-population display without a specific question it answers.

## Removed: "Areas far from a music institution" section

The coverage section (map of areas with no institution within 300 km, plus a per-country table) was removed from the page (`site/index.html`, `site/js/app.js`, `site/css/style.css`).

**Why:** the feature was judged unnecessary for the page.

**How to apply:** `scripts/build_coverage.py`, `data/coverage.json` and `data/reference/` are kept in the repository and `scripts/update.py` still regenerates the data, so the section can be restored from git history if needed. Don't re-add it without a specific question it answers.

## Erasmus+ mobility profile: classes, not counts; 2014–2022

The panel shows mobility types and a four-class scale per institution (`data/mobility.json`), not exact counts or ratios.

**Why:** the question is what mobility each institution offers and roughly how much, not a comparison per capita or per student. The data has no institution identifiers, so institutions are matched by name, and organisation names are missing from part of the rows; exact counts would look more precise than they are. Class limits come from the data (quartiles among the institutions on the page; thirds for traineeships, where quartile limits overlap), not from chosen round numbers. Short-term student mobility is kept in `mobility.json` but hidden on the page: 150 of 186 institutions have none in the data (2021–2022 only), so the row would be mostly empty. Show it again once more years are complete. 2023–2024 exist in the source but are incomplete until the projects close.

**How to apply:** when extending the years, move `LAST_YEAR` in `scripts/build_mobility.py` only once the year is at least two to three years old, and re-run `find_mobility_names.py` to catch new name forms. Keep "Not in data" distinct from "not offered". Four institutions could not be found (Friedrich Gulda School of Music, Evangelische Hochschule für Kirchenmusik Halle, IESM Aix-en-Provence, Conservatorio Tchaikovsky Nocera Terinese).

## International office contact per institution

The details panel shows, after the address, the general e-mail address of the institution's international office, or a link to the office's contact page when no general address is published (`data/contacts.json`).

**Why:** the ECHE list has no contact details (only name, address, website and codes), and a visitor looking for a partner usually needs exactly this.

**How to apply:** only general office addresses (for example international@…, erasmus@…), never the names or e-mail addresses of individual people, so the data stays current when staff change and no personal data is published. Every address has the page it was found on (`source`) and the date it was checked. Suggestions come from `scripts/find_contacts.py`; every entry was checked against its source page. In September 2026: 134 addresses, 25 contact pages, 27 institutions with neither (their sites publish only personal addresses, block automated access or were unreachable); the panel says "No general address found on the website" for those. Re-check about once a year, and fill the gaps one country at a time.

## Networks: AEC and EUA checked, IASJ and ELIA not yet

The details panel lists the networks an institution belongs to, discipline networks first and umbrella organisations second (`data/networks.json`), with a coverage line naming the networks whose member lists have been checked and those that have not.

**Why:** an empty list must not read as "not a member of any network". Only the AEC (European Association of Conservatoires) and the EUA (European University Association) have been checked (September 2026): 151 of 186 institutions are AEC members, 6 are EUA members. The AEC list on its website is paginated inconsistently (some members repeat, others are skipped), so it was completed with the site's keyword search by city; the result, 311 members, matches the site. ELIA's site blocks automated access and IASJ has no public member list at a stable address.

**How to apply:** add a network by setting `mapped: true` only after its whole member list has been matched; until then keep it in `networks` with `mapped: false` so the coverage line names it. Match by website address where the list has one (EUA), otherwise by name and city, and check by hand: several institutions are listed under English or older names (for example the KMH as "Royal College of Music in Stockholm", PESMD Bordeaux as "RésoNAnces").

The Networks filter has "AEC member", "Not an AEC member" and "EUA member". "Not an AEC member" (35 of 186) is the more interesting group, and it is a real value only because the whole AEC list has been checked; a network may get a "not a member" option only once it is fully mapped.

### Next: IASJ (to be mapped)

Map the International Association of Schools of Jazz next: jazz schools and departments, which ties in with a colleague's wish to see pop and jazz institutions. Find a stable, complete member list first; match by name and city as with the AEC, then set `mapped: true`.

### Waiting: ELIA

ELIA (European League of Institutes of the Arts) stays `mapped: false`: its website blocks automated access (HTTP 403), so the member list cannot be retrieved reliably. Revisit if ELIA publishes a list that can be downloaded, or if checking by hand country by country is worth it.

