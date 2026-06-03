# Hilin Mu — Data Completeness for Master Reconstruction (C4–C7)

Per-cohort completeness across the four data families needed for analysis:
**Pre/Post test scores** (baseline + endline Math & French), **Gov scores**
(term evaluations + annual average / CFEPD), **EOY status** (promotion / dropout /
orientation), and **College tracking** (secondary enrollment). Analysis unit is
**school-level** (school × cohort × side).

Verdicts: **complete** (≥90% fill, both arms) · **usable** (present, 50–90% or one
arm stronger) · **partial** (present but sparse / one arm only) · **gap** (absent).

Figures come from the repo data-completeness audit (`data_completeness_audit.xlsx`),
cross-checked against manual inspection of the key files. Where a family is supplied by
a file other than the primary candidate, the source is named in the appendix.

---

## Headline completeness

| Cohort | Level | Side | Pre/Post Scores | Gov Scores | EOY Status | College Tracking |
|--------|-------|------|-----------------|------------|------------|------------------|
| **C4** | CM1 | intervention | 100% complete | avg 100% complete; terms gap | 96% complete | N/A (CM1) |
| **C4** | CM1 | control | 100% complete | avg 100% complete; terms partial | 83% usable | N/A (CM1) |
| **C4** | CM2 | intervention | 99% complete | avg + 3/3 terms 96% complete | 100% complete | 91% elig.¹ |
| **C4** | CM2 | control | 100% complete | 2/3 terms 95% usable | 99% complete | 100% elig.¹ |
| **C5** | CM1 | intervention | 97% complete | avg 100% + 3/3 terms 96% complete | 98% complete | N/A (CM1) |
| **C5** | CM1 | control | 99% complete | avg 100% + 3/3 terms 95% complete | 98% complete | N/A (CM1) |
| **C5** | CM2 | intervention | 97% complete | avg + 3/3 terms 100% complete | 99% complete | 100% elig.³ |
| **C5** | CM2 | control | 100% complete | avg 100% + 3/3 terms 83% complete | 98% complete | 100% elig.³ |
| **C6** | CM1 | both | intervention-only (partial) | avg 99% (Marcus file) | 100% complete (EOY file) | N/A (CM1) |
| **C6** | CM2 | intervention | 99% complete | avg + 2/3 terms ~100% complete | 100% complete | usable (aggregate) |
| **C6** | CM2 | control | **gap** | avg + 2/3 terms ~96% usable | ~95% complete | usable (aggregate) |
| **C7** | CM1 | both | 100% complete | avg 99% complete² | 100% complete² | N/A (CM1) |
| **C7** | CM2 | intervention | 98% complete | avg/CFEPD 96% + terms usable | 100% complete | 100% elig.³ |
| **C7** | CM2 | control | 87% usable | avg/CFEPD 92% + terms usable | 99% complete | 100% elig.³ |

**Reading the table.** *N/A (CM1)* = college tracking is not applicable at CM1 — secondary-
school transition happens after CM2, so CM1 files are not expected to carry it (its absence
is by design, not a gap). CFEPD likewise is a CM2 terminal exam and is N/A at CM1.

¹ **C4 CM2 college tracking is split across two files, and the meaningful figure is
eligible-only.** The Marcus canonical (`C4_CM2_Marcus_AllComplete_4ExtraSchools`) has
scores/EOY/the 4 extra control schools but **no college column**. College tracking
(`Situation … suivi des filles au college`, "Passe en 6e" etc.) lives only in the
supplementary `HilinMu_C4_CM2_All_AlmostComplete`. Raw fill is 58% (int) / 61% (ctrl), but
restricted to **transition-eligible girls (EOY = passe/admis)** it is **90.9% (int) /
99.6% (ctrl)** — i.e. near-complete. The shortfall on intervention is concentrated in the
**Tarna schools** (54 eligible Tarna girls, 0 with college data) — the one residual gap.
C4 CM2 thus needs both files (Marcus for scores + extra schools; AlmostComplete for college).

³ **College tracking is reported eligible-only** where computable: the % of
*transition-eligible* girls (end-of-year status = passe/admis) who have college data. A
blank for a girl who dropped out (Abandon) or repeated (Redouble) is expected — she did not
transition to collège — so it is not a gap. Raw fill (counting all girls) is much lower
(e.g. C5 control 37% raw → 100% eligible) and understates completeness; the eligible-only
figure is the meaningful one. Where the EOY column uses non-passe/admis vocabulary (some C6
files) the metric could not be auto-computed and raw fill is shown — those raw figures are
already high (75–100%).

² **C7 CM1 gov scores and EOY** come from sibling files, not the pre/post canonical
(`C7_CM1_TX_CTRL_prepost_status`, which has pre/post only). `C7_CM1_Resultats_FinAnnee`
supplies the annual average (99.5%), term scores, and EOY status (100%);
`C7_CM1_Consolidated2` additionally combines pre/post with the term scores in one sheet
(note: its EOY status labels have a UTF-8 encoding issue — e.g. "R√©doublante" — that
needs a cleanup pass before label normalization).

**Bottom line.** Dropout / pass / orientation (EOY) and college tracking (at CM2) are
available across cohorts at school level. Pre/Post scores are complete for C4, C5, C7 and
C6 intervention CM2. The genuine, potentially-recoverable gaps are few — see the LFF ask.

---

## Per-source appendix (which file supplies each family)

### Cohort 4
- **CM1** — `C4_CM1_Marcus_BaseDeDonnees_IntCtrl`: pre/post 100%, gov *average* ~100%
  both arms; **gov term-breakdown columns present but empty** (intervention) / sparse
  (control). EOY 83–96%. No college-tracking column.
