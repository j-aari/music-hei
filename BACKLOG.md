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
