# Poźniak Table S1 — patient-level clinical crosswalk (2026-11-15)

**SOURCE:** User-provided `mmc1.xlsx`, worksheet `Sup_table_1`, range `A1:P47`.  
**SHA256:** `ce8597674c02dc2e349e597b36fef69c7ae46a846556b9d69cee0654fd8b44bf`  
**STATUS:** UPLOADED_TABLE_INSPECTED / CLINICAL_CROSSWALK_RECONSTRUCTED / SOURCE_FILE_AUTHENTICITY_NOT_INDEPENDENTLY_ATTESTED / CELL_LEVEL_VALIDATION_OPEN

## Exact workbook accounting

The uploaded sheet has 46 data rows, 23 unique patient IDs, 23 BT sample rows representing 22 patients, and 23 OT rows. Patient 16 contributes two BT biopsies, requiring a prespecified single-patient selection rule. Patient 39 has OT only.

At baseline there are 17 anti-PD-1 monotherapy **sample rows** representing 16 patients, with the following `Criterion` labels:

| Criterion | BT sample rows | Distinct patients |
|---|---:|---:|
| BOR PD | 10 | 9 |
| BOR PR | 4 | 4 |
| BOR CR | 1 | 1 |
| BOR SD | 1 | 1 |
| no pCR | 1 | 1 |
| **Total** | **17** | **16** |

The frozen BFF **clinical** CR/PR-versus-PD inclusion set therefore has **15 BT rows / 14 unique patients: five CR/PR responders and nine PD nonresponders**. These are not yet independently verified melanoma-cell-and-macrophage paired CD36 observations.

| Category | Patient IDs (public pseudonyms from uploaded sheet) |
|---|---|
| BOR CR/PR | 15, 20, 21, 29, 30 |
| BOR PD | 16, 17, 18, 19, 23, 25, 26, 33, 36 |
| Excluded BOR SD | 22 |
| Excluded pathological criterion (`no pCR`) | 14 |

All six BT combination-therapy patient records are excluded, regardless of their BOR/pCR labels. Other OT biopsies are excluded. The `Responder?` 0/1 field is **not** itself a sufficient endpoint; the `Criterion` field is used to distinguish BOR PD/SD and pCR.

The authors' `GC_ALL_MALIGNANT.R` script also excludes `scrCMA109` (patient 30, BOR PR, BT pembrolizumab) in its explicit sample exclusion list. This provides an additional **known exclusion from that malignant-cell script**, leaving **at most 13** clinically eligible patients in its malignant analysis subset, if no other exclusions apply. Do not assume that a different released object has identical contents without checking. Patient 30's sample is not proven to have usable malignant expression merely because Table S1 records a BT biopsy.

## Next biological data gate

The count of eligible *paired-cell* patients remains UNKNOWN. Required per-patient facts:

- that the original sample (not another timepoint) contributes malignant and macrophage cells to the same processed object,
- sufficiently supported cell annotation and observed CD36 expression with a declared assay scale,
- one deterministic biopsy-selection rule for patient 16 (for instance lexicographically first BT Sample ID, frozen before outcomes are inspected),
- an independent source/provenance check against the journal supplement or authors' original workbook,
- leakage-safe and separately-versioned exploratory design with independent outcome validation.

**No expression matrix has been downloaded, no CD36 values computed, no predictive model fitted, no existing v2 model re-scored, and no clinical prediction made.**

```text
UPLOADED_TABLE_SHEET_AUDITED := TRUE
FILE_SHA256 := ce8597674c02dc2e349e597b36fef69c7ae46a846556b9d69cee0654fd8b44bf
SAMPLES_TOTAL := 46
PATIENTS_TOTAL := 23
BASELINE_MONOTHERAPY_SAMPLES := 17
BASELINE_MONOTHERAPY_PATIENTS := 16
FROZEN_ENDPOINT_ELIGIBLE_SAMPLES := 15
FROZEN_ENDPOINT_ELIGIBLE_PATIENTS := 14
BOR_CR_PR_PATIENTS := 5
BOR_PD_PATIENTS := 9
MALIGNANT_SCRIPT_EXCLUDED_SAMPLE := scrCMA109
MALIGNANT_SCRIPT_POTENTIALLY_ELIGIBLE_UPPER_BOUND := 13
PATIENT_MATCHED_CELL_CD36_COUNT := UNKNOWN
INDEPENDENT_SUPPLEMENT_AUTHENTICATION := NOT_RUN
CELL_EXPRESSION_DATA := NOT_RETRIEVED
PATIENT_LEVEL_PREDICTION := NOT_RUN
FROZEN_V2 := UNCHANGED
```
