# Hilin Mu — Master Dataset Source Repository (Cohorts 4–7)

Canonical source, built, and reference files for the Hilin Mu RCT master-dataset
reconstruction, organized by cohort and grade level (CM1 / CM2).

## Layout
```
CohortN/CM1/sources   CohortN/CM2/sources   CohortN/CM2/built   _built/   _shared/
```

## Known gaps & decisions
- **C6 CM2:** 10 control schools confirmed absent from ALL existing files (incl. Marcus's zip). Must come from the LFF Niger team.
- **C6 CM2 matching:** `C6_CM2_PairMatching_PROXY.xlsx` is a PLACEHOLDER (Matching 2023 tab from the C5 CM1 base). Replace with the official LFF doc when received.
- **C4 CM2:** canonical = Marcus 'after cleaning' file (has Kara Kara 2 / Riadi Centre 2 / Imbelbelou 3 / Dallia).
- **C5 CM1:** `C5_CM1_BaseDeDonnees_IntCtrl_931_743.xlsx`; its Matching 2023 tab is the C6 proxy source.
- **C5 CM2:** canonical file verified to carry end-of-year status + college tracking.
- **C7 CM1:** RESOLVED. Canonical = TX+CTRL prepost file (2,345 girls, pre+post+status25). Merge rule: drop footer rows lacking a groupIC2 value (they are SD/count summaries).
- **_shared:** `canonical_mapping.txt` and `handoff_context.json` still to be added.

## File manifest
| Dest | Original | Hash | Note |
|------|----------|------|------|
| `Cohort4\CM1\sources\MD edits 2021-2022_Primaire Base de donnees Intervention, Controle_2022 (1) (version 1).xlsx` | MD edits 2021-2022_Primaire Base de donnees Intervention, Controle_2022 (1) (version 1).xlsx | e9c7aabe0c | Marcus File 3. Int 1005 / Ctrl 856. CANONICAL C4 CM1. |
| `Cohort4\CM1\sources\C4_CM1_Marcus_BaseDeDonnees_IntCtrl.xlsx` | MD edits 2021-2022_Primaire Base de donnees Intervention, Controle_2022 (1) (version 1).xlsx | e9c7aabe0c | Marcus File 3. Int 1005 / Ctrl 856. CANONICAL C4 CM1. |
| `Cohort4\CM1\sources\2022-02-22_Primaire Base de donnees Intervention & Controle_2021-2022 (1).xlsx` | 2022-02-22_Primaire Base de donnees Intervention & Controle_2021-2022 (1).xlsx | a88a92b4bc | Non-Marcus raw (Int 1051 / Ctrl 865). Provenance only. |
| `Cohort4\CM1\sources\C4_CM1_raw_Feb2022_provenance.xlsx` | 2022-02-22_Primaire Base de donnees Intervention & Controle_2021-2022 (1).xlsx | a88a92b4bc | Non-Marcus raw (Int 1051 / Ctrl 865). Provenance only. |
| `Cohort4\CM2\sources\MD Edits 2021-2022 Hilin Mu CM2 Base de donnees after cleaning 2021-2022 C4  .xlsx` | MD Edits 2021-2022 Hilin Mu CM2 Base de donnees after cleaning 2021-2022 C4  .xlsx | a83703d828 | Marcus File 2. CANONICAL C4 CM2 (Kara Kara 2 / Riadi Centre 2 / Imbelbelou 3 / Dallia). |
| `Cohort4\CM2\sources\C4_CM2_Marcus_AllComplete_4ExtraSchools.xlsx` | MD Edits 2021-2022 Hilin Mu CM2 Base de donnees after cleaning 2021-2022 C4  .xlsx | a83703d828 | Marcus File 2. CANONICAL C4 CM2 (Kara Kara 2 / Riadi Centre 2 / Imbelbelou 3 / Dallia). |
| `Cohort4\CM2\sources\HilinMu_C4_CM2_All_AlmostComplete.xlsx` | HilinMu_C4_CM2_All_AlmostComplete.xlsx | d38969cc5b | Your earlier pick. Missing the 4 extra control-school sheets. Provenance only. |
| `Cohort4\CM2\sources\C4_CM2_AlmostComplete_NO_extra_schools_provenance.xlsx` | HilinMu_C4_CM2_All_AlmostComplete.xlsx | d38969cc5b | Your earlier pick. Missing the 4 extra control-school sheets. Provenance only. |
| `Cohort4\CM2\built\HilinMu_C4_CM2_Merged_Database.xlsx` | HilinMu_C4_CM2_Merged_Database.xlsx | e977cae74f | Built artifact (Int 1000 / Ctrl 851). |
| `Cohort4\built\Cohort4_SubMaster.xlsx` | Cohort4_SubMaster.xlsx | 76a79e3ed6 | Built C4 paired sub-master. |
| `Cohort5\CM1\sources\C6_CM2_PairMatching.xlsx` | C6_CM2_PairMatching.xlsx | f7eb9ca82d | Full C5 CM1 DB (931 int / 743 ctrl) + Matching 2023. Matching tab also feeds C6 (see PROXY). |
| `Cohort5\CM1\sources\C5_CM1_BaseDeDonnees_IntCtrl_931_743.xlsx` | C6_CM2_PairMatching.xlsx | f7eb9ca82d | Full C5 CM1 DB (931 int / 743 ctrl) + Matching 2023. Matching tab also feeds C6 (see PROXY). |
| `Cohort5\CM1\sources\Suivi Base Phase pilote CM1.2022.xlsx` | Suivi Base Phase pilote CM1.2022.xlsx | 80c0c09fc3 | C5 CM1 pilot (Louloubi/Kadata/Barouana). |
| `Cohort5\CM1\sources\C5_CM1_Pilote_Suivi.xlsx` | Suivi Base Phase pilote CM1.2022.xlsx | 80c0c09fc3 | C5 CM1 pilot (Louloubi/Kadata/Barouana). |
| `Cohort5\CM2\sources\2023-08-10 Base Phase Pilote CM2(3).xlsx` | 2023-08-10 Base Phase Pilote CM2(3).xlsx | 3ff9dfcfa7 | CANONICAL C5 CM2. Verified: 'Situation (fin d'annee)' + 'Suivi des filles' (college) populated. |
| `Cohort5\CM2\sources\C5_CM2_BasePhasePilote_EOY_CollegeTracking.xlsx` | 2023-08-10 Base Phase Pilote CM2(3).xlsx | 3ff9dfcfa7 | CANONICAL C5 CM2. Verified: 'Situation (fin d'annee)' + 'Suivi des filles' (college) populated. |
| `Cohort5\CM2\sources\HilinMu_C5_CM2_All_Complete.xlsx` | HilinMu_C5_CM2_All_Complete.xlsx | 914b14e848 | Prior pick; EOY column could not be confirmed. Provenance only. |
| `Cohort5\CM2\sources\C5_CM2_All_Complete_provenance.xlsx` | HilinMu_C5_CM2_All_Complete.xlsx | 914b14e848 | Prior pick; EOY column could not be confirmed. Provenance only. |
| `Cohort6\CM1\sources\C6 Filles CM1 situation fin d'année.xlsx` | C6 Filles CM1 situation fin d'année.xlsx | a36717848d | CANONICAL C6 CM1 (1,414 girls, all communes, EOY status). |
| `Cohort6\CM1\sources\C6_CM1_SituationFinAnnee_AllCommunes.xlsx` | C6 Filles CM1 situation fin d'année.xlsx | a36717848d | CANONICAL C6 CM1 (1,414 girls, all communes, EOY status). |
| `Cohort6\CM1\sources\Marcus Edits 2023-2024 Hilin Mu CM1 BASE DE DONNEE 6 cohorte 062824.xlsx` | Marcus Edits 2023-2024 Hilin Mu CM1 BASE DE DONNEE 6 cohorte 062824.xlsx | 0b4decf711 | Marcus-cleaned C6 CM1 base. Supplementary. |
| `Cohort6\CM1\sources\C6_CM1_Marcus_BaseDeDonnees.xlsx` | Marcus Edits 2023-2024 Hilin Mu CM1 BASE DE DONNEE 6 cohorte 062824.xlsx | 0b4decf711 | Marcus-cleaned C6 CM1 base. Supplementary. |
| `Cohort7\CM1\sources\CM1_Consolidated2 121425.xlsx` | CM1_Consolidated2 121425.xlsx | 37b5f6affa | Superseded by TX+CTRL canonical. Provenance. |
| `Cohort7\CM1\sources\C7_CM1_Consolidated_PrePost_provenance.xlsx` | CM1_Consolidated2 121425.xlsx | 37b5f6affa | Superseded by TX+CTRL canonical. Provenance. |
| `Cohort7\CM1\sources\Données compilées Pré-test_Post-test CM1 et CM2 Hilin Mu C7 .xlsx` | Données compilées Pré-test_Post-test CM1 et CM2 Hilin Mu C7 .xlsx | 32cf369f2e | Superseded by TX+CTRL canonical. Provenance. |
| `Cohort7\CM1\sources\C7_CM1_Donnees_Compilees_PrePost_provenance.xlsx` | Données compilées Pré-test_Post-test CM1 et CM2 Hilin Mu C7 .xlsx | 32cf369f2e | Superseded by TX+CTRL canonical. Provenance. |
| `Cohort7\CM1\sources\Compilation données Note et situation fille Hilin Mu C7.xlsx` | Compilation données Note et situation fille Hilin Mu C7.xlsx | 6a9ce34ca6 | C7 CM1 note+situation (CM1 2257 / CM2 1294). Provenance. |
| `Cohort7\CM1\sources\C7_CM1_Compilation_Note_Situation_provenance.xlsx` | Compilation données Note et situation fille Hilin Mu C7.xlsx | 6a9ce34ca6 | C7 CM1 note+situation (CM1 2257 / CM2 1294). Provenance. |
| `Cohort7\CM1\sources\Les données de LFF Hilin Mu IEP de Tchadoua ( 2025).xlsx` | Les données de LFF Hilin Mu IEP de Tchadoua ( 2025).xlsx | c203db66cc | C7 CM1 Tchadoua outcomes. |
| `Cohort7\CM1\sources\C7_CM1_Tchadoua.xlsx` | Les données de LFF Hilin Mu IEP de Tchadoua ( 2025).xlsx | c203db66cc | C7 CM1 Tchadoua outcomes. |
| `Cohort7\CM1\sources\Résultats pré-test CM1 et CM2 HILIN MU cohorte 7 Intervention & Controle.xlsx` | Résultats pré-test CM1 et CM2 HILIN MU cohorte 7 Intervention & Controle.xlsx | e53b4decf3 | C7 pre-test only (CM1 1298 int / 1010 ctrl) + CM2. Provenance. |
| `Cohort7\CM1\sources\C7_CM1_CM2_PreTest_IntCtrl_provenance.xlsx` | Résultats pré-test CM1 et CM2 HILIN MU cohorte 7 Intervention & Controle.xlsx | e53b4decf3 | C7 pre-test only (CM1 1298 int / 1010 ctrl) + CM2. Provenance. |
| `Cohort7\CM2\sources\C7_Pair_Matching.xlsx` | C7_Pair_Matching.xlsx | 3db7ac5563 | Clean 53-row matching table (better than the .docx). |
| `Cohort7\CM2\sources\C7_CM2_PairMatching_clean_spreadsheet.xlsx` | C7_Pair_Matching.xlsx | 3db7ac5563 | Clean 53-row matching table (better than the .docx). |
| `_built\Hilin_Mu_Master_C4_C7.xlsx` | Hilin_Mu_Master_C4_C7.xlsx | 0ccc00c4d4 | Compiled paired master C4-C7. |
| `_built\Hilin_Mu_MasterDoc_Compiled.xlsx` | Hilin_Mu_MasterDoc_Compiled.xlsx | 5ad7cff33b | Compiled master doc (185-school panel). |
| `_shared\School_Name_Review_By_Commune_2.xlsx` | School_Name_Review_By_Commune_2.xlsx | a1092e6d8d | School-name canonicalization worksheet. |
| `_shared\School_Name_Review_By_Commune.xlsx` | School_Name_Review_By_Commune_2.xlsx | a1092e6d8d | School-name canonicalization worksheet. |
| `_shared\Antoine_s_Copy_of_LFF_Hilin_Mu_historical_data_for_RCT_evaluation_UCB_1.xlsx` | Antoine_s_Copy_of_LFF_Hilin_Mu_historical_data_for_RCT_evaluation_UCB_1.xlsx | 27dbdb07b7 | Original LFF historical CM2 data + metric definitions (fuller 1141-row copy). |
| `_shared\LFF_historical_data_UCB.xlsx` | Antoine_s_Copy_of_LFF_Hilin_Mu_historical_data_for_RCT_evaluation_UCB_1.xlsx | 27dbdb07b7 | Original LFF historical CM2 data + metric definitions (fuller 1141-row copy). |
| `Cohort7\CM1\sources\CM1 Resultats fin d'année Hilin Mu C7 121425.xlsx` | CM1 Resultats fin d'année Hilin Mu C7 121425.xlsx | 100e3cc4ed | C7 CM1 year-end academic results (glob-resolved). |
| `Cohort7\CM1\sources\C7_CM1_Resultats_FinAnnee.xlsx` | CM1 Resultats fin d'année Hilin Mu C7 121425.xlsx | 100e3cc4ed | C7 CM1 year-end academic results (glob-resolved). |
| `Cohort7\CM1\sources\CM1 Pré-test_Post-test Hilin Mu C7(1).xlsx` | CM1 Pré-test_Post-test Hilin Mu C7(1).xlsx | c9cdd459b3 | C7 CM1 pre/post tests (glob-resolved). Provenance. |
| `Cohort7\CM1\sources\C7_CM1_PrePost_Tests_provenance.xlsx` | CM1 Pré-test_Post-test Hilin Mu C7(1).xlsx | c9cdd459b3 | C7 CM1 pre/post tests (glob-resolved). Provenance. |
| `Cohort7\CM1\sources\Hilin Mu C7 CM1 (TX & CTRL) prepost-tests.xlsx` | Hilin Mu C7 CM1 (TX & CTRL) prepost-tests.xlsx | 01a8746c3d | CANONICAL C7 CM1: 2345 girls (1287 int/1058 ctrl), pre+post+status25 populated. Drop footer rows lacking groupIC2 (SD/count summaries) on merge. |
| `Cohort7\CM1\sources\C7_CM1_TX_CTRL_prepost_status_CANONICAL.xlsx` | Hilin Mu C7 CM1 (TX & CTRL) prepost-tests.xlsx | 01a8746c3d | CANONICAL C7 CM1: 2345 girls (1287 int/1058 ctrl), pre+post+status25 populated. Drop footer rows lacking groupIC2 (SD/count summaries) on merge. |
| `Cohort7\CM2\sources\Hilin Mu C7 CM2 (TX & CTRL) prepost-tests.xlsx` | Hilin Mu C7 CM2 (TX & CTRL) prepost-tests.xlsx | e544eb547d | C7 CM2 merged (1381 rows, incl. mentor-name column). Compare vs folder file on merge. |
| `Cohort7\CM2\sources\C7_CM2_TX_CTRL_prepost_mentor.xlsx` | Hilin Mu C7 CM2 (TX & CTRL) prepost-tests.xlsx | e544eb547d | C7 CM2 merged (1381 rows, incl. mentor-name column). Compare vs folder file on merge. |
| `Cohort6\CM2\sources\C6_CM2_Djirataoua_Control_CollegeTracking.xlsx` | C6_CM2_Djirataoua_Control_CollegeTracking.xlsx | 1ba5e3e690 | Already-renamed canonical file. |
| `Cohort6\CM2\sources\C6_CM2_Djirataoua_Control_EOY_Status_GovScores.xlsx` | C6_CM2_Djirataoua_Control_EOY_Status_GovScores.xlsx | 6ea4231470 | Already-renamed canonical file. |
| `Cohort6\CM2\sources\C6_CM2_Djirataoua_Interv_CollegeTracking.xlsx` | C6_CM2_Djirataoua_Interv_CollegeTracking.xlsx | fcc2f23f10 | Already-renamed canonical file. |
| `Cohort6\CM2\sources\C6_CM2_Djirataoua_Interv_EOY_Status_GovScores.xlsx` | C6_CM2_Djirataoua_Interv_EOY_Status_GovScores.xlsx | 52f4dee1c3 | Already-renamed canonical file. |
| `Cohort6\CM2\sources\C6_CM2_Interv_Pre_Post_TestScores.xlsx` | C6_CM2_Interv_Pre_Post_TestScores.xlsx | bfbdb701dc | Already-renamed canonical file. |
| `Cohort6\CM2\sources\C6_CM2_Sae_Saboua_Control_EOY_Status_GovScores.xlsx` | C6_CM2_Sae_Saboua_Control_EOY_Status_GovScores.xlsx | d6816e1b72 | Already-renamed canonical file. |
| `Cohort6\CM2\sources\C6_CM2_Sae_Saboua_Interv_EOY_Status_GovScores.xlsx` | C6_CM2_Sae_Saboua_Interv_EOY_Status_GovScores.xlsx | 369c138b84 | Already-renamed canonical file. |
| `Cohort6\CM2\sources\C6_CM2_Safo_Control_CollegeTracking.xlsx` | C6_CM2_Safo_Control_CollegeTracking.xlsx | a5a0e610bc | Already-renamed canonical file. |
| `Cohort6\CM2\sources\C6_CM2_Safo_Control_EOY_Status_GovScores.xlsx` | C6_CM2_Safo_Control_EOY_Status_GovScores.xlsx | c44fc8dc25 | Already-renamed canonical file. |
| `Cohort6\CM2\sources\C6_CM2_Safo_Interv_EOY_Status_GovScores.xlsx` | C6_CM2_Safo_Interv_EOY_Status_GovScores.xlsx | 750fe7a28d | Already-renamed canonical file. |
| `Cohort6\CM2\sources\C6_CM2_Tibiri_Control_CollegeTracking.xlsx` | C6_CM2_Tibiri_Control_CollegeTracking.xlsx | f92abb2619 | Already-renamed canonical file. |
| `Cohort6\CM2\sources\C6_CM2_Tibiri_Control_EOY_Status_GovScores.xlsx` | C6_CM2_Tibiri_Control_EOY_Status_GovScores.xlsx | 683a6eab43 | Already-renamed canonical file. |
| `Cohort6\CM2\sources\C6_CM2_Tibiri_Interv_EOY_Status_GovScores.xlsx` | C6_CM2_Tibiri_Interv_EOY_Status_GovScores.xlsx | 93c783786a | Already-renamed canonical file. |
| `Cohort7\CM2\sources\C7_CM2_All_CollegeTracking.xlsx` | C7_CM2_All_CollegeTracking.xlsx | fbf7398a69 | Already-renamed canonical file. |
| `Cohort7\CM2\sources\C7_CM2_All_Pre_Post_TestScores_GovScores_EOY.xlsx` | C7_CM2_All_Pre_Post_TestScores_GovScores_EOY.xlsx | 527cbca19b | Already-renamed canonical file. |
| `Cohort7\CM2\sources\C7_CM2_PairMatching.docx` | C7_CM2_PairMatching.docx | 2d38845520 | Already-renamed canonical file. |
| `Cohort6\CM2\sources\C6_CM2_PairMatching_PROXY.xlsx` | PROXY from C6_CM2_PairMatching.xlsx | (built) | PROXY pending official LFF C6 matching doc. |
