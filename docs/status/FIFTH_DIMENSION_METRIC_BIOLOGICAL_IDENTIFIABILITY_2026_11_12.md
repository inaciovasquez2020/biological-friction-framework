# Fifth-dimensional geometry versus five-state biology: identifiability gate

**Scientific verdict:** PHYSICAL EXTRA DIMENSION = OPEN; BIOLOGICAL
COUPLING = OPEN. Neither is proved by this repository. The included
mathematical obstruction and exact finite witness specify the weakest
additional inputs needed before those claims can be tested.

**Audited sources:** BFF main `c218f7f727c149fa1864a94387e7e819b0311f1c`;
Pachner main `a0962c0da22f6b48c021b583bb996b00daba994b` (axiom-free
mixed-carrier join/link formalization). Exact verified BFF face-count
rigidity and rational relaxation are documented separately. A manifold's
topological dimension, a five-coordinate state space, and an additional
physical spacetime coordinate have different operational meanings.

## Rigorous mathematical nonidentifiability obstruction

Consider the combinatorial 5-sphere `K=boundary(6-simplex)`.
Its unweighted face incidence structure has `f=(7,21,35,35,21,7)`.
On every five-simplex assign consistent equilateral Euclidean edge
lengths `ell=1`. Glue along matching faces. This gives a piecewise
Euclidean metric on the underlying 5-dimensional polyhedron.

Now repeat on the **same** simplicial complex with `ell=2`.
Every face, link, and combinatorial bistellar adjacency stays
unchanged, yet all intrinsic lengths double, and every 5-volume
increases by a factor `2^5=32`. For a regular 5-simplex, the
edge-vector Gram matrix has diagonal `ell^2` and off-diagonal
`ell^2/2`; its determinant is `3*ell^10/16`.
Thus the two metric assignments are mathematically valid and
distinguishable by metric observations but **indistinguishable by
unweighted combinatorial face counts or incidence**.

This is a constructive proof that an algorithm whose only input is the
unweighted abstract triangulation cannot uniquely recover the
underlying metric length scale. The argument generalizes to uniform
positive rescaling of any compatible piecewise Euclidean metric.
Standard differential geometry likewise has `g -> c*g` changing
distances by `sqrt(c)`, scalar curvature by `1/c`, and n-volume
by `c^(n/2)` (see Princeton Ricci-flow notes, Lemma 1.19,
https://web.math.princeton.edu/~nsher/ricciflow.pdf ).

**Important limitation:** This does NOT show that geometric metric data
cannot be added, that a 5D manifold is impossible, or that extra
physical dimensions are absent. It shows that combinatorial
topology alone does not determine calibrated geometry, causal
propagation, clock rates, physical observables, or biological dynamics.

## Precise possible meanings of a fifth dimension

1. **Five-dimensional state-space coordinate** `x_5`: an internal
   latent degree of freedom in an ordinary dynamical system. Such
   models routinely live in four-dimensional spacetime; their fifth
   state coordinate does not introduce an extra spatial direction.
2. **Fifth-dimensional simplicial space:** combinatorial PL dimension
   five, as in `K` above. This is geometric/topological, but the
   metric, time-signature and physical dynamics have not been supplied.
3. **Physical extra spacetime coordinate:** requires a five-dimensional
   metric with declared signature (for example one time and four space
   dimensions), specified matter/field couplings and equations of
   motion. It must predict observable effects distinguishable from
   an ordinary 4D model; see Particle Data Group, *Extra Dimensions*
   https://pdg.lbl.gov/2025/reviews/rpp2024-rev-extra-dimensions.pdf .

The three meanings are not equivalent. Neither 5D face-count rigidity
nor the 5-state dissipative toy example provides the missing
identification or an observational discovery.

## Minimum testable model interface

Before promoting **PHYSICAL_5D := SUPPORTED**, explicitly specify:

- A 5D event/metric structure and the time/space signature; physical
  units for metric coefficients, fields and event clocks
- A concrete measurable map `O_5` from that structure to observed
  gravitational, cosmological or biological quantities
- A matched 4D null model `O_4` using the same input information,
  observational units and calibration freedoms
- At least one preregistered **different prediction** after all shared
  nuisance parameters are optimized, not merely a different latent
  coordinate labeling
- Independent measurement data with uncertainties, selection
  effects, calibration and dimensional/parameter identifiability audits
- Tests of locality, causal consistency, symmetry and energy
  conservation/dissipation under the selected dynamics

Before promoting **BIOLOGICAL_COUPLING := SUPPORTED**, additionally
identify the biological variables, their measurement procedures,
dimensionless normalization or physical units, a quantitative coupling
to geometry, controlled/longitudinal data, and predictive performance
against a simpler matched state-space baseline.

A scientific hypothesis with no distinguishing observational
prediction is currently **not identified**, even if its equations are
internally consistent. Empirical support cannot be manufactured by
proof-assistant compilation or finite synthetic simulation.

## Reproducibility and exact scope

`python3 tools/verify_5d_metric_identifiability_obstruction.py`
uses only the Python standard library, reconstructs the 7-facet
5-sphere, checks its full f-vector, and verifies four distinct
consistent equilateral edge-length models using exact rational Gram
determinants. It explicitly compares `ell=1` with `ell=2`
and rejects optimized Python (`-O`).

**COMPUTATION_PASS** means the exact finite construction passes.
The general metric-rescaling argument is ordinary mathematics;
**LEAN_VERIFIED = NO** for that new argument. No physical data were
analyzed and no physical fifth-dimensional or biological mechanism is
claimed.

**RESEARCH STOP BOUNDARY:** The geometry needs full 5D bistellar
star/link/nonface/collision formalization. Physical identification
needs a specified metric/field theory, measurable coupling, and
discriminating external observations. Neither obligation can be
replaced by adding more abstract coordinates.
