#!/usr/bin/env python3
"""
Hilin Mu — DATA COMPLETENESS AUDIT across the master-candidate files.

For each cohort x level x side, measures completeness of FOUR data families:
  1. Pre/Post test scores   (baseline + endline Math & French)
  2. Gov scores             (1er / 2e trimester evaluations + CFEPD/MA)
  3. EOY status             (Situation / Observation: passe/redouble/abandon/...)
  4. College tracking       (secondary enrollment / orientation CEG-CFM)

TWO completeness measures per family (both, as you asked):
  * school coverage  = (# schools that have ANY non-empty value in that family) /
                       (# schools present in the file)
  * fill rate        = (# non-empty cells in that family's column) / (# data rows)

HOW COLUMNS ARE FOUND (so you can verify, no silent mismatch):
  The four families sit in different columns across differently-structured files,
  and C6 files have banner headers. So the script does NOT assume fixed column
  names. It scans the header band (first 8 rows), reconciles multi-row headers,
  and matches each family by keyword. It PRINTS the matched column header for every
  family in every sheet, so when you recheck by hand you can confirm it located the
  right column. Anything it can't find is reported as 'column not found' (0%), not guessed.

OUTPUT: data_completeness_audit.xlsx
  - 'Summary'      : one row per cohort x level x side x family -> coverage% + fill%
  - 'Per-School'   : one row per school -> a fill% for each family
  - 'Column Map'   : which header it matched for each family in each file (VERIFY THIS)

Read-only on the repo. Run:  python audit_completeness.py
Needs: openpyxl
"""

import re
import unicodedata
from pathlib import Path
from collections import defaultdict

REPO = Path.home() / "Desktop" / "HilinMu1.1"
OUTPUT = REPO / "data_completeness_audit.xlsx"

# Candidate files by cohort x level (mirrors CANDIDATES.md / master_candidates).
CANDIDATES = {
    ("C4", "CM1"): ["Cohort4/CM1/sources/C4_CM1_Marcus_BaseDeDonnees_IntCtrl.xlsx"],
    ("C4", "CM2"): ["Cohort4/CM2/sources/C4_CM2_Marcus_AllComplete_4ExtraSchools.xlsx",
                    "Cohort4/CM2/sources/HilinMu_C4_CM2_All_AlmostComplete.xlsx"],
    ("C5", "CM1"): ["Cohort5/CM1/sources/C5_CM1_BaseDeDonnees_IntCtrl_931_743.xlsx",
                    "Cohort5/CM1/sources/HILIN_MU_C5_CM1_EXAMENS_08_08_2023.xlsx"],
    ("C5", "CM2"): ["Cohort5/CM2/sources/C5_CM2_BasePhasePilote_EOY_CollegeTracking.xlsx"],
    ("C6", "CM1"): [
        "Cohort6/CM1/sources/C6_CM1_SituationFinAnnee_AllCommunes.xlsx",
        "Cohort6/CM1/sources/C6_CM1_Marcus_BaseDeDonnees.xlsx",
    ],
    ("C6", "CM2"): [
        "Cohort6/CM2/sources/C6_CM2_Interv_Pre_Post_TestScores.xlsx",
        "Cohort6/CM2/sources/C6_CM2_Tibiri_Interv_EOY_Status_GovScores.xlsx",
        "Cohort6/CM2/sources/C6_CM2_Tibiri_Control_EOY_Status_GovScores.xlsx",
        "Cohort6/CM2/sources/C6_CM2_Tibiri_Control_CollegeTracking.xlsx",
        "Cohort6/CM2/sources/C6_CM2_Djirataoua_Interv_EOY_Status_GovScores.xlsx",
        "Cohort6/CM2/sources/C6_CM2_Djirataoua_Control_EOY_Status_GovScores.xlsx",
        "Cohort6/CM2/sources/C6_CM2_Djirataoua_Interv_CollegeTracking.xlsx",
        "Cohort6/CM2/sources/C6_CM2_Djirataoua_Control_CollegeTracking.xlsx",
        "Cohort6/CM2/sources/C6_CM2_Safo_Interv_EOY_Status_GovScores.xlsx",
        "Cohort6/CM2/sources/C6_CM2_Safo_Control_EOY_Status_GovScores.xlsx",
        "Cohort6/CM2/sources/C6_CM2_Safo_Control_CollegeTracking.xlsx",
        "Cohort6/CM2/sources/C6_CM2_Sae_Saboua_Interv_EOY_Status_GovScores.xlsx",
        "Cohort6/CM2/sources/C6_CM2_Sae_Saboua_Control_EOY_Status_GovScores.xlsx",
    ],
    ("C7", "CM1"): ["Cohort7/CM1/sources/C7_CM1_TX_CTRL_prepost_status_CANONICAL.xlsx",
                    "Cohort7/CM1/sources/C7_CM1_Consolidated2.xlsx",
                    "Cohort7/CM1/sources/C7_CM1_Resultats_FinAnnee_full.xlsx"],
    ("C7", "CM2"): [
        "Cohort7/CM2/sources/C7_CM2_TX_CTRL_prepost_mentor.xlsx",
        "Cohort7/CM2/sources/C7_CM2_All_Pre_Post_TestScores_GovScores_EOY.xlsx",
        "Cohort7/CM2/sources/C7_CM2_Consolidated_YearEnd_IC.xlsx",
        "Cohort7/CM2/sources/C7_CM2_All_CollegeTracking.xlsx",
    ],
}

