# Melanoma ER-exit B16-F10 candidate — first failed clause — 2026-09-06

## Status

`CONDITIONAL / EVIDENCE-GATE AUDIT`

This document tests the strongest retained melanoma near-exit observation against the ordered `EXIT_EVIDENCE_ADMISSIBLE` gate introduced for the spiderweb / ER-exit geometry. It does not identify a treatment, establish clinical efficacy, or claim cure.

## Candidate

The cited 2025 Blood abstract reports:

```text
intratumoral IL-12+ADA engineered E. coli
  -> complete regression in a B16-F10 melanoma model
  -> 100% survival
  -> tumor rechallenge confirming durable antitumor immunity
```

The rechallenge result materially strengthens the candidate because it provides same-arm evidence of durable antitumor immune memory after complete regression.

Evidence anchor:

- Sendker et al., Blood 2025 supplement / ASH poster 5912, `Dual-function engineered bacteria remodel AML tumor microenvironment via IL-12 delivery and adenosine depletion to sustain NK cell immunity`.
  - https://doi.org/10.1182/blood-2025-5912

## Ordered gate test

The first evidence clause is:

```text
CLAUSE_1 :=
absence of viable malignant state on the declared measurement surface
```

The complete-regression plus rechallenge result still does not establish this clause.

A regression outcome and successful rechallenge are not, by themselves, direct certificates that no viable melanoma cells remained immediately after the original tumor regression. The cited abstract does not declare, for the original B16-F10 complete-regression arm, a residual-viability assay surface with sampled compartments and a detection threshold sufficient to infer zero viable malignant state.

Therefore:

```text
B16_COMPLETE_REGRESSION
+ B16_DURABLE_RECHALLENGE_IMMUNITY
  !=
CERTIFIED_ABSENCE_OF_VIABLE_MALIGNANT_STATE
```

and

```math
EXIT\_EVIDENCE\_CLAUSE_1(B16\text{-}F10) = \mathrm{UNPROVED}.
```

## What the rechallenge result does strengthen

The new same-arm evidence should not be discarded.

```text
ESTABLISHED_AT_ABSTRACT_LEVEL :=
complete regression
+ 100% survival
+ tumor rechallenge with durable antitumor immunity
```

This is stronger than a regression-only near-miss and may become relevant to the later recurrence/reseeding clause after Clause 1 is discharged.

However, because the exit gate is ordered:

```text
STOP_AT_FIRST_FAILURE := CLAUSE_1
DO_NOT_PROMOTE_CLAUSE_2..CLAUSE_5_TO_CLOSURE_CREDIT
```

The later evidence may be retained as supportive information but cannot make `H` admissible while Clause 1 remains unproved.

## Weakest missing object

```text
MISSING_OBJECT :=
a matched B16-F10 residual-viability certificate for the original complete-regression arm
that declares the sampled tissue/compartments, assay modality, detection threshold,
and observation time and establishes no detectable viable malignant melanoma state
on that declared measurement surface
```

Examples of measurements that could contribute to such a certificate include pathology/histology tied to the regressed site, sensitive residual tumor-burden imaging, viable-cell recovery/culture, or another explicitly quantified residual-disease assay. The required object is the measurement certificate itself, not any particular assay named here.

Even such a certificate would discharge only Clause 1; it would not automatically prove the full `EXIT_ADMISSIBLE` gate.

## Boundary

```text
BOUNDARY :=
not proved that the B16-F10 complete-regression state contains zero viable malignant
melanoma on a declared sufficiently sensitive measurement surface; the same-arm
rechallenge result strengthens durability evidence but does not discharge Clause 1
```

## Next bounded action

```text
NEXT_ACTIONS :=
1. Search for a same-arm B16-F10 pathology, histology, residual tumor-burden,
   viable-cell, or other quantified residual-disease measurement tied to the
   complete-regression cohort.
2. If none is reported, retain Clause 1 as the first unresolved ER-exit barrier.
```
