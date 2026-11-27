# biological-friction-framework

A reference repository for the Biological Friction Framework.

## Scope

This repository presents a documentation-first framework artifact describing biological friction as a structural concept across biological systems.

The repository may contain notes, scripts, examples, workflows, formal mathematics, evidence maps, and support materials. Those artifacts support inspection and reproducibility but do not enlarge the claim boundary unless explicitly stated.

## Current reference Boundary

Primary current reference files:

- README.md
- STATUS.md
- FREEZE.md
- CITATION.cff

## Intended Content Areas

- conceptual framework
- mathematical formalization
- examples / toy models
- biological evidence maps and executable consistency certificates
- notes for future expansion
- support tooling

## Current Operational Surfaces

The repository contains distinct surfaces that must not be conflated:

- **Biological evidence / certificate surface:** active Python verifiers and tests check evidence provenance, melanoma interaction-graph consistency, unresolved-state accounting, and selected public-data analyses. These checks are computational consistency checks; they are not clinical validation or theorem-level proof of biology.
- **Formal mathematics surface:** Lean 4 files contain both completed proofs and explicitly conditional material. Some formal claims remain dependent on project-defined axioms, recorded proof gaps, or quarantined frontier assumptions.
- **Archived foreign-scope formal material:** archived Lean dependencies remain outside the active biological claim surface unless explicitly reintroduced and discharged.

## Non-Claims

This repository does not by itself:

- constitute clinical guidance
- provide medical diagnosis
- claim universal empirical validation
- replace peer-reviewed biological evidence

## Status

Repository-scope framework artifact with supporting infrastructure.

## Formal Status

Status: Conditional Framework / Frontier Claims

Build status:
- A successful Python certificate or CI check means only that the checked computational surface passes its declared consistency rules.
- A successful Lean build means the checked Lean target compiles.
- Neither result implies that axiom-dependent, admit-dependent, frontier-assumption-dependent, or otherwise conditional results prove their headline targets.

Theorem status:
- The current formal inventory contains project-defined axioms and recorded conditional/frontier dependencies; it is not an unconditional theorem-level closure.
- Current project `sorry` token count: **0**, as recorded by `docs/status/BFF_SORRY_QUARANTINE_2026_05_02.md` and `artifacts/bff_sorry_inventory_2026_05_02.json`.
- The former `sorry` holes were converted into explicit named frontier assumptions; that conversion is bookkeeping/quarantine, not proof discharge.
- `axiom` is a trusted assumption, not a proof.
- `admit` is a proof hole when present in the active formal inventory.
- An explicit frontier assumption is also not a proof.
- Any result depending on high-girth, non-coboundary, quotient-independence, project axioms, admits, quarantined frontier assumptions, or explicitly named missing lemmas is Conditional.

Current status:
- Strongest verified theorem: none asserted at repository level
- Weakest missing theorem: replace each load-bearing axiom/admit/sorry with a proof or quarantine it as an explicit assumption
- Conditional inventory: `docs/status/CONDITIONAL_FRONTIER_STATUS_2026_04_27.md`
- Sorry quarantine registry: `docs/status/BFF_SORRY_QUARANTINE_2026_05_02.md`
- Terminal frontier registry: `docs/status/BFF_TERMINAL_FRONTIER_REGISTRY_2026_05_02.md`

## External status

This repository is governed by [`docs/status/EXTERNAL_STATUS_LOCK.md`](docs/status/EXTERNAL_STATUS_LOCK.md). Build success, CI success, dashboards, ledgers, axioms, admits, quarantined frontier assumptions, `sorry`, or placeholder witnesses do not constitute theorem-level closure.

## Cross-domain information recovery — 2026-11-27 UTC

Three scoped mathematical connections: 52 distinct audited Lean theorem declarations across two standalone certificates (41 + 11; the original 33 are counted once).

- [Chronos–Biological Friction, BFF #116](https://github.com/inaciovasquez2020/biological-friction-framework/blob/799b41b4692c71589587cba037f26f0ad4bff7fb/proofs/hidden-dissipation/receipt/HiddenDissipation.lean): merged; 33/33 audited declarations, fresh Linux build PASS. In finite cyclic Markov models with the stated stationary and path-gauge observations, different entropy production can be indistinguishable; sharp absolute-error minimax equals half maximal dissipation in the bounded current family. `BFF.HiddenDissipation.ring_observation_minimax`.
- [Biology–Cosmology, BFF #117](https://github.com/inaciovasquez2020/biological-friction-framework/blob/c5c8b2f24a0d4de57c764c161ab29c3689bec62f/proofs/hidden-dissipation/receipt/HiddenDissipation.lean): merged; eight additional declarations, cumulative 41/41 audit and fresh Linux build PASS. One diagonal generator-square observable with the specified stationary observations identifies squared current and entropy production; the restricted cosmological mode coefficient is invertible for known positive radius and nonzero mode. `BFF.HiddenDissipation.entropy_identified_by_curvature`, `BFF.HiddenDissipation.mode_identifiable`.
- [Cosmology–Chronos, #1392 pinned PR revision](https://github.com/inaciovasquez2020/chronos-urf-rr/blob/2ed7df1497824343fce34924501d42a220c3006f/research/certificates/cosmology_causal_projection/receipt/CausalProjection.lean): Mac 11/11 and dedicated Linux Lean CI PASS; wider integration CI pending at this dated checkpoint. Identical projected coordinates can conceal different causal comparability; strip-area algebra and optimal pointwise decision loss are verified. `Chronos.CosmologyBridge.no_perfect_visible_decoder`, `Chronos.CosmologyBridge.strip_optimal_decoder`.

Only permitted standard Lean axioms were audited. These are mathematical comparisons, not physical equivalence or software dependencies. Full semigroup derivative, covariant action/Fourier derivation, continuum measure formalization, empirical validation, physical 5D detection and independent novelty remain OPEN. No repository-wide status promotion.
