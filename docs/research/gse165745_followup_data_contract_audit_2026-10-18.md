# GSE165745 follow-up audit: processed values, controls, and remaining hard blockers
Date: 2026-10-18

## New source-grounded findings

### 1. The deposited sample table is not raw integer counts
GEO sample records label the expression column `VALUE Gene conts`, but the visible values include non-integers and wide sample-to-sample scales. For example, GEO's sample record GSM5049359 reports WNT8B 22.79910168, LRP6 3235.029678, STAT3 12598.94644; GSM5049358 reports WNT8B 11.22102058, LRP6 2416.910258, STAT3 15025.43442; GSM5049371 reports WNT8B 3.596513148, LRP6 5526.180779, STAT3 7203.815836. This is evidence that the displayed table is not simply an untouched integer-count matrix. It does not identify the exact processing steps, and it does not prove that log1p is the right transformation.

Sources:
- https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM5049359
- https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM5049358
- https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM5049371

### 2. GEO confirms collection and software, not the analysis contract
The GEO sample processing text says the data were collected on a NanoString nCounter Max system with the nCounter Vantage 3D Human Wnt Pathways Panel (N2_WNT_Pth_v1.0), plus custom cytolytic T-cell markers and IDO1, and analyzed with nSolver. It does not state which background correction, positive-control normalization, housekeeping/content normalization, thresholds, or export transformation were used.

Platform record: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GPL29668

### 3. Why the missing nSolver settings matter
The nSolver 4.0 user manual documents configurable positive-control normalization and CodeSet-content normalization; the recommended mRNA standard uses the geometric mean of selected housekeeping genes, and settings can be changed. Thus “analyzed with nSolver” is insufficient to reconstruct the processed values. This is a general software-method fact, not evidence of which settings DeVito et al. actually used.

Sources:
- https://nanostring.com/wp-content/uploads/MAN-C0019-08_nSolver_4.0_Analysis_Software_User_Manual.pdf
- https://pmc.ncbi.nlm.nih.gov/articles/PMC8138885/ (review of NanoString normalization/QC options)

### 4. The paper supports a pathway association, not the implemented score
The original article says the NanoString comparison includes 12 responders and 12 nonresponders and uses Benjamini–Yekutieli FDR correction across the whole gene panel. It describes increased Wnt ligand/FZD receptor activity and higher LRP5, PYGO1, DVL1, DKK2 and SFRP2 in nonresponders. RNF43 evidence is discussed in the separate GSE78220 RNA-seq reanalysis (Figure 1C/Table S1), not as validation of the exact fixed arithmetic score implemented here. Table S2 is the relevant supplement for the NanoString cohort.

Source: https://pmc.ncbi.nlm.nih.gov/articles/PMC8148423/

### 5. The updated GSE280470 dataset is useful for annotation, but overlap must be resolved
GSE280470 contains 39 samples and explicitly says it includes previously published GSE165745 samples with updated clinical data. Its sample labels include a “group” characteristic, and its deposited processed values have a different-looking scale (GEO labels them “processed signal”; sample examples include values around 4–14). This is a strong warning not to pool GSE165745 and GSE280470 expression values or treat all 39 as independent. A patient/sample crosswalk and explicit overlap list are required before any reanalysis.

Sources:
- https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE280470
- https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8598415

## Model implementation defects / interpretation controls
- V1 applies `log1p` to the GSE165745 `VALUE` field without a verified rationale. Keep this frozen only as a historical exploratory candidate; do not interpret its score as biologically calibrated.
- V1 computes a midpoint-of-minimum-and-maximum score threshold on the same 24 samples and reports balanced accuracy at that threshold. This is an in-sample, data-derived threshold and is not a valid performance estimate for a locked classifier. It must never be described as a usable cutoff.
- AUROC is threshold-independent, but it remains an exploratory estimate on n=24 with deposited labels and no independent validation. The observed AUROC for nonresponse is 0.5208333333, near chance.
- The sample-title parser is using labels encoded in GEO titles, not a clinical adjudication file. This reproduces the repository's chosen label mapping; it does not independently verify response definitions.

## What is still not obtained
Despite searching the accessible primary-source index and article text, the actual supplementary PDF tables have not been extracted in this execution. The original Table S2 gene-level table, sample-level clinical characteristics, and exact response criteria remain unverified here. The RCC archives and series-matrix files also have not been downloaded and hashed in this execution; network access from the execution container failed and the GEO browser endpoints were intermittently blocked by access challenges. Do not claim those downloads or table extraction have happened.

## Required next steps, in evidence order
1. Obtain NIHMS1700572 supplement 1 and supplement 2; extract Table S1 and Table S2 into a machine-readable table and cite the exact source pages.
2. Obtain `GSE165745_RAW.tar`, the series matrix, and `GSE280470_RAW.tar`; hash each source file and record per-sample RCC identifiers.
3. Parse RCC controls and endogenous target counts, run QC, and compare candidate processing pipelines to GEO `VALUE`. Only select a pipeline if its output reproduces deposited values within a stated tolerance or the original processing is otherwise documented.
4. Extract GSE280470 clinical metadata and build a strict sample/patient overlap crosswalk. Use updated clinical annotations only after identifying the corresponding GSE165745 samples; exclude shared cases from any independent-test claim.
5. Freeze an explicit clinical endpoint and target mapping before any score evaluation. If these cannot be reconstructed from public data, state that as a data limitation and request source metadata from the study authors rather than infer criteria.
6. After resolving the data contract, rerun the exact frozen v1 unchanged as a reproduction check. Any scientifically justified alternative preprocessing or score becomes a separately versioned candidate, not a replacement of the current result.
7. Do not use the observed cohort to optimize a cutoff. Independent evaluation requires a distinct compatible cohort; report confidence intervals and baseline comparisons.

## Decision
`STATUS := SOURCE_SEARCH_EXTENDED; RAW_DATA_AND_SUPPLEMENT_EXTRACTION_BLOCKED`
`GEO_VALUE_IS_RAW_INTEGER_COUNT := FALSE_FOR_DISPLAYED_EXAMPLES`
`EXACT_NORMALIZATION := UNRESOLVED`
`LOG1P_VALIDITY := UNRESOLVED`
`TABLE_S1_S2_EXTRACTION := NOT_COMPLETED`
`CLINICAL_ENDPOINT := LABELS_DEPOSITED; OPERATIONAL_CRITERIA_UNVERIFIED`
`GSE280470_OVERLAP := KNOWN_TO_EXIST; CASE_LEVEL_CROSSWALK_PENDING`
`V1_AUROC := 0.5208333333`
`CLINICAL_USE := NOT_SUPPORTED`