# Gov / term-evaluation scores: THREE terms tracked separately (composition |
# trimestre | evaluation vocabularies), plus the annual average. CFEPD stays separate
# (it is the terminal national exam, not a term eval).
FAMILIES = {
    "gov_t1":      ["1ere composition", "1er composition", "1ere compo", "1er trim",
                    "1ere evaluation", "1er evaluation", "evaluation n.1", "m du 1er",
                    "1er trimestre", "1ere comp", "moyenne1er", "moyenne 1er", "moy1er"],
    "gov_t2":      ["2e composition", "2eme composition", "2e compo", "2eme compo",
                    "2e trim", "2eme trim", "2eme evaluation", "2eme evaluation",
                    "evaluation n.2", "m du 2e", "2eme comp", "moyenne2eme", "moyenne 2eme",
                    "moy2eme"],
    "gov_t3":      ["3e composition", "3eme composition", "3e compo", "3eme compo",
                    "3eme compo", "3e trim", "3eme trim", "3eme evaluation",
                    "3eme compo", "3eme comp", "composition 3", "3eme compo",
                    "moyenne3eme", "moyenne 3eme", "moy3eme"],
    "gov_avg":     ["moyenne generale", "moyenne annuelle", "\\bmg\\b", "moy generale",
                    "moy annuelle"],
    "cfepd":       ["cfepd", "m/cfepd", "moy cfepd", "m. cfepd", "m/ cfepd", "cfepd score"],
    "eoy_status":  ["situation finale", "situations finales", "observation", "statut",
                    "\\bsituation\\b", "situation 20", "yearendoutcome", "year end outcome",
                    "year-end outcome"],
    "college":     ["college", "colege", "secondaire", "inscription ecole secondaire",
                    "inscription.*secondaire", "situation au college", "orientee ceg",
                    "orientee cfm", "oriente.*ceg", "inscrite au ceg", "\\bceg\\b",
                    "suivi des filles"],
}

# Pre/post score columns are matched separately (need baseline-vs-endline logic).
# Each entry: (subject, keyword-regexes for the generic score header).
SCORE_SUBJECTS = {
    "math":   ["mathematique", "maths", "math"],
    "french": ["francais", "french", "franc"],
}
# Explicit baseline / endline header signals (folded substrings).
BASELINE_SIG = ["baseline", "base ", "basemath", "basefranc", "baseavg", "pre-test",
                "pre test", "pretest", "pre math", "pre-math", "pre franc", "1er passage"]
