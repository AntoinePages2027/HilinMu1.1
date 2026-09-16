# Repo Update — July 2026 Session

## How to apply

```bash
cd /path/to/HilinMu1.1
unzip repo_update_july2026.zip    # extracts into current dir, preserving paths
git add -A
git commit -m "Add Cohort 8 sources + EOY, C4 Tarna college file, panel build C4-C8, pairing docs C4-C8, crosswalk v3, Column L / Table 1

Cohort 8:
- Intervention + Control bases (v5, pre-test duplication fixed in CM2 ctrl)
- 5 commune EOY files (June 2026 year-end, all girls parsed)
- Paired: 50 pairs from Cohorte 8 docx (canonical), 178/179 rows matched

C4 additions:
- Base Suivi 6e with Tarna college tracking (52/65 eligible girls) — closes last C4 gap
- Two pairing correction docs from Dec 2021

Panel build (_analysis/panel_build/):
- hm.py: shared helpers (canonical mapping, status crosswalk, aggregation)
- build_c4_v2.py through build_c78.py: per-cohort girl-level extraction
- hilinmu_school_panel_DRAFT.csv: 606 school-level rows, C4-C8, all outcomes
- hilinmu_coverage_grid.csv: non-null outcome counts by cohort x level x side
- HilinMu_ColonneL_Tableau1.xlsx: exposure classification + Table 1 by stratum

Pairing (_shared/pairing/):
- c4_pairs.csv through c8_pairs.csv: canonical pair lists from verified docs
- C4 correction docs (original Dec 2021 site-selection files)

Crosswalk updates (_shared/):
- canonical_mapping_v3.txt: v2 + 30 new name mappings (C8 commune-file variants)
- status_crosswalk_session_additions.csv: 8 new status entries (CET, Passse, etc.)

Known issues documented in panel:
- 18 legacy schools (C1-C3) misassigned as e=0; g must be corrected from master col G/I
- C4 CM1 rows = same girls as C4 CM2 (pre-treatment records, flagged)
- C4 'Passe en 6e' inscription = orientation only, not verified presence (flagged)
- C8 CM2 control pre-test duplication fixed in v5 but 3 schools still 100% identical
"
git push origin main
```

## File inventory (37 files)

### Cohort8/ (19 xlsx)
Sources: intervention base, control base v5, 5 commune EOY files (Djirataoua, Tchadoua, Tibiri, Safo, Saé Saboua)
master_candidates/: same files promoted per CANDIDATES convention

### Cohort4/CM2/sources/ (1 xlsx)
C4_CM2_CollegeTracking_BaseSuivi6e_incl_Tarna.xlsx — the missing Tarna college tracking

### _analysis/panel_build/ (9 files)
Build scripts (hm.py, build_c4_v2.py, build_c5.py, build_c6.py, build_c78.py)
Panel CSV + coverage grid + C4 intermediate + Column L workbook

### _shared/ (8 files)
pairing/: c4-c8_pairs.csv + 2 C4 pairing docs
canonical_mapping_v3.txt, status_crosswalk_base.csv, status_crosswalk_session_additions.csv
