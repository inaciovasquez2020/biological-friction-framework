# Melanoma exit-set admissibility gate — 2026-09-06

## Status

`CONDITIONAL / MODEL-LEVEL MATHEMATICS`

This document sharpens the missing exit object used by the spiderweb / ER-exit geometry. It does not identify a treatment, establish clinical efficacy, or claim cure.

## Existing obstruction

The current executable melanoma graph contains three states marked non-malignant:

```text
therapy_pressure
melanoma_context
metastatic_context
```

but these are context/source states with outgoing paths into malignant states. Therefore

```text
non-malignant label != admissible exit state
```

The retained evidence also contains a B16-F10 complete-regression near-miss under an IL-12+ADA engineered-bacteria combination, but the repository explicitly does not promote that observation to durable melanoma closure.

## Exit-set gate

Let

```text
G_x = (V,E_x)
M subset V := retained malignant/recurrent/gap states
H subset V := proposed exit set
Reach_plus(v,x) := interaction-aware fixed-point reachable set from v
```

Define graph-level exit admissibility by

```math
EXIT_GRAPH_ADMISSIBLE(H,x) :=
  (H \ne \varnothing)
  \land (H \cap M = \varnothing)
  \land \left(\forall h\in H,\; Reach_+(h,x)\cap M=\varnothing\right).
```

Equivalently, no state admitted to `H` may have a retained baseline or control-induced path back into any malignant, recurrent, or unresolved-gap state.

This is stronger than requiring only

```text
h.malignant = false
```

because a non-malignant context node can still feed malignant trajectories.

## Evidence-level gate

Graph safety alone is not enough to create a biological exit state. Define

```text
EXIT_EVIDENCE_ADMISSIBLE(H,x) :=
for every proposed h in H, there is matched-context evidence supporting:

1. absence of viable malignant state on the declared measurement surface;
2. absence of retained reseeding / recurrence state on that surface;
3. no known transition from h into a retained malignant/gap state is omitted;
4. the observation horizon and assay sensitivity are explicitly declared;
5. the evidence path is repository-anchored and inspectable.
```

Then the full gate is

```math
EXIT_ADMISSIBLE(H,x)
:= EXIT_GRAPH_ADMISSIBLE(H,x)
\land EXIT_EVIDENCE_ADMISSIBLE(H,x).
```

Only an `H` satisfying this gate may be used as the boundary condition

```math
q_i = 1 \quad (i\in H)
```

in the ER-exit committor problem.

## Near-miss test

The retained B16-F10 complete-regression report does not discharge this gate.

It is useful evidence of a strong tumor-control outcome, but the repository records missing matched mechanistic attribution and does not establish durable source-independent melanoma closure. Therefore it cannot, by itself, instantiate an absorbing `H`.

```text
COMPLETE_REGRESSION_OBSERVATION
  !=
EXIT_ADMISSIBLE(H,x)
```

## Consequence for the ER direction

The spiderweb / ER geometry remains mathematically defined but biologically uninstantiated:

```math
ER(i)
= \operatorname*{arg\,max}_{j:(i,j)\in E_x}
  \frac{[q_j-q_i]_+}{\rho_{ij}}
```

may not receive biological interpretation until an exit set passes `EXIT_ADMISSIBLE`.

Thus the construction now fails closed at a precise gate rather than at an informal phrase such as "validated non-malignant state."

## Ranked gaps

```text
GAP_1 := no retained state currently satisfies EXIT_ADMISSIBLE.
GAP_2 := edge frictions / transition rates remain uncalibrated.
GAP_3 := matched longitudinal occupancy p(t) remains absent.
```

## Boundary

```text
BOUNDARY :=
no retained melanoma state is currently certified as an absorbing non-malignant
exit set for the ER-exit geometry; complete regression in one bounded experiment
is insufficient without the graph-level and evidence-level no-return gate
```

## Next bounded action

```text
NEXT_ACTIONS :=
1. Search retained melanoma status objects for the strongest candidate observation
   that could satisfy one clause of EXIT_EVIDENCE_ADMISSIBLE, and record exactly
   which clause fails first.
```
