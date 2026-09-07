# Melanoma route-burden v1 — GSE78220 development result — 2026-09-06

## Status

`DEVELOPMENT-NEGATIVE / V1 RETIRED`

This record applies only to the frozen route-burden feature defined in
`MELANOMA_ROUTE_BURDEN_PREDICTIVE_FEATURE_2026_09_06.md` and implemented by
`infra/ci/score_melanoma_route_burden.py`.

It does not establish a validated predictive melanoma model, treatment-selection system, clinical efficacy, or cancer cure.

## Exact reproducible evidence

```text
AUDIT_MERGE_COMMIT := 6c192189384055e8a19174105de7d645b759ede6
MAINLINE_AUDIT_RUN := 34070111840
MAINLINE_CANONICAL_RUN := 34070111844
MAINLINE_VERIFY_RUN := 34070111853
MAINLINE_EXTERNAL_STATUS_LOCK_RUN := 34070111871
MAINLINE_AUDIT_ARTIFACT := 10000172438
MAINLINE_AUDIT_ARTIFACT_DIGEST := sha256:996ab98539ec5af6f3c01bb9a12bff0ed2dc4744418169d8cfe769419e8b7942
```

All four exact-mainline jobs completed successfully.

The audit used the original NCBI GEO workbook and required

```text
GSE78220_PatientFPKM.xlsx
SHA256 := ae3b044f23a0a4cd2859da36726a220856c35216a169c17f93dfc3bd20b04de6
GENES := 25268
SAMPLES := 28
```

The original NCBI GEO series matrix was also used.

## Frozen patient-selection rule

Selection was fixed before response-score association:

```text
RULE := earliest pretreatment biopsy ordinal per patient; selection ignores response
KEEP := Pt27A
EXCLUDE := Pt27B  # later pretreatment biopsy for Pt27
EXCLUDE := Pt16   # on-treatment
```

The primary endpoint remained

```text
CR or PR versus PD
```

with

```text
N_INCLUDED := 26
N_RESPONDER := 14
N_NONRESPONDER := 12
```

## Frozen v1 hypothesis

The prespecified direction was

```text
higher S_PD1 -> greater probability of CR/PR rather than PD
```

where

```math
B_{route}(p)=\max_g z_{pg},
\qquad
S_{PD1}(p)=1-B_{route}(p).
```

No weights were learned from outcomes.

## Development result

The exact mainline audit reproduced

```text
AUROC := 0.49404761904761907
AUROC_95_CI := [0.27380952380952384, 0.7261904761904762]
AUPRC := 0.5509429849961887
RESPONDER_PREVALENCE := 0.5384615384615384
BOOTSTRAP := stratified patient bootstrap, 5000 iterations, seed 20260906
```

Therefore

```text
V1_DIRECTIONAL_HYPOTHESIS_SUPPORTED := false
```

The score does not discriminate CR/PR from PD in the development cohort in its prespecified direction.

## Fail-closed consequence

```text
V1_CALIBRATION_ADMISSIBLE := false
V1_GSE91061_UNBLIND_ADMISSIBLE := false
RETROSPECTIVELY_VALIDATED_PREDICTIVE_MODEL := false
VALIDATED_TREATMENT_SELECTION_SYSTEM := false
CANCER_CURE_ESTABLISHED := false
```

`GSE91061` remains locked for v1. A development-negative feature is not promoted merely because an independent cohort exists.

## Structural diagnosis

The v1 construction compares each route gene with the rest of the transcriptome **within the same tumor**, then takes the maximum across seven signed route spokes.

A plausible structural failure mode is therefore saturation: if at least one retained route proxy sits at a high within-sample percentile in most tumors, the maximum is high across both response classes and `S_PD1` has little patient-to-patient discrimination.

This is a diagnosis of the feature construction, not a proved biological mechanism of anti-PD-1 resistance.

The empirical GSE78220 result is sufficient to reject v1 as the candidate predictive score regardless of whether this saturation diagnosis is ultimately correct.

## Boundary

```text
BOUNDARY :=
the frozen Spiderweb route-burden v1 score is development-negative in GSE78220;
it must not be promoted, calibrated, retuned under the v1 name, or evaluated against
the locked GSE91061 outcomes as v1
```

## Next bounded action

```text
NEXT_ACTIONS :=
1. Define one separately versioned v2 feature that replaces within-tumor/max saturation with a development-fitted, patient-discriminative route normalization and a prespecified multi-spoke aggregation.
2. Freeze the complete v2 transformation and all hyperparameters before accessing GSE91061 outcomes.
3. Keep GSE91061 as the one-time independent test and fail closed if its validation gate is not met.
```
