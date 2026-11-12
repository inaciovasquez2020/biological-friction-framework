# Constraint-preserving dissipation on rational 5D face-count data

**Classification:** mathematical construction PROVED by elementary linear algebra;
bounded exact computational validation subject to CI; new Lean theorem **NOT_RUN**.
No fifth spatial dimension, measured biological coupling, or geometric evolution
is established.

## Verified source boundary

- BFF main at `ea1fa377a5464b70119131827cd60df759014356`: Dehn–Sommerville rank-three face-count relations and five-coordinate rational toy dissipation.
- Pachner main at `6252f3ab377ecd5f7c276290a356a20a05eb3bb5`: exact finite joined 5D bistellar-move transport and reversibility obstruction.

## Rational geometric relaxation and mathematical theorem

Let `V` be the rational vector subspace of `Q^6` cut out by the
three Dehn–Sommerville equations:

```
f0-f1+f2-f3+f4-f5=0
-4*f0+4*f1-3*f2+2*f3-f4=0
5*f0-5*f1+3*f2-f3=0
```

Every PL 5-sphere face-count vector belongs to `V`. The converse is
false: `V` includes fractional vectors and vectors of impossible
triangulations. Fix a reference `f* ∈ V` and a rational `0<q<1`.
Define the affine contraction

```
T_q(f) = f* + q (f - f*)
E(f)   = 1/2 sum_i (f_i - f*_i)^2 .
```

**Theorem.** For every `f ∈ V`: `T_q(f) ∈ V`, and
`E(T_q(f)) = q² E(f)`. Consequently energy strictly decreases whenever
`f != f*`, and `T_q^m(f) = f* + q^m(f-f*)`. Proof: linearity of the
three constraints, then homogeneity of the squared norm.

This is an exact, non-vacuous constraint-preserving dissipative evolution
on the rational *relaxation*. It does NOT produce elementary Pachner
moves and does not ensure entries are integer, nonnegative, or
realizable as a PL sphere triangulation.

## Precise realizability obstruction

Choose `f*` from `boundary(4-simplex) * boundary(triangle)`,
whose face counts are `(8,28,55,65,45,15)`. Apply a legal base
3D `1→4` move before the join, obtaining the actual 5-sphere
face-count vector `(9,35,76,98,72,24)`. The difference is

`(1,7,21,33,27,9)`.

At `q=1/2`, the affine midpoint has first entry `17/2`, so it
cannot be a face-count vector for any finite simplicial complex.
It still satisfies all three Dehn–Sommerville equations. This is a
decisive witness that preserving those constraints and dissipating
energy are insufficient for genuine geometric evolution.

Even integer nonnegative vectors satisfying Dehn–Sommerville may fail
other PL-sphere feasibility constraints. One must independently certify
a triangulation and legal move at each discrete transition.

## Reproducibility

Run `python3 tools/verify_5d_ds_preserving_dissipation.py` with
standard Python. It independently enumerates 3D base complexes after
`1→4` and `2→3`, joins them to circles with 3–15 edges, computes
all six f-numbers exactly, and checks 10 rational evolution steps for
each of 39 source complexes: **390 rational steps**. Each step checks
the Dehn–Sommerville equations, energy reduction by a factor 1/4,
and the closed-form formula for the iterated contraction. Additional
negative tests check fractional midpoint and a diagonal contraction
that violates the face-count constraints. The checker refuses
`python3 -O` to avoid silent skipped assertions.

**OPEN:** A state-selection rule on *actual triangulations* which
defines dissipative admissibility, proves energy change for each
chosen move, and identifies a measured biological or physical variable
with the geometric potential. The 5D state dimension and the 5D
simplicial dimension cannot be equated solely by this algebra.
