# Conditional Frontier Status — 2026-04-27

Status: Conditional Framework / Frontier Claims

This repository contains conditional formalization work.
Any result depending on high-girth, non-coboundary, quotient-independence, project axioms, admits, or sorries is not an unconditional theorem.
The repository should explicitly separate verified local lemmas from frontier assumptions.

Axiom count: 17
Admit count: 1
Sorry count: 7

## Axiom locations

- `archive/foreign-scope/reintroduced/lean/Cyclone/HighGirthOverlapFamily.lean:22` — `axiom high_girth_high_overlap_family`
- `archive/foreign-scope/reintroduced/lean/Cyclone/HighGirthOverlapFamily.lean:31` — `axiom overlap_rank_linear_formula`
- `archive/foreign-scope/reintroduced/lean/Cyclone/CFILiftSeparation.lean:32` — `axiom cfi_lift_separation`
- `archive/foreign-scope/reintroduced/lean/Cyclone/CycleRigiditySpine.lean:39` — `axiom overlap_quotient_rigidity`
- `archive/foreign-scope/reintroduced/lean/Cyclone/CycleRigiditySpine.lean:47` — `axiom obstruction_non_factorization`
- `archive/foreign-scope/reintroduced/lean/Cyclone/CycleRigiditySpine.lean:82` — `axiom lift_monotone_rank`
- `archive/foreign-scope/reintroduced/lean/Cyclone/CycleRigiditySpine.lean:87` — `axiom lift_linear_growth`
- `archive/foreign-scope/reintroduced/lean/Cyclone/NonCoboundarySignature.lean:37` — `axiom non_coboundary_signature_exists`
- `archive/foreign-scope/reintroduced/lean/Cyclone/NonCoboundarySignature.lean:44` — `axiom cycle_trap_signature`
- `archive/foreign-scope/reintroduced/lean/Cyclone/CFILocalIsomorphism.lean:39` — `axiom local_lift_isomorphism`
- `archive/foreign-scope/reintroduced/lean/Cyclone/CFILocalIsomorphism.lean:46` — `axiom cfi_separation_constructive`
- `archive/foreign-scope/reintroduced/lean/Cyclone/LocalGlobalSeparation.lean:30` — `axiom ball_tree_of_girth_gt_twoR`
- `archive/foreign-scope/reintroduced/lean/Cyclone/LocalGlobalSeparation.lean:36` — `axiom local_cycle_space_trivial_of_girth_gt_twoR`
- `archive/foreign-scope/reintroduced/lean/Cyclone/LocalGlobalSeparation.lean:42` — `axiom local_global_separation`
- `archive/foreign-scope/reintroduced/lean/Cyclone/QuotientIndependence.lean:28` — `axiom quotient_independence_core`
- `archive/foreign-scope/reintroduced/lean/Cyclone/TreePotential.lean:22` — `axiom unique_path (G : Graph) (u v : G.V) : ∃! p : Path G u v, True`
- `urf-core/URF_Core/URF_Axioms_Core.lean:13` — `axiom spectral_gap_core :`

## Admit locations

- `archive/foreign-scope/reintroduced/lean/Cyclone/CFILocalIsomorphism.lean:238` — `admit`

## Sorry locations

- `archive/foreign-scope/reintroduced/lean/Cyclone/CFILiftSeparation.lean:55` — `sorry`
- `archive/foreign-scope/reintroduced/lean/Cyclone/CFILiftSeparation.lean:64` — `sorry`
- `archive/foreign-scope/reintroduced/lean/Cyclone/NonCoboundarySignature.lean:62` — `sorry`
- `archive/foreign-scope/reintroduced/lean/Cyclone/CFILocalIsomorphism.lean:248` — `sorry`
- `archive/foreign-scope/reintroduced/lean/Cyclone/CFILocalIsomorphism.lean:256` — `sorry`
- `archive/foreign-scope/reintroduced/lean/Cyclone/CFILocalIsomorphism.lean:263` — `sorry`
- `archive/foreign-scope/reintroduced/lean/Cyclone/QuotientIndependence.lean:7` — `- Remove all false “no-sorry” claims.`

## Boundary rule

If `axiom + admit + sorry > 0`, no unconditional theorem-closure claim is allowed.
