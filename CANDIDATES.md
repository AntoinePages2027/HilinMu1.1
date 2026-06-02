# Hilin Mu — Master Dataset Candidate Files (C4–C7)

**Purpose.** This file tells you, for each cohort × class level, **which file in this
repo is the canonical source** to use for the master reconstruction — and which files
are supplementary (kept for provenance, not for the build). Analysis unit is
**school-level** (school × cohort × side), per the RCT analysis plan.

Outcomes targeted (per analysis plan): dropout % (TAUX D'ABANDON), secondary-exam
pass % (TAUX DE REUSSITE / CFEPD), secondary enrollment % (TAUX D'INSCRIPTION),
plus Math and French scores (baseline & endline, CM1 and CM2).

Cohort → year: C4 = 2021–22 · C5 = 2022–23 · C6 = 2023–24 · C7 = 2024–25.

---

## ESSENTIAL — canonical sources for the master build

### Cohort 4 (2021–22)
- **CM1 — `Cohort4/CM1/sources/C4_CM1_Marcus_BaseDeDonnees_IntCtrl.xlsx`**
  Full intervention + control, baseline/endline Math & French, EOY status, plus a
  primary-matching tab. ~1004 int / 855 ctrl.
- **CM2 — `Cohort4/CM2/sources/C4_CM2_Marcus_AllComplete_4ExtraSchools.xlsx`**
  Richest C4 file: baseline AND endline blocks, CFEPD exam compositions (1ère/2è/3è),
  three EOY-status years (2022/2023/2024), weekly attendance (dosage), and **4 extra
  control-school sheets** (Kara Kara 2, Riadi Centre 2, Imbelbelou 3, Dallia) absent
  from the older "AlmostComplete" version.
  *Known defect:* the `Moyenne générale` column shows `#VALEUR!` in control / extra-school
  sheets (formula error in source). Recompute from the three composition columns.

### Cohort 5 (2022–23, pilot — Saé Saboua)
- **CM1 — `Cohort5/CM1/sources/C5_CM1_BaseDeDonnees_IntCtrl_931_743.xlsx`**
  931 int / 743 ctrl, baseline + EOY + a 2023 matching tab.
- **CM2 — `Cohort5/CM2/sources/C5_CM2_BasePhasePilote_EOY_CollegeTracking.xlsx`**
  Pre/post tests, EOY status, and college tracking all populated.
  *Known defect:* the `Identifiant Unique` column carries `#REF!` / `#ERROR!` on the
  first intervention rows. Irrelevant for school-level work (we don't join on girl ID),
  but flag if ever used at girl level.

### Cohort 6 (2023–24)
- **CM1 — `Cohort6/CM1/sources/C6_CM1_SituationFinAnnee_AllCommunes.xlsx`**
  EOY 2024 status for ~1,412 girls across all communes. (Marcus C6 CM1 file kept as backup.)
  *Note:* no girl ID; school + name only. Has EOY status, not baseline/endline scores.
- **CM2 — this is a SET, not one file** (C6 CM2 was never consolidated into a single workbook):
  - `Cohort6/CM2/sources/C6_CM2_Interv_Pre_Post_TestScores.xlsx` — intervention baseline/endline
    (girl-level, with `Identifiant Unique`).
  - Per-commune EOY/GovScores files (CM1-promotion + CM2/CFEPD outcomes):
    `C6_CM2_Tibiri_Interv_…`, `C6_CM2_Tibiri_Control_…`, `C6_CM2_Djirataoua_Interv_…`,
    `C6_CM2_Djirataoua_Control_…`, `C6_CM2_Safo_Interv_…`, `C6_CM2_Safo_Control_…`,
    `C6_CM2_Sae_Saboua_Interv_…`, `C6_CM2_Sae_Saboua_Control_…`.
  - College-tracking files (secondary enrollment / orientation):
    `C6_CM2_Tibiri_Control_CollegeTracking`, `C6_CM2_Djirataoua_Control_CollegeTracking`,
    `C6_CM2_Safo_Control_CollegeTracking`.
  - **Pair structure — `C6_CM2_PairMatching_OFFICIAL_MarcusZip.xlsx`** (the real LFF doc,
    "Matching des écoles pour cohorte 6, 2023-2024"). Authoritative for *pairing*; school
    names are abbreviated, so use source files for canonical spelling.
  *Each per-commune file also has a `CM1 & CM2 Metrics` tab* with school-level
  inscrites/admises/abandon counts — directly usable as event-study inputs.

### Cohort 7 (2024–25)
- **CM1 — `Cohort7/CM1/sources/C7_CM1_TX_CTRL_prepost_status_CANONICAL.xlsx`**
  ~2,345 girls all communes; side via `groupIC2` (0/1), baseline/endline Math & French,
  `status25` (0=abandon / 1=presente / 2=death). Two trailing sheets (`CM1 charts`,
  `Sheet2`) are analysis scratch — ignore.
- **CM2 — `Cohort7/CM2/sources/C7_CM2_TX_CTRL_prepost_mentor.xlsx`**
  ~1,381 rows; pre/post, mentor column; control EOY 2024-25 in the `Groupe Controle CM2`
  sheet (note: that sheet has stacked/merged headers — read carefully).
  - **College tracking — `Cohort7/CM2/sources/C7_CM2_All_CollegeTracking.xlsx`**
    (secondary enrollment: presente / abandonner / transferee / decedee).
  - **Pair structure — `Cohort7/CM2/sources/C7_CM2_PairMatching_clean_spreadsheet.xlsx`**
    (52 pairs; Tchadoua pairs 41–52 are CM1-only, no CM2 outcomes for 2024-25).

---

## SUPPLEMENTARY — kept for provenance, NOT for the build

- All `*_provenance.xlsx` files (raw/intermediate snapshots of the canonical files above).
- `Cohort4/CM2/sources/HilinMu_C4_CM2_All_AlmostComplete.xlsx` — superseded by the Marcus
  AllComplete file (lacks the 4 extra control schools and the multi-year EOY).
- `Cohort6/CM2/sources/C6_CM2_PairMatching_PROXY.xlsx` — placeholder (C5 matching tab);
  superseded by the OFFICIAL matching doc above.
- Content-identical C5 CM2 duplicates (`HilinMu_C5_CM2_All_Complete`, `2023-08-10 Base…`).
- `Cohort7/CM1/sources/C7_CM1_Tchadoua.xlsx` — school-level rate/ranking tabs only; girl-level
  Tchadoua data is subsumed by the C7 CM1 canonical. Useful for pre-computed Tchadoua summaries.
- Everything under `_built/` — earlier assembled masters, kept as references.

---

## KNOWN DATA GAPS (the remaining LFF ask)

- **C6 control schools with no data anywhere:** Safo Chadaoua, Radi Centre 1, Radi Centre 2,
  Radi Quartier (Safo), Karambi Saboua (Saé Saboua).
- **C6 CM2 still missing** for Soura Saraki and Maza Tsaye 2 (CM1 found, CM2 not).
- **C7:** zero schools missing (all pairs resolved).

## KNOWN DEFECTS TO HANDLE IN THE BUILD

- C4 CM2 control/extra sheets: `#VALEUR!` in `Moyenne générale` — recompute.
- C5 CM2 intervention: `#REF!`/`#ERROR!` in `Identifiant Unique` — irrelevant at school level.
- Status labels vary across files (Passe / Passante / Passe au CM2 / Redouble / Orientée CEG /
  Orientée CFM / Absante / Transferée / non Admise …) — normalize before computing rates.
- School-name spellings vary across files — resolve via the school-name crosswalk
  (`school_name_crosswalk_REVIEW.xlsx`) before merging.

*Last updated from full header-inventory verification of all 65 repo files.*