ENDLINE_SIG = ["endline", "endmath", "endfranc", "endavg", "post-test", "post test",
               "posttest", "post math", "post-math", "post franc", "2e passage", "\\bend\\b"]
# A column whose SHORT header contains one of these marks the start of the endline block
# (used when baseline/endline columns share an identical generic header).
ENDLINE_DIVIDER = ["endline", "moyenne generale", "2e passage", "post-test", "2eme passage"]

# Family groups for the family-level report (your four families):
FAMILY_GROUPS = {
    "PrePost_Scores":   ["pre_math", "post_math", "pre_french", "post_french"],
    "Gov_Avg":          ["gov_avg", "cfepd"],          # annual average / terminal exam = the floor
    "Gov_Terms":        ["gov_t1", "gov_t2", "gov_t3"], # by-term breakdown = the bonus
    "EOY_Status":       ["eoy_status"],
    "College_Tracking": ["college"],
}

# Aggregate school-level columns found on the 'CM1 & CM2 Metrics' tabs (counts per school).
# These cover dropout/pass/enrollment at school level directly.
AGG_COLS = {
    "agg_inscrites": ["insrites", "inscrites", "inscrit"],
    "agg_presentes": ["presentes", "presente", "present"],
    "agg_admises":   ["admises", "admise", "admis"],
    "agg_abandon":   ["abandonee", "abandon", "abandonnee"],
}

# Headers identifying the SCHOOL column (to count school coverage), banner-aware.
SCHOOL_HEADERS = ["ecole", "ecoles", "etablissement", "school", "nom d'ecole"]
ANTI_SCHOOL = ["nom et prenom", "noms et prenom", "prenoms et noms", "titulaire", "mentor"]
HEADER_SCAN = 8


def fold(s):
    if s is None:
        return ""
    s = unicodedata.normalize("NFKD", str(s))
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", s.lower().strip())


def header_band_text(rows, j):
    cells = [str(r[j]).strip() for r in rows[:HEADER_SCAN]
             if j < len(r) and r[j] not in (None, "") and str(r[j]).strip()]
    return cells


def match_family_col_best(rows, drows, keywords, max_len=35):
    """Like match_family_col, but when multiple columns match the header keywords,
    return the one with the HIGHEST fill over the real data rows (drows). Fixes the
    case of two same-named columns where the first is empty (e.g. duplicate 'Situation')."""
    cands = find_all_cols(rows, keywords, max_len=max_len)
    if not cands:
        return None, None
    best = None
    for j, hdr in cands:
        filled = sum(1 for r in drows if j < len(r) and not is_empty(r[j]))
        if best is None or filled > best[0]:
            best = (filled, j, hdr)
    return (best[1], best[2]) if best else (None, None)


def match_family_col(rows, keywords, max_len=35):
    """Return (col_index, matched_header_text) for the first column whose reconciled
    short header matches any keyword (regex, folded). Short cells only (<= max_len) to
    avoid banner-title false positives. None if not found."""
    if not rows:
        return None, None
    ncol = max((len(r) for r in rows[:HEADER_SCAN]), default=0)
    for j in range(ncol):
        cells = header_band_text(rows, j)
        for c in cells:
            if len(c) > max_len:
                continue
            fc = fold(c)
            for kw in keywords:
                if re.search(kw, fc):
                    return j, c
    return None, None


def find_all_cols(rows, keywords, max_len=35):
    """Return list of (col_index, matched_header) for ALL columns whose short header
    matches any keyword (regex, folded)."""
    out = []
    if not rows:
        return out
    ncol = max((len(r) for r in rows[:HEADER_SCAN]), default=0)
    for j in range(ncol):
        cells = header_band_text(rows, j)
        for c in cells:
            if len(c) > max_len:
                continue
            fc = fold(c)
            if any(re.search(kw, fc) for kw in keywords):
                out.append((j, c))
                break
    return out


