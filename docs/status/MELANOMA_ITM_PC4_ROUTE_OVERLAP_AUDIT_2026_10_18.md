# ITM PC4 melanocytic signature vs frozen route markers — source and overlap audit

Date: 2026-10-18

## Purpose

Build an outcome-blind, reproducible bridge between the published ITM PC4 melanocytic signature and the frozen seven-marker route-burden v2 feature definition. This is a source/identity/overlap audit only. It is not a new response score, prognostic model, or clinical claim.

## Source facts and cohort accounting

The published study reports 170 high-quality spatial regions of interest (ROIs) from 105 distinct patients. The article separately describes 116 ROIs from 84 patients as in-transit lesions, alongside additional ROIs from other metastatic sites. Therefore, the 84-patient / 116-ROI count is a subset description, not by itself evidence of a contradictory dataset version. Analysis must state which population is being used and join every ROI to a patient identifier.

The PC4 positive melanocytic signature contains 36 genes; the PC4 negative signature contains 56 genes. The paper identifies PMEL, TYRP1, TRPM1, GPR143, and TSPAN10 among the highest-contribution positive genes. The signature is a PCA-derived transcriptional state and is not the same object as the frozen seven-marker route score.

Published sources:
- Article: https://pmc.ncbi.nlm.nih.gov/articles/PMC13398476/
- Dryad data record: https://datadryad.org/dataset/doi:10.5061/dryad.kh18932pf
- Related data/software record: https://zenodo.org/records/19104096
- GEO series: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE325123
- Released analysis code: https://github.com/ziyinhuang96/stgemox_itm_mel_tma/releases/tag/submission-v2

The available matrix is described as log2CPM. The frozen route-burden v2 ECDF reference was built from the GSE78220 FPKM matrix. These units are not presumed interchangeable. The script added with this note deliberately does not read or transform expression values, score the seven-marker model, or fit survival models.

## Reproducible input contract

Once source files are retrieved, provide three local files:

1. A gene-by-ROI expression matrix in CSV or TSV format. First column contains unique gene symbols; remaining column headers are ROI/sample IDs. Expression values are ignored by this audit.
2. A complete PC4 signature table with columns `gene_symbol,pc4_direction`; each direction is `positive` or `negative`. Include all 36 positive and all 56 negative signature genes from the source supplement/code.
3. A sample manifest with columns `sample_id,patient_id`, one row per ROI and the source-defined patient identifier.

Run:

```bash
python3 infra/ci/audit_itm_pc4_route_overlap.py \
  --matrix ITM_log2CPM.csv \
  --signature pc4_signature.csv \
  --manifest itm_roi_manifest.csv \
  --output itm_pc4_route_overlap_receipt.json
```

The receipt records matrix/manifest identity, ROI and unique-patient counts, repeated ROIs per patient, missing signature genes, exact route-marker overlap, and direction-consistent versus direction-conflicting overlap. The default size gate requires 36 PC4-positive and 56 PC4-negative genes. If the source's official complete signature has different documented dimensions, change the expected counts only after recording the source evidence.

## Interpretation rules

- Exact overlap is descriptive, not evidence of biological equivalence.
- Direction-consistent overlap is defined mechanically against the frozen route directions: high-direction markers align with PC4-positive genes; the low-direction SOX10 marker aligns with PC4-negative genes. This convention is a comparison rule, not a claim that the two signatures are equivalent.
- A sample-identity mismatch or incomplete signature blocks interpretation; do not silently drop unmatched rows.
- Any survival analysis must be patient-level and account for multiple ROIs per patient. Do not treat 170 ROIs as 170 independent patients.
- Do not apply the frozen FPKM ECDF score to log2CPM values. A future same-pipeline reconstruction would require a separate, outcome-blind compatibility gate.
- The published survival association for PC4 is prognostic evidence for that signature. It does not validate the frozen seven-marker score as an anti-PD-1 response predictor.

## Current result and boundary

The input matrix and complete PC4 signature were not successfully retrieved in this work session. Therefore, no numerical overlap, correlation, patient-level survival estimate, or new prediction metric is reported. The script and regression tests are ready for execution when the source files are available.

```text
SOURCE_COHORT_ACCOUNTING_RECONCILED := 170_ROI_105_PATIENT_TOTAL_WITH_84_PATIENT_116_ROI_IN_TRANSIT_SUBSET
PC4_SIGNATURE_EQUIVALENCE_TO_FROZEN_ROUTE_SCORE := NOT_ESTABLISHED
FROZEN_V2_SCORING_ON_LOG2CPM := PROHIBITED_BY_CURRENT_COMPATIBILITY_EVIDENCE
NEW_RESPONSE_PREDICTION_VALIDATION := NOT_ESTABLISHED
```

`BOUNDARY := ¬ established_equivalence(PC4_melanocytic_signature, frozen_7_marker_route_score)`

`BOUNDARY := ¬ established_response_prediction(frozen_7_marker_route_score)`
