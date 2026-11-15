# CD36 methodological reconciliation — 2026-11-15

## Status

COMPUTATION_PASS: exact 12-patient response-label permutation audit,
reproduced on the researcher's Mac using the original RDS objects.

This addendum supplements, but does not replace, `aggregate_results.json`.

## Original certificate reproduction

| Measurement | Exact two-sided p-value | Reproduction |
|---|---:|---|
| Malignant CD36 | 214/495 | PASS |
| Myeloid CD36, clusters 10 and 13 | 346/495 | PASS |

Original statistic: difference of patient-level means between
PD and CR/PR of per-cell `log1p(10000 * CD36_counts / library_size)`.
Four responders and eight PD patients; all 495 allocations enumerated.

## Malignant-cell contamination correction

Exact cell-ID overlap identified 17 known malignant cells among
941 original candidate myeloid cells. Excluding the complete known
malignant-cell identifier set retains 924 primary candidate cells.
Adding cluster 16 and applying the same exclusion retains
1,137 extended candidate cells.

| Corrected test | Exact two-sided p-value |
|---|---:|
| Primary myeloid CD36, mean log1p-normalized signal | 288/495 = 0.581818 |
| Extended myeloid CD36, mean log1p-normalized signal | 372/495 = 0.751515 |

All 12 baseline specimens remain represented.

## Separate AUROC analysis

Using patient means of *unlogged* depth-adjusted CD36 counts:

| Measurement | AUROC (higher signal predicts response) | Exact two-sided p-value |
|---|---:|---:|
| Corrected primary myeloid | 0.40625 | 338/495 |
| Corrected extended myeloid | 0.53125 | 462/495 |
| Malignant | 0.18750 | 54/495 |

These are distinct statistics and transformations. The AUROC
permutation results must not be substituted for the original
mean-difference permutation tests.

## Interpretation and restrictions

- No statistically significant CD36-response association was
  established in this 12-patient exploratory cohort.
- Clusters 10 and 13 have strong myeloid-associated marker signatures;
  definitive macrophage identity remains OPEN.
- Cell-library-size adjustment does not eliminate biological,
  sequencing-depth or cell-composition confounding.
- Post hoc sensitivity analyses are descriptive, not validation.
- The original Table S1 source-authenticity assessment remains limited.
- No novel resistance mechanism or clinical predictive utility established.
- Independent cohort validation: NOT_RUN.
- Frozen melanoma v2 predictor and its negative external validation:
  UNCHANGED.
- Patient-level CSV and raw single-cell datasets remain outside
  this public-facing repository checkpoint.

## Provenance

The preserved private checkpoint includes the patient CSV,
the R extraction log, and the exploratory statistical certificate.
Previously reported source SHA-256 hashes are recorded in
`aggregate_results.json`. The original two statistics were reproduced
from the RDS objects in a separate 2026-11-15 Mac run.

This document describes computation receipts supplied by the
researcher, not an independent external clinical review.
