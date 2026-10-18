# GSE165745 RCC-to-processed-matrix reconciliation — 2026-10-18

## Result

**Gate: FAIL — mixed measurement scales detected.** This is an empirical input-integrity finding, not a recovered description of the original nSolver workflow.

The raw archive and processed series matrix were downloaded in CI and matched by the GSM accession in each RCC filename and the corresponding GEO matrix column.

- Samples: 24/24 matched.
- Frozen score genes: 19/19 present in each sample.
- Matched gene measurements: 456/456.
- Sample scale classes: 23 `LINEAR_SCALAR_MULTIPLE`; 1 `LOG2_RAW_COUNT_PLUS_OFFSET`.
- The exceptional sample is **GSM5049357** (RCC member `GSM5049357_R010.RCC.gz`, RCC-internal sample ID `GB12`). For its 19 panel genes, processed values equal `log2(raw RCC count) + offset` with offset approximately `-0.0243935`, to the audit tolerance.
- The other 23 samples have processed panel values equal to raw RCC counts multiplied by a sample-specific scalar, within the audit tolerance.

The scale classification is empirical. It does **not** establish which nSolver or downstream normalization settings were intended, nor justify converting one sample automatically. The original pipeline and the cause of the exceptional sample remain unresolved.

## Source provenance

- GEO series: [GSE165745](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE165745)
- Raw archive: `GSE165745_RAW.tar`
  - SHA-256: `2e7efcee340cb2710aa0b291df6188c00d5e9312ddca912c94d9508f3db5df74`
  - Bytes: 92,160
- Compressed series matrix: `GSE165745_series_matrix.txt.gz`
  - SHA-256: `c6973bc2a9e1a460b7585e605b47451fedd3c53f7b7d922252592b96bc6c164b`
  - Bytes: 34,047
- Decompressed matrix-content SHA-256: `6a201f525da8b9bce96228ba66641c2264efbdc131f01a04dd54aca8555ab648`

The executable audit and its JSON receipt are emitted by the `geo-source-inventory-audit` artifact in the Wnt workflow.

## Consequence for the candidate score

The existing score applies `log1p` to the deposited GEO values. Because one sample is on a different empirical scale, the cohort-wide AUROC of 0.5208 and descriptive balanced accuracy of 0.625 are not interpretable as a scale-consistent test of the frozen score. Preserve those historical numbers as a record of the prior run, but do not use them as evidence for or against the biological hypothesis.

Do not repair the exceptional sample by an undocumented automatic transform, refit the score, or tune the threshold. First establish the authoritative processed-data pipeline and whether the GSM5049357 column was intentionally transformed. Then rerun a prespecified, scale-consistent analysis from a reproducible input source.

## Independent-validation boundary

GSE280470 is not an independent validation cohort without patient-level overlap reconciliation. Its own source audit also reports mixed empirical scale classes (35 log2-plus-offset, 4 unresolved/mixed among 39 samples); this is an input-audit result, not an independent performance estimate.

## Explicit not-proved fields

- Original nSolver / downstream normalization procedure: **not established**.
- Cause of the GSM5049357 scale anomaly: **not established**.
- Correct transformation for GSM5049357: **not established**.
- Validity of the current fixed-score performance estimate under a consistent scale: **not established**.
- Independent validation, calibration, clinical utility, or treatment benefit: **not established**.

## NEXT_ACTIONS :=

1. Recover and document the exact preprocessing pipeline and settings used to produce the deposited matrix.
2. Resolve GSM5049357 against the authoritative processing record; do not infer a correction from model performance.
3. Rerun the fixed score only after the input-scale gate passes, preserving the gene panel and threshold rule without outcome-driven tuning.
4. Keep PR #100 draft and unmerged until the scale discrepancy and independent-validation boundary are resolved.
