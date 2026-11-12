"""Generoi site/data/european-music-institutions.xlsx: kaikki sivun laitokset ja niiden tiedot Excel-taulukkona.

Ajetaan build_site.py:n lopussa (ja erikseen tarvittaessa). Lukee vain valmiit datatiedostot (site.json,
contacts, networks, strategies, programmes, disciplines, mobility), ei hae mitään verkosta.

Välilehdet:
  Institutions        yksi rivi per laitos, kaikki tiedot omina sarakkeinaan
  Study programmes    yksi rivi per laitos ja ala (tasot BA/MA/Doc omina sarakkeinaan)
  Strategy documents  yksi rivi per dokumentti
  About               lähteet, hakupäivä ja vastuulauseke
Sivun tekstit ovat englanniksi, joten myös taulukko on englanniksi.
"""

import json
import sys

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

from common import CONTACTS, DISCIPLINES, NETWORKS, PROGRAMMES, PUBLIC_DATA, SITE, STRATEGIES, MOBILITY

XLSX_NAME = "european-music-institutions.xlsx"
CHARTER = {"eche": "Holds an ECHE", "from_2027": "From 2027 (no ECHE yet)"}
STRATEGY_TYPES = {"strategy": "Strategy", "internationalisation-strategy": "Internationalisation strategy", "annual-report": "Annual report"}
MOBILITY_TYPES = [("studies", "Student exchange"), ("traineeships", "Student traineeships"), ("teaching", "Staff teaching"), ("training", "Staff training")]
LEVELS = ["BA", "MA", "Doc"]
HEAD_FONT = Font(bold=True, color="FFFFFF")
HEAD_FILL = PatternFill("solid", fgColor="0F1620")
LINK_FONT = Font(color="1D4ED8", underline="single")


def load(path):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None


def sheet(wb, title, cols, rows, widths, link_cols=()):
    """Taulukko: lihavoitu otsikkorivi, jäädytetty otsikko, automaattisuodatin, linkit klikattaviksi."""
    ws = wb.create_sheet(title)
    ws.append(cols)
    for c in ws[1]:
        c.font, c.fill = HEAD_FONT, HEAD_FILL
        c.alignment = Alignment(vertical="center", wrap_text=True)
    for r in rows:
        ws.append(["" if v is None else v for v in r])
    for idx in link_cols:
        for (cell,) in ws.iter_rows(min_row=2, min_col=idx, max_col=idx):
            if isinstance(cell.value, str) and cell.value.startswith("http"):
                cell.hyperlink, cell.font = cell.value, LINK_FONT
    for k, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(k)].width = w
    ws.freeze_panes = "B2"
    ws.auto_filter.ref = ws.dimensions
    return ws


