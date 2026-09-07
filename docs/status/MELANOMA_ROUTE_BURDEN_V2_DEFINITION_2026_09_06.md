# Melanoma route-burden v2 definition — 2026-09-06

## Status

`CONDITIONAL / FROZEN SUCCESSOR FEATURE DEFINITION`

This document defines one separately versioned successor to the retired v1 route-burden score.

It does not establish predictive validity, treatment selection, clinical efficacy, or cure.

## Why v2 exists

V1 used within-tumor transcriptome percentiles and then

```math
B_{route}^{(1)}(p)=\max_g z_{pg}.
```

The exact GSE78220 development audit was negative:

```text
AUROC := 0.49404761904761907
```

V1 is retired and may not be retuned under the v1 name.

V2 changes exactly two structural elements:

```text
1. NORMALIZATION:
   within-tumor gene rank
   -> development-reference, marker-specific empirical CDF

2. AGGREGATION:
   maximum spoke
   -> unweighted arithmetic mean of all seven spokes
```

The marker set and biological directions are unchanged.

## Frozen marker set

```text
HIGH := KDM5B, CD36, MITF, MTHFD2, NGFR, NT5E
LOW  := SOX10
```

No marker may be added, removed, re-signed, or outcome-weighted within v2 after this definition is frozen.

These remain expression proxies for retained route families, not complete causal state definitions in an individual patient.

## Development reference population

Let

```text
D := GSE78220 samples retained by the already-frozen response-blind sampling rule:
     earliest pretreatment biopsy ordinal per patient
```

The reference set is constructed from expression/sample metadata only. Response labels are not used to estimate any v2 normalization parameter.

Every reference patient must have finite measurements for all seven frozen route genes.

For the currently audited GSE78220 surface this gives the first pretreatment biopsy per patient, including `Pt27A`, excluding later `Pt27B`, and excluding on-treatment `Pt16`.

## Marker-specific development ECDF

Let `x_pg` be the declared source-normalized expression of route gene `g` in patient `p`.

For each route gene `g`, freeze the empirical development-reference map

```math
F_g^{D}(x)
:=
\frac{
\#\{q\in D:x_{qg}<x\}
+\tfrac12\#\{q\in D:x_{qg}=x\}
}{|D|}.
```

For a development patient `p`, define

```math
u_{pg}:=F_g^{D}(x_{pg}).
```

For every later external-validation patient, the **same frozen GSE78220 map** `F_g^D` must be applied. No GSE91061 outcome or expression distribution may be used to refit, recenter, rescale, or rerank the map.

Values below the entire development reference receive `0`; values above it receive `1` under the same formula.

Because this is an order-based marker-specific map, a strictly increasing transformation applied consistently to both the development reference and queried expression values leaves the ordering unchanged. Cross-study measurement compatibility nevertheless remains an empirical validation issue.

## Signed route spokes

For

```text
KDM5B, CD36, MITF, MTHFD2, NGFR, NT5E
```

define

```math
z_{pg}^{(2)}:=\nu_{pg}.
```

For the SOX10-low route define

```math
z_{p,SOX10}^{(2)}:=1-\nu_{p,SOX10}.
```

Thus every v2 spoke has the orientation

```text
larger z^(2) := greater expression support for its retained malignant-route proxy
```

## V2 Spiderweb burden

Let

```text
G_route := {KDM5B, CD36, MITF, MTHFD2, NGFR, NT5E, SOX10-low}.
```

Define

```math
B_{route}^{(2)}(p)
:=
\frac{1}{7}
\sum_{g\in G_{route}}z_{pg}^{(2)}.
```

and the v2 anti-PD-1 directional score

```math
S_{PD1}^{(2)}(p):=1-B_{route}^{(2)}(p).
```

The frozen directional hypothesis remains

```text
higher S_PD1^(2) -> greater probability of CR/PR rather than PD under anti-PD-1
```

No route-specific weights are learned from outcomes. No top-k rule, maximum rule, marker selection, interaction term, nonlinear learner, or outcome-derived threshold belongs to v2.

## Missing-data rule

```text
V2_SCORE_ADMISSIBLE(p) := all seven route genes finite
```

Otherwise

```text
S_PD1^(2)(p) := unavailable
```

No marker substitution or partial-score renormalization is permitted in the primary v2 analysis.

## Development screen

Before GSE91061 can be accessed for v2, the unchanged v2 score must be evaluated once on the frozen GSE78220 CR/PR-vs-PD endpoint.

The prespecified development continuation screen is

```text
V2_DEVELOPMENT_CONTINUE :=
    AUROC > 0.60
    AND AUPRC > responder_prevalence
    AND observed direction is higher S_PD1^(2) for CR/PR
```

This is only a candidate-continuation screen. Passing it does not establish predictive validity.

If the screen fails:

```text
RETIRE_V2 := true
GSE91061_UNBLIND_FOR_V2 := false
```

No alternate aggregation or marker subset may be tried under the v2 name after seeing that result.

## Probability calibration gate

`S_PD1^(2)` is a ranking score, not a probability.

Only if `V2_DEVELOPMENT_CONTINUE` passes may a separately recorded development-only calibration map be fit and frozen before external validation.

The locked GSE91061 cohort may not be used to select or tune that calibration.

## Locked external validation

```text
LOCKED_VALIDATION_COHORT := GSE91061_PRETREATMENT
```

GSE91061 outcomes remain locked until all of the following are frozen and executable:

```text
- v2 route marker set
- v2 directions
- GSE78220 reference membership
- seven F_g^D maps
- arithmetic-mean aggregation
- missing-data handling
- patient deduplication
- endpoint mapping
- any development-only probability calibration
- validation metrics and pass/fail gate
```

## Claim state

```text
V2_FEATURE_DEFINED := true
V2_DEVELOPMENT_TESTED := false
RETROSPECTIVELY_VALIDATED_PREDICTIVE_MODEL := false
VALIDATED_TREATMENT_SELECTION_SYSTEM := false
CANCER_CURE_ESTABLISHED := false
```

Even a favorable GSE78220 v2 result cannot promote the last three flags.

## Boundary

```text
BOUNDARY :=
v2 is a separately versioned, mechanistically constrained successor designed to remove
v1's within-tumor/max saturation structure; it has not yet been development-tested,
independently validated, shown to select among treatments, or shown to cure cancer
```

## Next bounded action

```text
NEXT_ACTIONS :=
1. Implement the frozen seven marker-specific GSE78220 ECDF maps and unweighted mean scorer without accepting outcome labels.
2. Add unit tests that prove reference fitting and scoring are outcome-blind and that the frozen GSE78220 map is reused for external samples.
3. Run v2 exactly once on the frozen GSE78220 endpoint and apply V2_DEVELOPMENT_CONTINUE without changing the definition.
4. Keep GSE91061 locked unless the prespecified development screen passes and any required probability calibration is frozen first.
```
