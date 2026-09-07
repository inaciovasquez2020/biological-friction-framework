# Melanoma route-burden v2 calibration freeze — 2026-09-06

## Status

`CONDITIONAL / DEVELOPMENT-ONLY CALIBRATION PROTOCOL`

This document freezes the probability-calibration map and binary decision rule for the already-frozen melanoma route-burden v2 score before any GSE91061 outcome scoring.

It does not establish predictive validity, treatment selection, clinical efficacy, or cure.

## Preconditions

The frozen GSE78220 v2 continuation screen passed on 26 development patients:

```text
AUROC := 0.7023809523809523
AUPRC := 0.657140619405657
RESPONDER_PREVALENCE := 0.5384615384615384
EXPECTED_DIRECTION := observed
```

The locked independent validation cohort remains:

```text
LOCKED_VALIDATION_COHORT := GSE91061_PRETREATMENT
VALIDATION_OUTCOMES_TOUCHED := false
```

## Frozen score input

Let

```math
s_p := S_{PD1}^{(2)}(p) \in [0,1]
```

be the already-frozen v2 score produced from the seven marker-specific development ECDF spokes.

No marker, sign, ECDF reference sample, aggregation rule, or v2 score parameter may change during calibration.

## Probability map

The calibration family is fixed to a two-parameter logistic map:

```math
\hat p_p
:=
\sigma(a+b s_p)
=
\frac{1}{1+e^{-(a+b s_p)}}.
```

The parameters `(a,b)` are fit once using only the frozen GSE78220 development endpoint:

```text
y = 1 := CR/PR
y = 0 := PD
```

by minimizing binary negative log-likelihood:

```math
L(a,b)
=
-\sum_p
\left[
 y_p\log \hat p_p
 +(1-y_p)\log(1-\hat p_p)
\right].
```

No validation patient, validation score distribution, validation response prevalence, or GSE91061 outcome may enter the fit.

### Fail-closed fitting rule

The implementation must use one deterministic optimization procedure with fixed numerical tolerances declared in code before fitting.

If the unpenalized two-parameter logistic maximum-likelihood fit is non-finite, fails to converge, or exhibits numerical separation such that finite `(a,b)` cannot be certified:

```text
CALIBRATION_FIT := failed
VALIDATION_UNBLIND := forbidden
```

No alternative calibration family, regularizer, penalty strength, binning scheme, or isotonic fit may be selected after seeing the failed fit without defining a new separately versioned model/calibration protocol.

## Frozen classification rule

The binary prediction rule is fixed as:

```math
\hat y_p = \mathbf 1\{\hat p_p \ge 0.5\}.
```

Thus:

```text
DECISION_THRESHOLD := calibrated_probability >= 0.5
```

The threshold is not optimized for balanced accuracy, sensitivity, specificity, Youden index, prevalence, or any other validation-cohort statistic.

## Frozen validation outputs

Once `(a,b)` have been fitted and serialized from GSE78220, the unchanged v2 feature map, ECDF reference, calibration coefficients, and `0.5` decision threshold may be applied exactly once to the locked GSE91061 pretreatment validation surface.

The primary report required by the existing validation gate remains:

```text
AUROC
balanced_accuracy
sensitivity
specificity
Brier_score
sample_count_by_class
95% confidence interval for AUROC
```

with null comparators:

```text
AUROC_null := 0.5
prevalence_only_Brier := p_validation * (1-p_validation)
```

The validation prevalence is used only to compute the declared null comparator after endpoint membership is frozen; it does not modify the calibrated model.

## Promotion rule remains unchanged

A favorable GSE91061 result alone is insufficient to set:

```text
RETROSPECTIVELY_VALIDATED_PREDICTIVE_MODEL := true
```

because the existing gate also requires reproduction on at least one second independent melanoma cohort without refitting the original model.

Therefore even after one successful locked validation:

```text
LEVEL_1_PROMOTION := pending_second_independent_replication
```

unless every other gate condition and the second independent replication are also satisfied.

## Claim-state flags

```text
RETROSPECTIVELY_VALIDATED_PREDICTIVE_MODEL := false
VALIDATED_TREATMENT_SELECTION_SYSTEM := false
CANCER_CURE_ESTABLISHED := false
```

## Boundary

```text
BOUNDARY :=
the v2 development score passed its prespecified continuation screen and now has a
frozen development-only probability-calibration family and fixed 0.5 decision rule,
but calibration coefficients have not yet been fitted and GSE91061 outcomes remain
locked; no retrospective validation, treatment selection, efficacy, or cure is established
```

## Next bounded action

```text
NEXT_ACTIONS :=
1. Implement the deterministic two-parameter logistic calibration fit and serialize `(a,b)` from the frozen GSE78220 v2 scores/outcomes only.
2. Verify finite convergence and freeze the resulting calibration object and its source-data/checksum provenance.
3. Freeze the exact GSE91061 pretreatment patient-selection and endpoint extraction surface without computing model metrics.
4. Only then run the one-time locked GSE91061 validation and report every required metric and null comparator.
5. Fail closed if any validation or leakage gate fails.
```
