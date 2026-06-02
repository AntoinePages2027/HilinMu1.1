# Hilin Mu: Master Dataset Source Repository (Cohorts 4-7)

Canonical source, built, and reference files for the Hilin Mu RCT master-dataset
reconstruction, organized by cohort and grade level (CM1 / CM2). Analysis unit is
**school-level** (school × cohort × side).

## Where to look
- **`CANDIDATES.md`** - a tentative list of which file is essential (canonical
  source) vs. supplementary, per cohort × level. **Start here.**
- **`provenance_flagged.csv`** - every file with its source, hash, per-sheet row counts,
  and a `master_doc_candidate` TRUE/FALSE flag.
- **`_shared/canonical_mapping_v2.txt`** - working school-name crosswalk (crosswalk = standardized mapping). Needs confirmation from LFF.
- **`school_name_crosswalk_REVIEW.xlsx`** - working crosswalk (full classification + review queue).

## Layout
```
CohortN/CM1/sources   CohortN/CM2/sources   CohortN/CM2/built   _built/   _shared/
```
Each canonical file is also kept under its original LFF filename for provenance;
`provenance_flagged.csv` ties the two together by hash.

## Completeness for master reconstruction (C4–C7)

| Cohort | CM1 | CM2 | Notes |
|--------|-----|-----|-------|
| **C4** (2021–22) |  complete | complete | Marcus files; CM2 has baseline+endline, CFEPD compositions, 3 EOY years, +4 extra control schools. |
| **C5** (2022–23, pilot) | complete | complete | Saé Saboua pilot; EOY + college tracking verified. |
| **C6** (2023–24) | Missing Pre-Post Test | Patrial Coverage for Pre-Post Test (~40%) | CM2 is a *set* of per-commune files (never consolidated). See gap below. |
| **C7** (2024–25) | complete | complete | Zero schools missing. |

**At school level, dropout / CFEPD-pass / secondary-enrollment outcomes are available for all of C4–C7 (minus the C6 school gap below). Math & French score outcomes are the exception for C6. CM2 control and cohort-wide CM1 pre/post are absent (see gap list).**

## Remaining data gap (the LFF ask)
- **C6 control schools with no data in any file:** Safo Chadaoua, Radi Centre 1,
  Radi Centre 2, Radi Quartier (Safo); Karambi Saboua (Saé Saboua).
- **C6 CM2 missing** for Soura Saraki and Maza Tsaye 2 (CM1 found, CM2 not).
- **C6 CM1 pre/post test** 
- **C7:** none outstanding thanks to recent dataset update provided by Sarah. 

## School-name standardization
- Tentative crosswalk: **`_shared/canonical_mapping_v2.txt`** (167 variant→canonical
  mappings, 80 canonicals). Built by fuzzy matching (commune-blocked, sibling-number
  protected) + manual review; `school_name_crosswalk_REVIEW.xlsx` is the working file.
- Confirmed: **Maza Tsaye** (no "n"), **Kontagora** (not Kantagora/Kountagora),
  **Radi** (not Riadi). Roman numerals normalized to arabic; sibling schools
  (Soura 1/2/3, etc.) kept distinct.
- **Pending LFF confirmation** (listed in the header of `canonical_mapping_v2.txt`):
  Danja (bare → which number), Dan Fillo (bare), Kountarou (distinct vs. Kountarou
  Mairairai), Kontagora Sofoua vs Kontagora Tsohoua, Takalmaoua (bare → which number),
  M.Saboua (= Mallamai Saboua?), Katare bare (= Guidan Ousmane 1 or 2?).

## Key merge notes
- **C6 CM2** is per-commune: pull EOY/CFEPD outcomes from the `*_EOY_Status_GovScores`
  files and secondary enrollment from the `*_CollegeTracking` files; each also has a
  `CM1 & CM2 Metrics` tab with school-level counts usable directly.
- **C6 matching:** `C6_CM2_PairMatching_OFFICIAL_MarcusZip.xlsx` is a real LFF doc
  ("Matching des écoles pour cohorte 6, 2023-2024"). Placeholder for *pairing* until further verification/confirmation from LFF; use
  source files for canonical spelling. (`_PROXY` retained as backup only.). 
  *Note:* LFF flagged a possible pairing error (Kalgon Waraou) — pairings pending correction.
- **C7 CM1 canonical:** drop footer rows lacking a `groupIC2` value (SD/count summaries).
- **Known defects:** C4 CM2 control sheets carry `#VALEUR!` in `Moyenne générale`
  (recompute); C5 CM2 intervention has `#REF!` in `Identifiant Unique` (irrelevant at
  school level). Status labels vary across files -> We must normalize before computing rates.

  **ALL MATCHING/PAIRING DOCS AWAITING VERIFICATION FROM LFF**

*Last updated after full header-inventory verification of all repo files and the
school-name standardization pass.*
