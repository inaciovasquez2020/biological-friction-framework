# Melanoma interaction-aware control invariant — 2026-08-31

## Status

`MODEL-LEVEL / LITERATURE-BOUNDED INVARIANT`

This document records a structural rule for the melanoma resistance graph. It is not clinical guidance, a treatment recommendation, or evidence of a cure.

## Problem

A static hitting-set model assumes that adding a control can only remove routes.

The retained melanoma literature no longer supports that monotone assumption.

Several already recorded examples show that a perturbation or state-control can suppress one route while exposing, inducing, or redirecting another:

```text
ApoE blockade
  -> favorable ferroptosis / immune effects
  AND
  -> unfavorable invasion / endothelial effects in other matched perturbation data

PI3K/mTOR suppression
  -> desired pathway suppression
  AND
  -> nuclear Polκ enrichment in the tested BRAF-V600E melanoma model

FAK-directed NCSC control
  -> removes the observed nongenetic NCSC trajectory
  AND
  -> surviving evolution can shift toward genetically fixed ERK-sensitive resistance

KDM5B manipulation
  -> direction-dependent phenotype effects;
     neither globally "increase" nor globally "decrease" is a valid monotone rule

ferroptosis control
  -> GPX4 and FSP1 dependence changes with metastatic niche / oxygen state
```

Therefore static route coverage is insufficient.

## Formal objects

Let:

```text
S := retained melanoma biological states
R := retained malignant-survival / dissemination / immune-escape routes
C := abstract functional controls
X := biological context (genotype, niche, treatment pressure, time)
```

For a control `c in C` and context `x in X`, define:

```text
Hit(c, r, x)
```

to mean that `c` is experimentally supported to suppress route `r` in context `x`.

Define:

```text
Induce(c, x)
```

as the set of experimentally supported states, route activations, trajectory shifts, or compensatory programs that become increased/reachable after applying an implementation of `c` in context `x`.

`Induce` is evidence-bounded: unknown effects are not invented.

## Local closure-credit invariant

A control does not receive closure credit merely because it hits its intended route.

```text
CONTROL_CREDIT(c, r, x) :=
    Hit(c, r, x)
AND
    forall s in Induce(c, x), Covered(s, x)
```

where `Covered(s, x)` means that every retained malignant escape route reachable from `s` in that context is already controlled by an independently supported constraint.

In words:

```text
A control earns closure credit only if its known induced escape states are also covered.
```

## Combination-level invariant

For a control set `U subset C`, define the interaction-aware reachable set:

```text
Reach_plus(U, x)
```

as the closure of the initial melanoma states under both:

```text
1. baseline biological transitions, and
2. experimentally supported control-induced transitions from every c in U.
```

Then the sufficient graph-level closure condition is:

```text
INTERACTION_AWARE_CLOSURE(U, x) :=
    no retained malignant terminal / recurrent escape state
    is reachable in Reach_plus(U, x)
```

This replaces the weaker static condition:

```text
STATIC_HIT_SET(U) := every baseline route is hit at least once
```

because `STATIC_HIT_SET` ignores routes created or exposed by the controls themselves.

## Why one-pass checking is insufficient

Control interactions can be recursive.

A control may induce a state that is handled by a second control, while the second control may induce another state.

Therefore the graph must be closed iteratively:

```text
Q0 := initial states
Q(n+1) :=
  Qn
  union baseline_successors(Qn)
  union control_induced_successors(Qn, U)

Q* := least fixed point of Qn
```

Closure credit is evaluated on `Q*`, not only on baseline routes.

## Known interaction classes already present in the repository

### Signed perturbation

```text
ApoE blockade := mixed-sign effect vector
```

A single scalar "beneficial" label is invalid.

### Compensatory stress induction

```text
PI3K/mTOR suppression -> nuclear Polκ state
```

This is a conditional implementation-level induced edge.

### Evolutionary redirection

```text
FAK-dependent NCSC route suppressed
  -> observed surviving evolution can return to ERK-sensitive genetic resistance
```

The second trajectory must remain covered by dynamic MAPK control.

### State-direction ambiguity

```text
KDM5B-high state
```

can be exploited by different experimental strategies in opposite directions, so the graph control is reseeding prevention rather than monotone KDM5B increase/decrease.

### Context-dependent dependency switch

```text
hypoxic LN -> FSP1 dependency
blood / hematogenous transit -> GPX4 dependency
```

The transition handoff remains unresolved.

### Temporal signaling escape

```text
low mean ERK != no functional ERK escape
```

`C_MAPK_DYNAMIC` therefore operates on signaling trajectories rather than snapshots.

## Structural consequence

The melanoma model is no longer a conventional static hitting-set problem.

The retained object is closer to a signed, context-indexed intervention-transition system:

```text
baseline state graph
+
control-removal edges
+
control-induced edges
+
time/niche-dependent state transitions
```

Therefore:

```text
RETIRE :=
"cover every baseline pathway once => residual disease closed"
```

and retain:

```text
REQUIRED :=
interaction-aware fixed-point reachability under the chosen control set
```

## What this invariant does not claim

```text
DO_NOT_INFER :=
interaction-aware graph closure => clinical cure

DO_NOT_INFER :=
all intervention-induced biology is known

DO_NOT_INFER :=
a currently covered induced state is universally covered across all contexts
```

The invariant only prevents the model from granting closure credit while ignoring already known adverse or compensatory transitions.

## Weakest executable missing object

```text
MISSING_OBJECT :=
a repository-native machine-readable interaction graph and verifier containing:

1. state identifiers,
2. baseline directed edges,
3. context labels,
4. abstract control identifiers,
5. experimentally supported Hit edges,
6. experimentally supported Induce edges,
7. signed outcome labels where needed,
8. temporal/niche transition labels,
9. fixed-point reachability computation,
10. fail-closed rejection if a retained malignant escape state remains reachable.
```

The verifier must not infer absent biological edges from pathway diagrams. Every nontrivial `Hit` or `Induce` edge should cite a repository evidence object.

## Boundary

```text
BOUNDARY :=
the literature-backed melanoma graph now requires interaction-aware closure;
a machine-checked interaction graph has not yet been implemented
```

## Repository evidence anchors

This invariant is synthesized from the bounded status results already retained in this repository, including:

```text
MELANOMA_APOE_1D7_BRIDGE_2026_08_31.md
MELANOMA_MTOR_POLK_ANTAGONISTIC_COUPLING_2026_08_31.md
MELANOMA_NCSC_FAK_MAPK_ROUTE_COMPRESSION_2026_08_31.md
MELANOMA_KDM5B_RESEEDING_BOUNDARY_2026_08_31.md
MELANOMA_FERROPTOSIS_NICHE_SWITCH_2026_08_31.md
MELANOMA_ERK_PULSE_DYNAMIC_MAPK_BOUNDARY_2026_08_31.md
```

## Next bounded action

```text
NEXT_ACTIONS :=
1. Treat CONTROL_CREDIT and INTERACTION_AWARE_CLOSURE as the model-level invariants.
2. Do not add another biological target until the interaction representation is inspected.
3. Identify the smallest existing repository location suitable for a machine-readable
   state/control graph without inventing a new architecture.
4. Implement only a minimal fail-closed verifier if repository-native structure supports it.
```
