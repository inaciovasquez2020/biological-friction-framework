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

Original source and receipt are preserved byte-for-byte in receipt/.

Lean: 4.29.0
Mathlib: 69cbc416b3f58ba11e331db067644d0508e78341
Original Mac Chronos HEAD:
a999b816df08bc393036cc7ebe8d0a6ed1939b6b

33 declarations audited with only the permitted standard Lean axioms.

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
