# Melanoma ER-exit B16-F10 candidate — first failed clause — 2026-09-06

## Status

`CONDITIONAL / EVIDENCE-GATE AUDIT`

This document tests the strongest retained melanoma near-exit observation against the ordered `EXIT_EVIDENCE_ADMISSIBLE` gate introduced for the spiderweb / ER-exit geometry. It does not identify a treatment, establish clinical efficacy, or claim cure.

## Candidate

The retained melanoma evidence records:

```text
intratumoral IL-12+ADA bacteria -> complete regression in a B16-F10 melanoma arm
```

The same retained status object classifies this as a near-miss rather than durable melanoma closure.

## Ordered gate test

The first evidence clause is:

```text
CLAUSE_1 :=
absence of viable malignant state on the declared measurement surface
```

The retained `complete regression` statement does not establish this clause.

A complete-regression tumor outcome is not, by itself, a direct certificate that no viable melanoma cells remained. The retained repository evidence does not provide, for the same B16-F10 arm, a declared residual-viability assay surface with a detection threshold sufficient to infer zero viable malignant state.

Therefore:

```text
B16_COMPLETE_REGRESSION
  !=
CERTIFIED_ABSENCE_OF_VIABLE_MALIGNANT_STATE
```

and

```math
EXIT\_EVIDENCE\_CLAUSE_1(B16\text{-}F10) = \mathrm{UNPROVED}.
```

## Fail-closed consequence

Because the gate is ordered, no later exit-evidence clause receives closure credit in this audit.

```text
STOP_AT_FIRST_FAILURE := CLAUSE_1
DO_NOT_TEST_AS_CLOSURE_CREDIT := CLAUSE_2..CLAUSE_5
```

The B16-F10 observation may remain a strong regression near-miss, but it cannot instantiate the absorbing exit set `H` used by the ER committor boundary condition.

## Weakest missing object

```text
MISSING_OBJECT :=
a matched B16-F10 residual-viability certificate for the complete-regression arm
that declares the sampled tissue/compartments, assay modality, detection threshold,
and observation time and establishes no detectable viable malignant melanoma state
on that declared measurement surface
```

Even such a certificate would discharge only Clause 1; it would not automatically prove recurrence/reseeding safety or the full `EXIT_ADMISSIBLE` gate.

## Boundary

```text
BOUNDARY :=
not proved that the retained B16-F10 complete-regression observation contains
zero viable malignant melanoma state on a declared sufficiently sensitive
measurement surface; therefore it cannot yet be used as H
```

## Next bounded action

```text
NEXT_ACTIONS :=
1. Search retained B16-F10 / IL-12+ADA evidence specifically for a residual-viability,
   rechallenge, pathology, or sensitive tumor-burden assay tied to the complete-regression arm.
2. If no such same-arm measurement exists, retain Clause 1 as the first failure and stop.
```
