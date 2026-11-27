# Hidden thermodynamic dissipation in cyclic reaction networks

## Classification

Scoped mathematical certificate: LEAN_VERIFIED on macOS.
Independent CI reproduction required for integration.
Biological empirical validation and independent novelty remain OPEN.

## Mathematical result

For finite cyclic continuous-time Markov generators with at least
three states, strictly positive normalized stationary probabilities,
positive edge traffic t_i and circulating current |J| <= M < t_i,
entropy production is

    sigma(J) = J * sum_i log((t_i + J)/(t_i - J)).

For fixed stationary probabilities and traffic, the exact minimax
absolute estimation error is

    E* = sigma(M)/2.

The observation relation includes stationary probabilities, edge
traffic, total exit rates, and independent gauge equivalence on
injective directed paths of bounded length.

An equilibrium model and a driven model have identical specified
observations but different entropy production when M > 0.

## Load-bearing declarations

- BFF.HiddenDissipation.generator_stationary
- BFF.HiddenDissipation.entropyProduction_eq
- BFF.HiddenDissipation.sameObservation_fixed
- BFF.HiddenDissipation.equilibrium_driven_collision
- BFF.HiddenDissipation.ring_observation_minimax

## Mathematical antecedents

Chronos local-to-global holonomy:
https://github.com/inaciovasquez2020/chronos-urf-rr/blob/5a88ac8e790a2bef5da5b03b538a64ce08afdf12/lean/Oblivion/LocalityHolonomySeparation.lean

URF-Core sharp minimax methodology:
https://github.com/inaciovasquez2020/urf-core/blob/9b9e2d7cbc59c466009c659de53a03985858cc51/lean/URF/Foundation/CyclePartitionRadiusMinimax.lean

These are mathematical antecedents, not imported software
dependencies of this standalone certificate.

## Verification

The extended Mac source and receipt are preserved byte-for-byte in receipt/.
The original 33-declaration certificate and receipt remain available at
commit 799b41b4692c71589587cba037f26f0ad4bff7fb.
The original Lean source is an unchanged prefix of the extended source.

Lean: 4.29.0
Mathlib: 69cbc416b3f58ba11e331db067644d0508e78341
Original Mac Chronos HEAD:
a999b816df08bc393036cc7ebe8d0a6ed1939b6b

41 declarations audited with only the permitted standard Lean axioms.

With pinned dependencies installed:

    (cd receipt && shasum -a 256 -c SHA256SUMS)
    lake build
    lake env lean receipt/HiddenDissipation.lean > fresh.log 2>&1
    python3 audit.py fresh.log

## Scope exclusions

No universal biological law, empirical validation, unrestricted
observation obstruction, clinical conclusion, independent novelty,
or repository-wide theorem closure is claimed.

The result does not assert that actual biochemical networks satisfy
the stated observation model. Direction-resolved measurements and
richer temporal statistics may distinguish the models.

Existing repository-level conditional status remains unchanged.


## Second-order identifiability extension

Eight additional declarations establish recovery identities
within the specified model families.

### Biological generator recovery

For the existing cyclic RingModel, write

    K_i(J) = (Q_J^2)_ii.

Then

    K_i(J) = K_i(0) - c_i J^2,

where

    c_i = 1/(4 p_i p_next) + 1/(4 p_i p_prev) > 0.

Consequently, the original stationary observations together
with one diagonal generator-square observable determine
the squared circulating current and entropy production.

Load-bearing declaration:
BFF.HiddenDissipation.entropy_identified_by_curvature.

The connection between the generator square and the second
derivative of the continuous-time transition semigroup is
not formalized in this certificate.

### Cosmological coefficient recovery

For the restricted coefficient family

    C_n = lambda*n^4/(2*b^3),

a known positive radius b and nonzero mode n give

    lambda = 2*b^3*C_n/n^4.

The zero mode is insensitive to lambda.

Load-bearing declaration:
BFF.HiddenDissipation.mode_identifiable.

Pinned DFM-MKC Cosmology antecedent:
https://github.com/inaciovasquez2020/dfm-mkc-cosmology/blob/bda11ce1347aeda076571de137e99ac93cd7e723/research/5d/mixed_spectral_hessian_nonidentifiability_audit.py

The coefficient inversion is Lean-verified. The covariant
action variation and Fourier reduction are not formalized here.
No general cosmological parameter identification is claimed.

### Scope

These are two instances of higher-order identifiability,
not a theorem identifying biological and cosmological physics.

Empirical applicability, experimental measurement feasibility,
full analytic formalization and independent novelty remain OPEN.

Repository-wide conditional research status is unchanged.
