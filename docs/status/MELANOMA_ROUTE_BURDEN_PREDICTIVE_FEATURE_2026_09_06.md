# Melanoma malignant-route burden predictive feature — 2026-09-06

## Status

`CONDITIONAL / FROZEN OUTCOME-BLIND FEATURE DEFINITION`

This document defines one patient-level feature map for the predictive-validation ladder. It does not establish predictive validity, treatment selection, clinical efficacy, or cure.

The feature is intentionally **not** an ER-exit committor or ER resistance score. The ER exit set `H` remains biologically unvalidated, so quantities requiring `H` cannot receive patient-level interpretation yet.

## Purpose

The executable melanoma graph already retains multiple independent malignant-survival, persistence, residual-state, and immune-escape routes. The first predictive bridge asks a narrower question:

```text
Does a pretreatment tumor with a stronger measured burden along any retained malignant-route spoke
have a lower probability of CR/PR under anti-PD-1 therapy?
```

This is a frozen retrospective hypothesis to be tested, not an established biological law.

## Frozen route-proxy set

Only repository-retained directional markers with direct transcript-level availability are admitted in this first feature:

```text
ROUTE_1 := KDM5B-high slow-cycling / reseeding persister proxy
ROUTE_2 := CD36-high SMC residual-state proxy
ROUTE_3 := MITF-high pigmented residual-state proxy
ROUTE_4 := MTHFD2-high mTOR/ATF4/MTHFD2 persistence proxy
ROUTE_5 := NGFR-high NCSC proxy
ROUTE_6 := NT5E-high / CD73 adenosine immune-escape proxy
ROUTE_7 := SOX10-low invasive/MRD proxy
```

Evidence anchors already retained by the repository:

```text
docs/status/MELANOMA_KDM5B_RESEEDING_BOUNDARY_2026_08_31.md
docs/status/MELANOMA_CD36_SMC_PEROXISOME_UGCG_RESIDUAL_2026_08_31.md
docs/status/MELANOMA_PIGMENTED_MITF_OXPHOS_RESIDUAL_2026_08_31.md
docs/status/MELANOMA_MTOR_ATF4_MTHFD2_UNABSORBED_RESIDUAL_2026_08_31.md
docs/status/MELANOMA_NCSC_FAK_MAPK_ROUTE_COMPRESSION_2026_08_31.md
docs/status/MELANOMA_CD73_ADENOSINE_RESIDUAL_2026_08_31.md
docs/status/MELANOMA_SOX10_LOW_DUAL_VULNERABILITY_2026_08_31.md
```

These genes are measurement proxies for retained route families. They are not asserted to uniquely identify a full cell state, pathway activity, or causal mechanism in an individual patient.

The set is frozen before locked-cohort outcome scoring. No marker may be added, removed, re-signed, or reweighted after inspecting `GSE91061` validation outcomes.

## Outcome-blind within-sample normalization

Let `x_pg` denote the expression value of gene `g` in pretreatment patient sample `p` after the source dataset's declared RNA-seq normalization.

For each patient independently, let `G_p` be the set of measured genes with finite expression values. Define the empirical within-sample percentile

```math
r_{pg}
:=
\frac{
  \#\{h\in G_p:x_{ph}<x_{pg}\}
  + \tfrac12\#\{h\in G_p:x_{ph}=x_{pg}\}
}{|G_p|}.
```

Thus

```math
0 < r_{pg} \le 1.
```

This transformation uses only the patient's measured transcriptome. It does not use treatment outcome labels, responder prevalence, or the distribution of other validation patients.

## Signed route-spoke values

For the six high-direction proxies define

```math
z_{pg}=r_{pg}
```

for

```text
KDM5B
CD36
MITF
MTHFD2
NGFR
NT5E
```

and for the SOX10-low route define

```math
z_{p,SOX10}=1-r_{p,SOX10}.
```

Every spoke therefore has the same orientation:

```text
larger z := more expression support for the corresponding retained malignant-route proxy
```

## Spiderweb route-burden statistic

The first score is deliberately weight-free.

Define the malignant-route burden

```math
B_{route}(p)
:=
\max_{g\in G_{route}} z_{pg},
```

where

```text
G_route := {KDM5B, CD36, MITF, MTHFD2, NGFR, NT5E, SOX10-low}.
```

Interpretation:

```text
B_route(p) := strongest measured malignant-route spoke in the frozen proxy set
```

The maximum operator is chosen because the executable graph is fail-closed: one strongly supported escape/persistence spoke is sufficient to keep malignant-route burden high. This is not a statement that one transcript alone is biologically sufficient for resistance.

Define the frozen anti-PD-1 response score

```math
S_{PD1}(p):=1-B_{route}(p).
```

The prespecified directional hypothesis is

```text
higher S_PD1 -> greater probability of CR/PR rather than PD under anti-PD-1
```

No threshold is needed for the primary AUROC analysis.

## Missing-data rule

The seven proxy measurements are required for the primary score.

```text
PRIMARY_SCORE_ADMISSIBLE(p) := all seven route proxies measured with finite values
```

If any primary proxy is missing:

```text
PRIMARY_SCORE(p) := unavailable
```

No outcome-dependent imputation, marker substitution, or partial-score renormalization is permitted in the primary analysis.

A separately named sensitivity analysis may use a prespecified partial-score rule, but it cannot replace the primary result.

## Cohort lock

The predictive-validation protocol remains:

```text
DEVELOPMENT_COHORT := GSE78220
LOCKED_VALIDATION_COHORT := GSE91061_PRETREATMENT
PRIMARY_ENDPOINT := CR/PR versus PD
UNIT := patient
```

This feature definition is frozen before validation scoring.

`GSE78220` may be used to confirm that the seven genes can be parsed and that the score is numerically computable. Its outcomes may not be used to alter this feature definition after the fact.

`GSE91061` outcomes may be used only after the parser, patient deduplication, endpoint mapping, and score computation are executable and frozen.

## Claim-state flags

At this stage:

```text
ROUTE_BURDEN_FEATURE_DEFINED := true
RETROSPECTIVELY_VALIDATED_PREDICTIVE_MODEL := false
VALIDATED_TREATMENT_SELECTION_SYSTEM := false
CANCER_CURE_ESTABLISHED := false
```

A favorable development-cohort association cannot change any of the last three flags.

## What would promote the first flag

The next promotion target is only:

```text
RETROSPECTIVELY_VALIDATED_PREDICTIVE_MODEL
```

and it remains governed by `MELANOMA_PREDICTIVE_VALIDATION_GATE_2026_09_06.md`, including independent validation, uncertainty, calibration, leakage checks, and replication on a second independent melanoma cohort.

## Boundary

```text
BOUNDARY :=
a frozen, outcome-blind patient-to-route feature map now exists for public pretreatment
RNA-seq data, but no patient outcomes have been scored and no predictive validity,
treatment-selection utility, clinical efficacy, or cure is established
```

## Next bounded action

```text
NEXT_ACTIONS :=
1. Implement an executable parser that computes within-sample percentiles and S_PD1 from a pretreatment RNA-seq matrix without reading outcome labels.
2. Implement patient-level deduplication and the frozen CR/PR-vs-PD endpoint parser as a separate verified step.
3. Confirm numerical computability on GSE78220 without changing the frozen marker set or signs.
4. Only then score the locked GSE91061 pretreatment cohort once and report the full validation gate metrics.
5. Fail closed if the validation gate is not met.
```