def find_divider_col(rows):
    """Index of the column whose short header marks the start of the endline block
    (e.g. an 'ENDLINE' or 'Moyenne générale' separator). None if absent."""
    ncol = max((len(r) for r in rows[:HEADER_SCAN]), default=0)
    for j in range(ncol):
        for c in header_band_text(rows, j):
            if len(c) > 40:
                continue
            fc = fold(c)
            if any(re.search(d, fc) for d in ENDLINE_DIVIDER):
                return j
    return None


def classify_scores(rows, subject_kws):
    """For one subject (math/french), find baseline & endline columns.
    Returns dict: {'pre': (j,hdr) or None, 'post': (j,hdr) or None, 'ambiguous': bool, 'note': str}.

    Logic, in priority order:
      1. Explicit header signal: a column header containing a baseline/endline marker
         is assigned directly.
      2. Divider: columns left of an ENDLINE/Moyenne-générale divider are baseline,
         right are endline.
      3. Two identical generic headers, no signal, no divider -> AMBIGUOUS (don't guess).
    """
    cols = find_all_cols(rows, subject_kws)
    res = {"pre": None, "post": None, "ambiguous": False, "note": ""}
    if not cols:
        return res

    # 1. explicit signals on the matched headers
    pre_explicit, post_explicit, plain = [], [], []
    for j, hdr in cols:
        fh = fold(hdr)
        if any(re.search(s, fh) for s in ENDLINE_SIG):
            post_explicit.append((j, hdr))
        elif any(re.search(s, fh) for s in BASELINE_SIG):
            pre_explicit.append((j, hdr))
        else:
            plain.append((j, hdr))
    if pre_explicit:
        res["pre"] = pre_explicit[0]
    if post_explicit:
        res["post"] = post_explicit[0]
    if res["pre"] and res["post"]:
        return res
    # if explicit handled one side and only plain cols remain, try to fill the other
    if plain:
        if res["pre"] and not res["post"]:
            res["post"] = plain[-1] if plain[-1][0] != res["pre"][0] else None
            res["note"] = "endline inferred (rightmost plain col)" if res["post"] else ""
            return res
        if res["post"] and not res["pre"]:
            res["pre"] = plain[0] if plain[0][0] != res["post"][0] else None
            return res

    # 2. divider-based split (for files with identical 'Mathématique/20' x2)
    if len(plain) >= 2:
        div = find_divider_col(rows)
        if div is not None:
            before = [c for c in plain if c[0] < div]
            after = [c for c in plain if c[0] > div]
            if before and after:
                res["pre"] = before[0]
                res["post"] = after[0]
                res["note"] = "split on ENDLINE/Moyenne-générale divider"
                return res
        # 3. two identical headers, no signal, no divider -> ambiguous
        res["pre"] = plain[0]
        res["post"] = plain[1]
        res["ambiguous"] = True
        res["note"] = "TWO score cols, no base/end signal — pre/post by POSITION, VERIFY"
        return res

    # exactly one plain column, no signal -> treat as baseline, note no endline found
    if len(plain) == 1 and not res["pre"] and not res["post"]:
        res["pre"] = plain[0]
        res["note"] = "only one score col found (no endline)"
    return res


def find_school_col(rows):
    """Index of the school-name column (banner-aware), or None."""
    if not rows:
        return None
    ncol = max((len(r) for r in rows[:HEADER_SCAN]), default=0)
    for j in range(ncol):
        cells = header_band_text(rows, j)
        joined = " ".join(fold(c) for c in cells)
        if any(a in joined for a in ANTI_SCHOOL):
            continue
        if any(any(h in fold(c) for h in SCHOOL_HEADERS) and len(c) <= 30 for c in cells):
            return j
    return None