def build(path_out=None):
    site = load(SITE)
    meta, items = site["meta"], site["institutions"]
    contacts = (load(CONTACTS) or {}).get("contacts", {})
    networks = load(NETWORKS) or {"networks": [], "memberships": {}}
    strategies = load(STRATEGIES) or {"documents": [], "institution_status": {}, "meta": {}}
    programmes = load(PROGRAMMES) or {"programmes": []}
    disciplines = load(DISCIPLINES) or {"disciplines": [], "groups": []}
    mobility = load(MOBILITY)

    disc_name = {d["id"]: d["name"] for d in disciplines["disciplines"]}
    group_of = {d: g["name"] for g in disciplines["groups"] for d in g["disciplines"]}
    progs_by = {}
    for p in programmes["programmes"]:
        progs_by.setdefault(p["erasmus_code"], []).append(p)
    status_labels = strategies["meta"].get("status_labels") or {}
    mapped = {n["id"] for n in networks["networks"] if n.get("mapped")}

    def mob_label(rec, t, k):
        if not mobility or not rec:
            return None
        cls = rec["types"][t][k]
        if cls is None:
            return "No field recorded"
        if not cls:
            return "Not in data"
        c = mobility["meta"]["classes"][f"{t}.{'out' if k == 0 else 'in'}"]
        lo, hi = c["ranges"][cls - 1]
        return f"{c['labels'][cls - 1]} ({lo}–{hi})"

    cols = ["Name", "Country", "City", "Street address", "Postal code", "Website", "Institution type", "Part of",
            "Erasmus Charter", "Erasmus code", "OID", "Name in the ECHE list", "International office e-mail",
            "International office contact page", "AEC member", "EUA member", "Strategy documents",
            "Fields of study", "Degree levels offered", "Disciplines taught (count)"]
    if mobility:
        y0, y1 = mobility["meta"]["years"]
        for _, label in MOBILITY_TYPES:
            cols += [f"{label}, outgoing {y0}–{y1}", f"{label}, incoming {y0}–{y1}"]
        cols.append("Most frequent partner countries (mobility)")
    cols += ["Latitude", "Longitude", "Note"]

    rows = []
    for i in items:
        later = i.get("charter") == "from_2027"
        code = i["erasmus_code"]
        c = contacts.get(code) or {} if code else {}
        recs = {r["network"] for r in networks["memberships"].get(code, [])} if code else set()
        aec = (("Yes" if i.get("aec_member") else "No") if later else ("Yes" if "aec" in recs else "No")) if "aec" in mapped else None
        eua = None if later or "eua" not in mapped else ("Yes" if "eua" in recs else "No")
        st = strategies["institution_status"].get(code) if code else None
        progs = progs_by.get(i["id"]) or (progs_by.get(code) if code else None) or []
        fields = sorted({group_of.get(p["discipline"], p["discipline"]) for p in progs})
        levels = [lv for lv in LEVELS if any(lv in p["levels"] for p in progs)]
        row = [i["name"], i["country"], i["city"], i.get("street"), i.get("postal_code"), i.get("website"),
               meta["tier_labels"][str(i["tier"])], i.get("parent_name"), CHARTER[i.get("charter") or "eche"], code,
               i.get("oid"), i.get("name_upstream"), c.get("email"), c.get("page"), aec, eua,
               status_labels.get(st, st) if st else ("Not collected" if not later else None),
               "; ".join(fields) or None, ", ".join(levels) or None, len(progs) or None]
        if mobility:
            rec = mobility["institutions"].get(code) if code else None
            for t, _ in MOBILITY_TYPES:
                row += [mob_label(rec, t, 0), mob_label(rec, t, 1)]
            row.append(", ".join(mobility["meta"].get("country_names", {}).get(cc, cc) for cc in rec["partners"]) if rec else None)
        row += [i.get("lat"), i.get("lon"), i.get("public_note")]
        rows.append(row)

    wb = Workbook()
    wb.remove(wb.active)
    widths = [42, 16, 16, 30, 11, 34, 32, 32, 22, 15, 14, 36, 34, 40, 11, 11, 28, 50, 14, 14]
    if mobility:
        widths += [22] * (2 * len(MOBILITY_TYPES)) + [34]
    widths += [10, 10, 40]
    sheet(wb, "Institutions", cols, rows, widths, link_cols=(6, 14))

    by_id = {i["id"]: i for i in items}
    by_code = {i["erasmus_code"]: i for i in items if i["erasmus_code"]}
    prow = []
    for p in programmes["programmes"]:
        inst = by_id.get(p["erasmus_code"]) or by_code.get(p["erasmus_code"])
        if not inst:
            continue
        names = "; ".join(dict.fromkeys(e["programme_name"] for e in p.get("evidence", []) if e.get("programme_name")))
        prow.append([inst["name"], inst["country"], inst["city"], inst["erasmus_code"], group_of.get(p["discipline"]),
                     disc_name.get(p["discipline"], p["discipline"]), *("Yes" if lv in p["levels"] else None for lv in LEVELS),
                     names or None, p.get("source_url")])
    prow.sort(key=lambda r: (r[1], r[0].casefold(), r[4] or "", r[5]))
    sheet(wb, "Study programmes", ["Institution", "Country", "City", "Erasmus code", "Field of study", "Discipline", "BA", "MA", "Doc",
                                   "Programme names", "Source"], prow, [42, 16, 16, 15, 30, 30, 6, 6, 6, 60, 50], link_cols=(11,))

    srow = []
    for d in strategies["documents"]:
        inst = by_code.get(d["erasmus_code"])
        if not inst:
            continue
        srow.append([inst["name"], inst["country"], d["name_original"], STRATEGY_TYPES.get(d["type"], d["type"]),
                     d.get("period") or d.get("publication_year"), d.get("language"), d["document_url"]])
    srow.sort(key=lambda r: (r[1], r[0].casefold()))
    sheet(wb, "Strategy documents", ["Institution", "Country", "Document", "Type", "Period or year", "Language", "Link"],
          srow, [42, 16, 50, 26, 14, 10, 60], link_cols=(7,))

    ws = wb.create_sheet("About")
    about = [
        ["European Music Institutions with an Erasmus Charter"],
        [],
        ["Scope", meta["scope_text"]],
        ["From 2027", meta.get("scope_text_2027") or ""],
        ["Institution data", f"European Commission list of ECHE holders, retrieved {meta['fetched']} ({meta.get('upstream_source') or ''})."],
        ["Mobility", f"{mobility['meta']['source']}, {mobility['meta']['source_url']}. Size classes among the music institutions on the page, not exact counts." if mobility else ""],
        ["Study programmes", "Collected from each institution's own website (October 2026); not verified by the institutions, some lists are partial."],
        ["Strategy documents", "Collected for selected countries only; 'Not collected' means the institution has not been checked."],
        ["Generated", meta["generated"]],
        ["Disclaimer", meta["disclaimer"]],
    ]
    for r in about:
        ws.append(r)
    ws["A1"].font = Font(bold=True, size=14)
    for (cell,) in ws.iter_rows(min_row=3, max_col=1):
        cell.font = Font(bold=True)
        cell.alignment = Alignment(vertical="top")
    for (cell,) in ws.iter_rows(min_row=3, min_col=2, max_col=2):
        cell.alignment = Alignment(wrap_text=True, vertical="top")
    ws.column_dimensions["A"].width = 20
    ws.column_dimensions["B"].width = 110

    out = path_out or (PUBLIC_DATA / XLSX_NAME if PUBLIC_DATA else None)
    if out:
        out.parent.mkdir(parents=True, exist_ok=True)
        wb.save(out)
    return out, len(rows), len(prow), len(srow)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    out, n, p, s = build()
    print(f"{out}: {n} laitosta, {p} ohjelmariviä, {s} strategiadokumenttia")
