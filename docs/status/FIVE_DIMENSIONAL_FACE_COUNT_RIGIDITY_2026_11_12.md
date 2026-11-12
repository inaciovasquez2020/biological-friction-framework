# 5D geometric face-count rigidity versus five-state biological models

**Classification:** Standard combinatorial topology theorem (mathematical derivation);
exact finite certificate (CI-gated); `LEAN_VERIFIED := NO`;
physical and biological identification **OPEN**.

Source revisions audited:
- `pachner-invariant` main `6252f3ab377ecd5f7c276290a356a20a05eb3bb5`, 5D Pachner join and reversible-dissipation certificates.
- This repository main `df6a6269d452c44b5c7ec6cb39b86309d8535b23`, rational five-coordinate dissipative observation example.

These source results use *different meanings of dimension*: simplicial-manifold
dimension 5 versus state-space dimension 5. The fact that the numeral agrees
does not identify their five-dimensional structures.

## The 5-sphere Dehn–Sommerville obstruction

Let `K` be a finite simplicial combinatorial (PL) 5-sphere, and let
`f_i(K)` be its number of i-dimensional faces, for `0<=i<=5`.

With `f_-1=1`, define `h_k = sum_(j=0)^k (-1)^(k-j)
binomial(6-j,6-k) f_(j-1)`, for `0<=k<=6`.
The classical Dehn–Sommerville theorem for simplicial spheres says
`h_0=h_6`, `h_1=h_5`, and `h_2=h_4`.

Expanding these three identities gives the linear equations
`f0-f1+f2-f3+f4-f5=0`,
`-4*f0+4*f1-3*f2+2*f3-f4=0`, and
`5*f0-5*f1+3*f2-f3=0`.

Solving yields EXACTLY

- `f3=5*f0-5*f1+3*f2`
- `f4=6*f0-6*f1+3*f2`
- `f5=2*f0-2*f1+f2`

Thus the full six-component face-count vector lies in a linear subspace
of dimension **at most three**. Any chosen five of these face counts
likewise supply at most three freely varying linear parameters.

**Precision:** This is a necessary linear constraint, not a claim that
every triple of nonnegative integers occurs as a 5-sphere face vector.
It does not assert that all 5D geometry has three physical degrees of
freedom: the triangulation's full incidence structure contains much
more information than the face-count vector.

## Consequence for this repository's five-coordinate observation bridge

The previously merged toy state model uses `x in Q^5` with five
independently selectable initial coordinates, strict contractive
dynamics, and a four-channel observation projection.

If someone tries to define those five independent coordinates as five
global face counts of a PL 5-sphere, the Dehn–Sommerville identities
obstruct the identification: the admissible image has rank at most three.
In particular `f3` and `f4` are functions of `(f0,f1,f2)`;
a putative fifth "hidden face-count coordinate" is not automatically
independent of four measured face counts.

A physically meaningful coupling must instead specify (i) which
geometric degrees of freedom are observed, (ii) a well-defined mapping
between actual biological states and geometric observables, and (iii)
which dynamics preserve the admissible geometric constraints.

## Exact bounded regression

Run `python3 tools/verify_5d_face_count_rigidity.py` with Python
standard library only. This checks the three expanded
Dehn–Sommerville linear equations and their coefficient rank (exact
rationals), independently counts the faces of joined sphere complexes
`K * C_n` with `n=3,...,15`, and checks the three successive
3D Pachner configurations (boundary of 4-simplex, one `1->4`, then
one `2->3`), for **39 exact joins**. It also checks Euler and ridge
incidences, h-vector symmetry, and the facet differences `+3n` and
`+n`.

Finite checks challenge implementation and assumptions; they do not
prove the Dehn–Sommerville theorem for all combinatorial spheres.
Optimization with `python3 -O` must fail closed.

**Remaining boundary:** A genuine feature map involving combinatorial
incidence, metric geometry, or physical fields could be higher
dimensional. No mathematical or biological evidence has yet justified
a five-state biological ↔ 5D geometric equivalence, nor any clinical
interpretation. Lean formalization and independent review remain open.