def data_rows(rows, anchor_cols):
    """Real data rows = rows (after header band) that have a non-empty value in at least
    one ANCHOR column (school name / person name / ID). This excludes trailing junk rows
    that carry only a stray value, which would otherwise inflate the denominator and
    deflate every fill rate."""
    out = []
    if not anchor_cols:
        # fallback: require at least 2 non-empty cells (weak anchor) to avoid 1-cell junk
        for r in rows[HEADER_SCAN:]:
            if sum(1 for c in r if c not in (None, "")) >= 2:
                out.append(r)
        return out
    for r in rows[HEADER_SCAN:]:
        if any(a < len(r) and r[a] not in (None, "") and str(r[a]).strip() for a in anchor_cols):
            out.append(r)
    return out


def find_anchor_cols(rows):
    """Columns usable as a row anchor: the school column plus any name/ID column."""
    anchors = []
    sc = find_school_col(rows)
    if sc is not None:
        anchors.append(sc)
    # name / id columns
    name_kws = ["nom et prenom", "noms et prenom", "prenoms et noms", "nom et prénom",
                "identifiant", "numero hm", "n° d'ordre", "noms et prénoms", "\\bnom\\b"]
    ncol = max((len(r) for r in rows[:HEADER_SCAN]), default=0)
    for j in range(ncol):
        if j in anchors:
            continue
        for c in header_band_text(rows, j):
            if len(c) > 35:
                continue
            if any(re.search(k, fold(c)) for k in name_kws):
                anchors.append(j)
                break
    return anchors


def is_empty(v):
    if v in (None, ""):
        return True
    s = str(v).strip()
    return s == "" or s in (".", "..", "...") or s.lower() in (
        "nan", "#valeur!", "#ref!", "#error!", "na", "n/a", "-")


