# Melanoma predictive-validation ladder — 2026-09-06

## Status

`CONDITIONAL / VALIDATION-PROTOCOL DEFINITION`

This document defines what would be required before the repository may promote any melanoma response model from a conceptual/executable framework to a retrospectively validated predictive model, then separately to a treatment-selection system, and finally to any cure-level claim.

It does not itself validate a predictor, recommend treatment, or establish cure.

## Three claim levels must remain separate

```text
LEVEL_1 := retrospectively validated predictive melanoma model
LEVEL_2 := validated treatment-selection system
LEVEL_3 := cancer-cure claim
```

The implication arrows are one-way only:

```text
LEVEL_3 requires evidence stronger than LEVEL_2
LEVEL_2 requires evidence stronger than LEVEL_1
LEVEL_1 does not imply LEVEL_2
LEVEL_2 does not imply LEVEL_3
```

A model that predicts response to one therapy is not automatically a treatment-selection system because it does not estimate comparative benefit among alternative therapies for the same patient.

## Public anti-PD-1 development surface

### GSE78220 / Hugo et al. 2016

Public source:

```text
GEO := GSE78220
PMID := 26997480
DOI := 10.1016/j.cell.2016.02.065
```

The public cohort contains pretreatment metastatic-melanoma biopsies profiled by RNA-seq before anti-PD-1 therapy. The GEO record contains 28 RNA-seq samples. The original paper notes that the RNA-seq set includes a second-site pretreatment biopsy from patient 27, so patient-level deduplication is mandatory before model evaluation.

This cohort may be used for development only.

```text
DEVELOPMENT_COHORT := GSE78220
```

No feature, coefficient, threshold, state weighting, or normalization choice may be selected using the locked validation cohort below.

## Locked independent validation surface

### GSE91061 / Riaz et al. 2017

Public source:

```text
GEO := GSE91061
PMID := 29033130
DOI := 10.1016/j.cell.2017.09.028
```

The GEO record contains 109 RNA-seq samples from 65 patients, with 51 pretreatment and 58 on-treatment samples. The pretreatment surface is the admissible independent validation surface for a pretreatment response predictor.

```text
LOCKED_VALIDATION_COHORT := GSE91061_PRETREATMENT
```

On-treatment samples may not be substituted into a pretreatment validation analysis.

## Common response endpoint

Published melanoma datasets differ in how stable disease is grouped. To avoid changing the endpoint after seeing model performance, the primary binary endpoint is frozen as:

```text
RESPONDER     := CR or PR
NONRESPONDER  := PD
EXCLUDED      := SD, mixed response, unevaluable, unknown
```

The mapping must be performed from source clinical annotations before model scores are inspected.

Any alternative endpoint that includes stable disease must be reported as a separately named sensitivity analysis and may not replace the primary endpoint after results are known.

## Patient-level unit of analysis

```text
UNIT := patient
```

Rules:

```text
1. repeated biopsies from the same patient may not appear as independent test cases;
2. feature selection must be performed on development patients only;
3. normalization using cohort-wide outcome information is forbidden;
4. model coefficients and decision thresholds must be frozen before validation labels are scored;
5. missing-feature handling must be declared before validation.
```

## Predictive-model validation gate

Let a frozen score be

```math
s(x) \in \mathbb R
```

for pretreatment patient features `x`, and let

```text
y = 1 := CR/PR
y = 0 := PD
```

on the locked validation cohort.

Define:

```text
PREDICTIVE_VALIDATION_ADMISSIBLE :=
  frozen_model
  AND patient_level_deduplication
  AND endpoint_frozen_before_scoring
  AND independent_validation_cohort
  AND no_validation_feature_selection
  AND complete_metric_report
  AND uncertainty_report
```

The minimum metric report is:

```text
AUROC
balanced_accuracy
sensitivity
specificity
Brier_score
sample_count_by_class
95% confidence interval for AUROC
```

The no-information comparators must also be reported:

```text
AUROC_null := 0.5
prevalence_only_Brier := p * (1-p)
```

where `p` is the responder prevalence in the locked validation set.

A single favorable point estimate is insufficient. Promotion to

```text
RETROSPECTIVELY_VALIDATED_PREDICTIVE_MODEL := true
```

requires all of:

```text
1. the complete frozen analysis is reproducible from repository code plus public source data;
2. validation AUROC > 0.5;
3. the prespecified AUROC uncertainty interval excludes 0.5 on its lower side;
4. Brier score improves on the prevalence-only predictor;
5. no patient or biopsy leakage exists between development and validation;
6. the result reproduces on at least one second independent melanoma cohort without refitting the original model.
```

Until those conditions hold:

```text
RETROSPECTIVELY_VALIDATED_PREDICTIVE_MODEL := false
```

## Treatment-selection gate

A validated predictor of response to anti-PD-1 alone cannot establish treatment selection.

Let

```math
Y(t)
```

denote the potential outcome under treatment `t`.

Treatment selection requires evidence about a contrast such as

```math
\Delta(x;t_1,t_2)
= E[Y(t_1)-Y(t_2)\mid X=x],
```

not merely

```math
P(Y=1\mid X=x,t_1).
```

Therefore:

```text
TREATMENT_SELECTION_ADMISSIBLE :=
  at_least_two_relevant_treatment_options
  AND patient-level comparable outcome definition
  AND externally validated comparative-benefit model
  AND explicit uncertainty/abstention rule
  AND prospective or otherwise clinically credible validation of model-guided choice
```

Until those conditions hold:

```text
VALIDATED_TREATMENT_SELECTION_SYSTEM := false
```

The spiderweb / ER quantities may become candidate explanatory features, but they may not be interpreted as treatment recommendations until this gate is discharged.

## Cure-level gate

Neither retrospective prediction nor treatment selection establishes cure.

A cure-level claim would require clinical evidence outside the present repository proving durable absence of clinically meaningful malignant disease under a defined intervention and follow-up regime, with recurrence and competing failure modes adequately addressed.

Thus:

```text
CANCER_CURE_ESTABLISHED := false
```

No repository consistency check, mathematical graph closure, retrospective AUROC, animal complete response, or absence of detectable tumor on a bounded assay can by itself set this flag to true.

## Relation to the spiderweb / ER framework

The existing ER-exit construction defines conditional quantities such as:

```math
q_i,
R_{ER}(i),
ER(i),
\|W_i(t)\|.
```

For predictive validation, any patient-level ER-derived feature must first receive an externally grounded mapping from measured patient data to graph state/edge quantities. Such a mapping must be frozen on the development cohort before independent validation.

Therefore the current logically prior missing object is:

```text
MISSING_OBJECT :=
a reproducible patient-to-spiderweb feature map that can be computed from public
pretreatment melanoma data without using validation outcomes
```

## Current boundary

```text
BOUNDARY :=
the repository now has a prespecified path toward retrospective melanoma-response
validation, treatment selection, and cure-level evidence, but none of those three
claim levels is currently established; the first executable missing object is a
frozen patient-level feature map followed by independent validation
```

## Next bounded action

```text
NEXT_ACTIONS :=
1. Define one patient-level spiderweb feature map using only repository-retained melanoma biology and pretreatment measurements available in GSE78220/GSE91061.
2. Freeze that feature definition without inspecting GSE91061 outcomes.
3. Implement patient deduplication and the CR/PR-vs-PD endpoint parser.
4. Train only on GSE78220 and score the locked GSE91061 pretreatment cohort once.
5. Fail closed if the independent validation gate is not met.
```
