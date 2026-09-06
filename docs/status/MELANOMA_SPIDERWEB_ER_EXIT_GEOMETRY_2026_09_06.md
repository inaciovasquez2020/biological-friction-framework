# Melanoma spiderweb movement / ER-exit geometry — 2026-09-06

## Status

`CONDITIONAL / MODEL-LEVEL MATHEMATICS`

This document adds a mathematical state-space geometry on top of the existing interaction-aware melanoma graph. It does not add a biological target, treatment recommendation, clinical claim, or cure claim.

The phrase `Einstein-Rosen bridge` is used only as a geometric analogy for a distinguished low-friction corridor in biological state space. No spacetime or wormhole mechanism is asserted.

## Existing graph surface

Let

```text
G_x = (V, E_x)
```

be the context-indexed directed melanoma transition graph already represented by the repository, after applying the chosen control set and retaining all baseline and control-induced edges that remain admissible in biological context `x`.

## Spiderweb movement object

Assign each active directed edge `(i,j)` a symbolic positive friction

```math
rho_ij(x) > 0
```

and define a corresponding symbolic transition rate

```math
k_ij(x) = a_ij(x) exp(-beta rho_ij(x)),
```

where `a_ij(x) >= 0` is an attempt-rate factor and `beta > 0` is a scale parameter.

For a state occupancy distribution `p(t)`, define directed net flux

```math
J_ij(t) = p_i(t) k_ij - p_j(t) k_ji.
```

The web-level movement magnitude is

```math
W(t)^2 = sum_{(i,j) in E_x} rho_ij J_ij(t)^2.
```

Thus

```math
W(t) = sqrt(sum_{(i,j) in E_x} rho_ij J_ij(t)^2).
```

This is the movement indicator: motion is distributed over the full transition web rather than represented by one pathway.

If states are assigned plotting coordinates `y_i in R^2` for visualization only, define local web motion

```math
W_i(t) = sum_{j : (i,j) in E_x} J_ij(t) (y_j - y_i).
```

The coordinates do not change graph reachability or biological claim status.

## Exit set

Introduce an abstract set

```text
H subset V
```

intended to represent a validated non-malignant absorbing/terminal region.

The present repository does not currently provide such a validated exit set. Therefore `H` is a missing object and must not be instantiated by assumption.

Let `M subset V` denote the retained malignant/recurrent region.

## Exit committor

Conditional on a validated `H` and transition rates `k_ij`, define the exit committor

```math
q_i = P_i(tau_H < tau_M).
```

For interior states, `q` satisfies the discrete harmonic equation

```math
sum_j k_ij (q_j - q_i) = 0,
```

with boundary conditions

```math
q_i = 1,  i in H,
q_i = 0,  i in M.
```

The scalar `q_i` is the model probability of reaching the validated exit region before returning to the retained malignant/recurrent region, conditional on the chosen transition model.

## ER-exit direction

Define the local Einstein-Rosen exit-direction operator by

```math
ER(i) = argmax_{j : (i,j) in E_x} ([q_j - q_i]_+ / rho_ij),
```

where

```math
[z]_+ = max(z, 0).
```

Interpretation:

```text
ER(i) := the admissible local transition giving the largest increase in exit committor per unit biological friction.
```

This turns the requested `direction to the exit` into a precise optimization rule rather than a visual metaphor.

## Global bridge corridor

Define the path resistance of a directed path `gamma` by

```math
R(gamma) = sum_{e in gamma} rho_e.
```

Conditional on `H`, define the minimum-friction exit corridor

```math
Gamma_ER(i,H) = argmin_{gamma : i -> H} R(gamma).
```

and the associated exit resistance

```math
R_ER(i) = min_{gamma : i -> H} R(gamma).
```

This is the global `bridge` object. Its first edge provides a pathwise exit direction; the committor operator above provides the probabilistic local direction.

## Combined movement indicator

The proposed state-level indicator is

```math
I_i(t) = ( ||W_i(t)||, q_i, R_ER(i), ER(i) ).
```

Semantically:

```text
||W_i||  := current web movement magnitude
q_i      := conditional exit propensity
R_ER(i)  := minimum symbolic friction to the validated exit set
ER(i)    := local direction of greatest exit gain per unit friction
```

## Strengthening relative to plain reachability

The existing interaction-aware graph answers whether malignant/gap states remain reachable.

This geometry adds, conditionally:

```text
1. how strongly state occupancy is moving through the graph;
2. whether movement is locally increasing or decreasing exit propensity;
3. the least-friction path to a validated exit region;
4. a scalar ordering of states by exit committor and exit resistance.
```

This is strictly richer than binary reachability as mathematics, but it does not strengthen the biological evidence until `H`, `rho_ij`, and `k_ij` are externally grounded.

## Ranked gaps

```text
GAP_1 := validated exit set H is absent.
GAP_2 := evidence-derived edge frictions / transition rates are absent.
GAP_3 := state occupancy p(t) is not yet supplied by matched longitudinal data.
GAP_4 := any 2D spiderweb embedding is visualization-only unless separately justified.
```

`GAP_1` is logically prior: without a validated target boundary, an exit-direction operator cannot receive biological closure credit.

## Boundary

```text
BOUNDARY :=
the spiderweb / ER-exit construction is a mathematically defined conditional
geometry over the repository's melanoma transition graph, but no validated
non-malignant exit set H, evidence-derived friction metric, or transition-rate
calibration is currently certified; therefore it does not establish cancer
closure, treatment efficacy, or cure.
```

## Next bounded action

```text
NEXT_ACTIONS :=
1. Search retained melanoma evidence for the weakest defensible non-malignant terminal/absorbing state definition.
2. If none exists, keep H abstract and do not compute ER(i).
3. Only after H is grounded, define the first evidence-backed edge friction or transition-rate calibration.
4. Add one verifier property at a time and fail closed on any ungrounded edge or exit label.
```