def audit():
    from openpyxl import load_workbook, Workbook
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.utils import get_column_letter

    summary_rows = []   # cohort, level, side, file, sheet, family, school_cov%, fill%, matched_col, note
    perschool = defaultdict(dict)  # (cohort,level,side,school) -> {familygroup: fill%}
    colmap_rows = []    # file, sheet, family, matched header (VERIFY)

    def side_of(name):
        f = fold(name)
        if any(w in f for w in ("control", "controle", "temoin", "ctrl")):
            return "control"
        if any(w in f for w in ("interv", "intervention", "tx", "lff")):
            return "intervention"
        return "?"

    for (cohort, level), files in CANDIDATES.items():
        for rel in files:
            fp = REPO / rel
            if not fp.exists():
                summary_rows.append([cohort, level, "?", Path(rel).name, "-", "-", "", "",
                                     "", "FILE MISSING"])
                continue
            try:
                wb = load_workbook(fp, read_only=True, data_only=True)
            except Exception as e:
                summary_rows.append([cohort, level, "?", Path(rel).name, "-", "-", "", "",
                                     "", f"OPEN ERROR: {e}"])
                continue

            for ws in wb.worksheets:
                rows = list(ws.iter_rows(values_only=True))
                if not rows:
                    continue
                # skip obvious non-data sheets
                if fold(ws.title) in ("readme", "explication des identifiants", "sheet2",
                                      "feuil1", "feuil2", "cm1 charts", "graphique des resultats"):
                    continue
                side = side_of(rel) if side_of(rel) != "?" else side_of(ws.title)
                anchor_cols = find_anchor_cols(rows)
                drows = data_rows(rows, anchor_cols)
                ndata = len(drows)
                if ndata == 0:
                    continue
                school_j = find_school_col(rows)

                # --- aggregate Metrics tabs: school-level counts (Insrites/Presentes/Admises/Abandon) ---
                if "metric" in fold(ws.title):
                    agg_found = {}
                    for ak, kws in AGG_COLS.items():
                        j, hdr = match_family_col_best(rows, drows, kws, max_len=30)
                        if j is not None:
                            agg_found[ak] = (j, hdr)
                            colmap_rows.append([Path(rel).name, ws.title, ak, hdr, "aggregate metrics tab"])
                    if agg_found:
                        # school coverage = schools with a non-empty Inscrites/Admises count
                        key_col = agg_found.get("agg_inscrites") or agg_found.get("agg_admises")
                        nsch = ndata
                        filled = 0
                        if key_col:
                            kc = key_col[0]
                            filled = sum(1 for r in drows if kc < len(r) and not is_empty(r[kc]))
                        covered = ", ".join(sorted(a.replace("agg_", "") for a in agg_found))
                        summary_rows.append([cohort, level, side, Path(rel).name, ws.title,
                                             "Aggregate_Metrics",
                                             round(100 * filled / nsch, 1) if nsch else 0,
                                             round(100 * filled / nsch, 1) if nsch else 0,
                                             "; ".join(f"{k}={v[1]}" for k, v in agg_found.items())[:120],
                                             f"school-level counts: {covered}"])
                    # Metrics tabs hold only aggregates; skip girl-level family scan for them
                    continue

                # locate score columns (pre/post-aware) and other families
                located = {}
                ambiguities = []
                for subj, kws in SCORE_SUBJECTS.items():
                    sc = classify_scores(rows, kws)
                    located[f"pre_{subj}"] = sc["pre"] if sc["pre"] else (None, None)
                    located[f"post_{subj}"] = sc["post"] if sc["post"] else (None, None)
                    if sc["ambiguous"]:
                        ambiguities.append(f"{subj}: {sc['note']}")
                    for tag, val in (("pre_" + subj, sc["pre"]), ("post_" + subj, sc["post"])):
                        if val:
                            note = sc["note"] if sc["ambiguous"] else ""
                            colmap_rows.append([Path(rel).name, ws.title, tag, val[1],
                                                note])
                for fam, kws in FAMILIES.items():
                    cap = 60 if fam in ("college", "eoy_status") else 40
                    j, hdr = match_family_col_best(rows, drows, kws, max_len=cap)
                    located[fam] = (j, hdr)
                    if j is not None:
                        colmap_rows.append([Path(rel).name, ws.title, fam, hdr, ""])

                # per family-group: coverage + fill, using the best atomic column present
                for grp, members in FAMILY_GROUPS.items():
                    cols = [located[m][0] for m in members if located[m][0] is not None]
                    if not cols:
                        summary_rows.append([cohort, level, side, Path(rel).name, ws.title,
                                             grp, "0", "0", "(none found)", "column not found"])
                        continue

                    grp_note = ""
                    if grp == "Gov_Terms":
                        # report how many of the 3 terms are present, and mean fill across them
                        terms_found = [m for m in ("gov_t1", "gov_t2", "gov_t3")
                                       if located.get(m, (None,))[0] is not None]
                        grp_note = (f"{len(terms_found)}/3 terms"
                                    + (f" ({','.join(t[-2:] for t in terms_found)})" if terms_found else ""))
                        term_cols = [located[m][0] for m in ("gov_t1", "gov_t2", "gov_t3")
                                     if located.get(m, (None,))[0] is not None]
                        if term_cols:
                            per = [100 * sum(1 for r in drows if c < len(r) and not is_empty(r[c])) / ndata
                                   for c in term_cols]
                            fill_pct = round(sum(per) / len(per), 1)
                        else:
                            fill_pct = 0.0
                    elif grp == "Gov_Avg":
                        which = "CFEPD" if located.get("cfepd", (None,))[0] is not None else ""
                        which = (which + " + " if which and located.get("gov_avg", (None,))[0] is not None else which)
                        which = which + ("Moyenne" if located.get("gov_avg", (None,))[0] is not None else "")
                        grp_note = f"avg: {which}" if which else ""
                        filled = 0
                        for r in drows:
                            if any(c < len(r) and not is_empty(r[c]) for c in cols):
                                filled += 1
                        fill_pct = round(100 * filled / ndata, 1)
                    else:
                        # fill rate: a row 'has' the group if ANY member col is non-empty
                        filled = 0
                        for r in drows:
                            if any(c < len(r) and not is_empty(r[c]) for c in cols):
                                filled += 1
                        fill_pct = round(100 * filled / ndata, 1)

                    # COLLEGE: also report fill among transition-ELIGIBLE girls only
                    # (EOY status = passe/admis). A blank for an abandon/redouble girl is
                    # expected, not a gap. Eligible-only fill is the meaningful number.
                    if grp == "College_Tracking":
                        eoy_j = located.get("eoy_status", (None,))[0]
                        if eoy_j is not None:
                            elig = []
                            for r in drows:
                                ev = fold(r[eoy_j]) if eoy_j < len(r) and r[eoy_j] not in (None, "") else ""
                                if "pass" in ev or "admis" in ev:
                                    elig.append(r)
                            if elig:
                                ef = sum(1 for r in elig
                                         if any(c < len(r) and not is_empty(r[c]) for c in cols))
                                elig_pct = round(100 * ef / len(elig), 1)
                                note2 = f"eligible-only (passe/admis): {elig_pct}% of {len(elig)}"
                                grp_note = (grp_note + " | " + note2) if grp_note else note2
                            else:
                                grp_note = (grp_note + " | no passe/admis rows to condition on") if grp_note else "no passe/admis rows to condition on"
                        else:
                            grp_note = (grp_note + " | (EOY col not found in sheet; raw fill only)") if grp_note else "(EOY col not found; raw fill only)"

                    # DIAGNOSTIC for LFF: if header(s) found but fill is 0%, the column
                    # exists but reads empty. Record the first values seen so the user can
                    # tell 'truly empty (ask Inspection to populate)' from 'audit misread rows'.
                    if cols and fill_pct == 0.0:
                        peek = []
                        for c in cols:
                            sample = [r[c] for r in drows[:8] if c < len(r)]
                            peek.append(f"col{c}={[str(v)[:8] for v in sample]}")
                        diag = "HEADER FOUND, 0% fill — sample: " + " ; ".join(peek)
                        grp_note = (grp_note + " | " + diag) if grp_note else diag

                    # school coverage
                    cov_pct = ""
                    if school_j is not None:
                        schools = defaultdict(lambda: False)
                        for r in drows:
                            sval = r[school_j] if school_j < len(r) else None
                            if is_empty(sval):
                                continue
                            sk = fold(sval)
                            if any(c < len(r) and not is_empty(r[c]) for c in cols):
                                schools[sk] = True
                            else:
                                schools.setdefault(sk, False)
                        if schools:
                            cov = sum(1 for v in schools.values() if v)
                            cov_pct = round(100 * cov / len(schools), 1)
                            # per-school detail
                            for r in drows:
                                sval = r[school_j] if school_j < len(r) else None
                                if is_empty(sval):
                                    continue
                                key = (cohort, level, side, str(sval).strip())
                                has = any(c < len(r) and not is_empty(r[c]) for c in cols)
                                prev = perschool[key].get(grp, 0)
                                # store max fill (1 if any row for that school has it)
                                perschool[key][grp] = max(prev, 100 if has else 0)
                    matched = "; ".join(f"{m}={located[m][1]}" for m in members
                                        if located[m][0] is not None)[:120]
                    summary_rows.append([cohort, level, side, Path(rel).name, ws.title,
                                         grp, cov_pct, fill_pct, matched, grp_note])
            wb.close()

    # ---------------- write workbook ----------------
    FONT = "Arial"
    hdr_fill = PatternFill("solid", fgColor="2F5496")
    hdr_font = Font(name=FONT, bold=True, color="FFFFFF", size=10)
    thin = Side(style="thin", color="BFBFBF")
    border = Border(left=thin, right=thin, top=thin, bottom=thin)

    def pct_fill(v):
        try:
            x = float(v)
        except (TypeError, ValueError):
            return PatternFill("solid", fgColor="F2F2F2")
        if x >= 90:
            return PatternFill("solid", fgColor="C6EFCE")   # green
        if x >= 50:
            return PatternFill("solid", fgColor="FFEB9C")   # amber
        if x > 0:
            return PatternFill("solid", fgColor="FFC7CE")   # red
        return PatternFill("solid", fgColor="F2DCDB")       # pale red (0)

    wb = Workbook()
    ws = wb.active
    ws.title = "Summary"
    cols = ["Cohort", "Level", "Side", "File", "Sheet", "Data Family",
            "School Coverage %", "Fill Rate %", "Matched Column(s)", "Note"]
    for j, c in enumerate(cols, 1):
        cell = ws.cell(1, j, c); cell.fill = hdr_fill; cell.font = hdr_font
        cell.alignment = Alignment(horizontal="center", wrap_text=True); cell.border = border
    for i, row in enumerate(summary_rows, 2):
        for j, v in enumerate(row, 1):
            cell = ws.cell(i, j, v); cell.font = Font(name=FONT, size=9); cell.border = border
            cell.alignment = Alignment(vertical="top", wrap_text=(j in (9, 10)))
            if j in (7, 8):
                cell.fill = pct_fill(v)
    for j, w in enumerate([7, 7, 12, 30, 22, 16, 13, 11, 40, 26], 1):
        ws.column_dimensions[get_column_letter(j)].width = w
    ws.freeze_panes = "A2"

    # Per-school sheet
    ws2 = wb.create_sheet("Per-School")
    groups = list(FAMILY_GROUPS.keys())
    head2 = ["Cohort", "Level", "Side", "School"] + [f"{g} %" for g in groups]
    for j, c in enumerate(head2, 1):
        cell = ws2.cell(1, j, c); cell.fill = hdr_fill; cell.font = hdr_font
        cell.alignment = Alignment(horizontal="center", wrap_text=True); cell.border = border
    r = 2
    for (cohort, level, side, school), fams in sorted(perschool.items()):
        ws2.cell(r, 1, cohort).font = Font(name=FONT, size=9)
        ws2.cell(r, 2, level).font = Font(name=FONT, size=9)
        ws2.cell(r, 3, side).font = Font(name=FONT, size=9)
        ws2.cell(r, 4, school).font = Font(name=FONT, size=9)
        for k, g in enumerate(groups, 5):
            v = fams.get(g, 0)
            cell = ws2.cell(r, k, v); cell.font = Font(name=FONT, size=9)
            cell.fill = pct_fill(v); cell.border = border
        for j in range(1, 5):
            ws2.cell(r, j).border = border
        r += 1
    for j, w in enumerate([7, 7, 12, 28, 16, 14, 12, 16], 1):
        ws2.column_dimensions[get_column_letter(j)].width = w
    ws2.freeze_panes = "E2"

    # Column Map sheet (VERIFY)
    ws3 = wb.create_sheet("Column Map (VERIFY)")
    for j, c in enumerate(["File", "Sheet", "Family", "Matched Header", "Note (verify if present)"], 1):
        cell = ws3.cell(1, j, c); cell.fill = hdr_fill; cell.font = hdr_font; cell.border = border
    for i, row in enumerate(colmap_rows, 2):
        for j, v in enumerate(row, 1):
            cell = ws3.cell(i, j, v); cell.font = Font(name=FONT, size=9)
            if j == 5 and v:
                cell.fill = PatternFill("solid", fgColor="FFEB9C")  # amber-flag ambiguous
    for j, w in enumerate([34, 24, 14, 40, 38], 1):
        ws3.column_dimensions[get_column_letter(j)].width = w
    ws3.freeze_panes = "A2"

    wb.save(OUTPUT)
    print(f"Wrote {OUTPUT}")
    print(f"  Summary rows: {len(summary_rows)} | Per-school rows: {len(perschool)} | "
          f"Column-map rows: {len(colmap_rows)}")
    print("  >> CHECK the 'Column Map (VERIFY)' sheet first: confirm each family matched "
          "the RIGHT column before trusting any %.")


if __name__ == "__main__":
    audit()
