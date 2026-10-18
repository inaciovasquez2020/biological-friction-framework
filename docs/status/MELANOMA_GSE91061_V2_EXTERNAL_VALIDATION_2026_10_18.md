# GSE91061 frozen melanoma v2 validation — 2026-10-18

## Result

**External validation gate failed. Do not promote melanoma v2 as a retrospectively validated predictive model.**

The locked GSE91061 pretreatment analysis completed using the frozen seven-marker ECDF score, frozen GSE78220 reference, frozen logistic calibration coefficients, and the fixed 0.5 probability threshold. No GSE91061 expression distribution or response label was used to refit a parameter.

Workflow run: https://github.com/inaciovasquez2020/biological-friction-framework/actions/runs/39086550454

The workflow's execution status is successful because the analysis ran and emitted a receipt. The model's statistical promotion gate is **not** successful.

## Frozen endpoint and cohort accounting

- GEO source: [GSE91061](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE91061)
- Pretreatment samples selected: 51
- Patient-level duplicate pretreatment exclusions: 0
- Primary endpoint included: 33 patients
  - CR/PR responders: 10
  - PD nonresponders: 23
- Excluded from the primary endpoint: 18
  - Stable disease: 16
  - Unknown response: 2
- On-treatment samples were not scored.
- The GEO response label `PRCR` was mapped to the frozen CR/PR responder class; published GSE91061 analyses use PRCR to denote partial/complete response (for example, https://www.nature.com/articles/s41419-023-05692-5).

## Metrics

| Metric | Locked GSE91061 result |
|---|---:|
| AUROC | 0.4913043478 |
| AUROC 95% stratified patient-bootstrap CI | [0.2739130435, 0.7173913043] |
| Balanced accuracy at frozen threshold 0.5 | 0.5043478261 |
| Sensitivity | 0.4000000000 |
| Specificity | 0.6086956522 |
| Brier score | 0.2548827830 |
| Prevalence-only Brier baseline | 0.2112029385 |

The AUROC point estimate is below 0.5, its confidence interval includes 0.5, and the Brier score is worse than the prevalence-only baseline. All three are adverse to the prespecified promotion gate.

## Frozen parameters and provenance

- Feature version: `MELANOMA_ROUTE_BURDEN_V2_DEFINITION_2026_09_06`
- Calibration version: `MELANOMA_V2_LOGISTIC_CALIBRATION_2026_09_06`
- Intercept: `-2.7753294906668593`
- Slope: `5.91276103727729`
- Probability threshold: `0.5`
- FPKM compressed SHA-256: `987c7637e72ff5ad9c9630b0ee959064713cd8f57348d05003fb85a2f4cc43d5`
- FPKM uncompressed SHA-256: `3930f91cf3b59d79f7905f1744ac269797a37a3703262875342b121bdf57fae1`
- Series matrix compressed SHA-256: `f3ebd04d019afab9f12af0b92cfcafa516bb2b170f5b45d22d5e330e2eebdca0`
- Series matrix uncompressed SHA-256: `73d577a05c0e8b8d4fa46841ad758a1bf2b0c60ad7bdfee2bcc2a80df6c461be`
- Entrez-to-symbol mapping was fixed to the seven model genes; no marker selection or re-signing occurred.
- Existing repository tests: 13 passed.

The full patient-level JSON receipt, including every included patient and every excluded endpoint row, is retained as the `gse91061-v2-validation` artifact on the linked workflow run.

## Decision and boundary

```text
GSE91061_LOCKED_ANALYSIS_EXECUTED := true
GSE91061_PRIMARY_METRICS_REPORTED := true
AUROC_GATE_PASSED := false
AUROC_CI_GATE_PASSED := false
BRIER_BASELINE_GATE_PASSED := false
RETROSPECTIVELY_VALIDATED_PREDICTIVE_MODEL := false
VALIDATED_TREATMENT_SELECTION_SYSTEM := false
CANCER_CURE_ESTABLISHED := false
```

Do not tune the current v2 definition against GSE91061 and then reuse this same cohort as validation. Any revised model must be separately versioned and evaluated on a new locked independent cohort. This result is retrospective research evidence only; it is not treatment advice or evidence of clinical utility.