- **CM2** — `C4_CM2_Marcus_AllComplete_4ExtraSchools`: pre/post 99–100%, gov terms
  (1ère/3è composition) ~95%, EOY ~100%. 4 extra control schools included. **No college
  column** — for C4 CM2 college tracking, use the supplementary
  `HilinMu_C4_CM2_All_AlmostComplete` file (`Situation … suivi des filles au college`,
  ~58% int / ~61% ctrl, "Passe en 6e" etc.), but note **Tarna schools have no college data
  there**. C4 CM2 thus needs both files (Marcus for scores + extra schools; AlmostComplete
  for college), analogous to the C6 CM2 multi-file structure.

### Cohort 5
- **CM1** — **use `HILIN_MU_C5_CM1_EXAMENS_08_08_2023`** (not the `…931_743` candidate,
  whose gov-term and EOY columns are empty). EXAMENS file: pre/post 97–99%, gov average
  ~100%, **3/3 composition terms 95–96% both arms**, EOY 98%. No college column.
- **CM2** — `C5_CM2_BasePhasePilote_EOY_CollegeTracking`: pre/post 97–100%, gov avg 100%,
  3/3 terms (intervention 100% / control 83%), EOY 98%, **college: intervention 87%,
  control 37% (sparse)**.

### Cohort 6
- **CM1** — `C6_CM1_SituationFinAnnee_AllCommunes`: EOY status 100% (1,412 girls, all
  communes). Pre/post scores only in `C6_CM1_Marcus_BaseDeDonnees` (~556 rows, <40% of
  cohort) — partial. Gov average present in the Marcus file (~99%).
- **CM2** — a per-commune SET. Each commune's `… _EOY_Status_GovScores` and
  `…_CollegeTracking` files supply gov scores (avg + 1er/2e terms, 57–100%), EOY
  (90–100%), and college (CEG/CFM orientation). Each also has a **`CM1 & CM2 Metrics`
  aggregate tab at 100%** giving school-level inscrites / présentes / admises / abandon —
  directly usable for dropout & pass rates. **Pre/Post test scores: intervention only
  (`C6_CM2_Interv_Pre_Post_TestScores`, 99%); control pre/post absent.**

### Cohort 7
- **CM1** — `C7_CM1_TX_CTRL_prepost_status_CANONICAL`: pre/post 100% both arms
  (basemaths/endmaths, basefrançais/endfrançais). **Gov scores + EOY come from sibling
  files:** `C7_CM1_Resultats_FinAnnee` (Moyenne Annuelle 99.5%, term scores, EOY status
  100%) and `C7_CM1_Consolidated2` (pre/post + term scores combined; EOY labels have an
  encoding issue to clean). College tracking N/A at CM1.
- **CM2** — **use `C7_CM2_All_Pre_Post_TestScores_GovScores_EOY`** (consolidated, both arms
  in one `group` 0/1 column): pre/post (int 97% / ctrl 87%), gov terms (Moyenne 1er/2e
  strong, 3e sparse ~32–42%), **CFEPD score 99% int / 92% ctrl**, EOY (Yearendoutcome)
  ~100%. College tracking from `C7_CM2_All_CollegeTracking` (int 100% / ctrl 84%). The
  `…prepost_mentor` file lacks CFEPD — the consolidated file supersedes it for gov/CFEPD.

---

## LFF ask — confirmed gaps to raise at the Inspections

College tracking and CFEPD at CM1 are **not applicable** (no secondary transition until
after CM2) and are excluded below. The genuine gaps:

1. **C6 CM2 control — pre/post Math & French test scores.** CONFIRMED MISSING (per Sarah):
   baseline/endline tests do not exist for the C6 control schools. Affects the Math/French
   score outcomes for the C6 control arm only.

2. **C6 CM1 — cohort-wide pre/post test scores.** The full-coverage C6 CM1 file has EOY
   status only; the file with score columns covers <40% of the cohort. Do complete C6 CM1
   baseline/endline scores exist?

3. **C4 CM2 — college tracking for Tarna schools.** College tracking for C4 CM2 is
   near-complete for transition-eligible girls (90.9% int / 99.6% ctrl), but the **Tarna
   schools are the exception: 54 eligible Tarna girls have no college data.** Was
   secondary follow-up done for the Tarna schools in 2021–22?

4. **C6 control schools missing entirely** (no data in any file): Safo Chadaoua, Radi
   Centre 1, Radi Centre 2, Radi Quartier (Safo); Karambi Saboua (Saé Saboua). Plus C6 CM2
   missing for Soura Saraki and Maza Tsaye 2.

5. **School-name confirmations** (from standardization; see `canonical_mapping_v2.txt`):
   Danja / Dan Fillo / Takalmaoua bare numbers; Kountarou vs Kountarou Mairairai;
   Kontagora Sofoua vs Tsohoua; M.Saboua; Katare 1/2.

6. **Pairing correction.** LFF flagged a possible C6 matching error (Kalgon Waraou) —
   confirm the correct intervention/control pairing.

*Note: college tracking is otherwise complete — apparent shortfalls in raw fill were girls
who did not transition (Abandon/Redouble), for whom a blank is correct. Measured among
transition-eligible girls, C5 and C7 college tracking are 100% and C4 is near-complete
(Tarna excepted). C5 CM2 control college, previously flagged at 37%, is in fact 100% of
eligible girls — not a gap.*

*Built from `data_completeness_audit.xlsx` (verified column detection + fill measurement)
and manual inspection of the C5 CM1 EXAMENS and C7 CM2 consolidated files. CM1 college
tracking / CFEPD treated as not-applicable by program structure.*
