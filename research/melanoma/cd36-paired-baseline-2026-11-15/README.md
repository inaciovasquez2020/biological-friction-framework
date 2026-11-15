# Matched baseline melanoma CD36 exploratory certificate

Date: 2026-11-15

## Scope

Read-only analysis of two previously obtained melanoma
single-cell RNA-seq datasets. Twelve patients were matched
between malignant and tumor-microenvironment compartments
using baseline specimen identifiers.

The original data, per-patient summaries, extraction scripts,
and full terminal receipts are retained in a separate
private research checkpoint.

## Method

- RNA raw counts, normalized by each cell's RNA library size.
- Transformation: log1p(10000 * CD36 / library size).
- Primary provisional myeloid populations: clusters 10 and 13.
- One selected baseline specimen per patient.
- A second baseline specimen from one patient was excluded.
- Patient, not cell, is the independent statistical unit.
- Two-sided exact response-label permutation tests
  enumerate all 495 allocations of four responders
  among twelve patients.
- Sensitivity analyses exclude one CD36 outlier and
  change the candidate myeloid cluster definitions.

## Results

- Malignant CD36 versus response: exact p = 214/495.
- Myeloid CD36 versus response: exact p = 346/495.
- Cross-compartment Spearman rho = 0.2867132867.
- Spearman rho after outlier exclusion = 0.4545454545.

These exploratory tests did not establish a statistically
significant CD36-response association.

## Limitations

The cohort is small. Candidate myeloid clusters are not
independently confirmed macrophage annotations.
Observational expression is not evidence of causation.
Non-significance is not proof of no effect.
Clinical prediction, external replication, and a novel
resistance mechanism are not established.

## Provenance and release boundary

aggregate_results.json records the source dataset hashes,
source sizes, software information, and aggregate statistics.

Source data and specimen-level records are not distributed
with this public-facing certificate.

The full private checkpoint was subjected to a local
structural and statistical receipt audit. Source SHA-256
digests were subsequently recomputed and matched.

The public certificate is a bounded computational record,
not a clinical model or a treatment recommendation.

Dataset reuse and redistribution conditions still require
review before publication.
