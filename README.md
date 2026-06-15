# Hilin Mu: Master Dataset Source Repository (Cohorts 4-7)

Canonical source, built, and reference files for the Hilin Mu RCT master-dataset
reconstruction, organized by cohort and grade level (CM1 / CM2). Analysis unit is
**school-level** (school × cohort × side).

## Where to look
- **`COMPLETENESS.md`** - authoritative per-cohort data completeness across the four
  data families (pre/post scores, gov scores, EOY status, college tracking), with the
  source file for each and the confirmed gaps to raise with LFF. **Start here for "what
  data do we have."**
- **`CANDIDATES.md`** - a tentative list of which file is essential (canonical
  source) vs. supplementary, per cohort × level.
- **`provenance_flagged.csv`** - every file with its source, hash, per-sheet row counts,
  and a `master_doc_candidate` TRUE/FALSE flag.
- **`data_completeness_audit.xlsx`** / **`audit_completeness.py`** - the reproducible
  audit (per-file column detection + fill rates, incl. eligible-only college metric) that
  `COMPLETENESS.md` is built from.
- **`_shared/canonical_mapping_v2.txt`** - working school-name crosswalk (crosswalk = standardized mapping). Needs confirmation from LFF.
- **`school_name_crosswalk_REVIEW.xlsx`** - working crosswalk (full classification + review queue).

## Layout
```
CohortN/CM1/sources   CohortN/CM2/sources   CohortN/CM2/built   _built/   _shared/
```
Each canonical file is also kept under its original LFF filename for provenance;
`provenance_flagged.csv` ties the two together by hash.

## Completeness summary

Full detail, per cohort × level × side, is in **`COMPLETENESS.md`** (the single source of
truth — do not duplicate its table here). In brief:

- **Dropout / CFEPD-pass / secondary-enrollment (EOY + college)** outcomes are available
  across C4–C7 at school level. College tracking, measured among transition-eligible girls
  (EOY = passe/admis), is complete or near-complete everywhere (apparent low raw fill was
  girls who did not transition).
- **Pre/Post test scores** are complete for C4, C5, C7; the exception is **C6** —
  intervention CM2 only, with control CM2 absent and CM1 cohort-wide only ~40% covered.
- **Gov scores** are present everywhere as at least the annual average; several files also
  carry the per-term breakdown. Some required pulling from sibling files (e.g. C5 CM1
  EXAMENS, C7 CM1 Resultats, C7 CM2 consolidated).

**Confirmed gaps for the LFF / Inspection visit** (see `COMPLETENESS.md` for the full list
and phrasing): C6 CM2 control pre/post (confirmed absent); C6 CM1 cohort-wide pre/post
(~40%); C4 CM2 college for the **Tarna** schools; C6 control schools with no data (Safo
Chadaoua, Radi Centre 1/2/Quartier, Karambi Saboua) and C6 CM2 missing for Soura Saraki &
Maza Tsaye 2; school-name confirmations; and the Kalgon Waraou pairing.

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

*Last updated after the data-completeness audit and the school-name standardization pass.*
