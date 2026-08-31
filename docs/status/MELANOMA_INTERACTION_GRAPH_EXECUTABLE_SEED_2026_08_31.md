# Melanoma interaction graph executable certificate — 2026-08-31

## Status

`EXECUTABLE / CONDITIONAL CERTIFICATE`

This document records the repository-native executable seed and bounded expansions of the interaction-aware melanoma resistance invariant. It is a model-verification artifact, not clinical guidance, a treatment recommendation, or evidence of a cure.

## Result

`RESULT := INTERACTION-AWARE CERTIFICATE NOW INCLUDES SIGNED, NICHE, RESEEDING, CLASSIC MRD, IMMUNE, REDOX, AND TRANSLATION BOUNDARIES`

The repository contains:

```text
infra/certificates/melanoma_interaction_graph.json
infra/ci/verify_melanoma_interaction_graph.py
tests/test_melanoma_interaction_graph.py
```

The certificate remains deliberately incomplete and includes only evidence-bounded objects already retained in repository status documents.

## Original executable slice

The initial certificate encoded:

```text
therapy pressure -> RTK / PI3K survival
therapy pressure -> mTOR / ATF4 / MTHFD2 persistence
therapy pressure -> NCSC nongenetic escape
therapy pressure -> dynamic ERK-pulse escape
```

with active controls:

```text
I_PI3K_SURVIVAL_CONTROL
I_MTOR_ISR_CONTROL
I_FAK_NCSC_CONTROL
C_MAPK_DYNAMIC
```

and induced interactions:

```text
PI3K suppression -> nuclear Polκ stress tolerance
mTOR suppression -> nuclear Polκ stress tolerance
FAK/NCSC control -> observed ERK-sensitive genetic escape
```

The first executable result left `polk_stress_tolerance` reachable.

## Expansion 1: ApoE signed tradeoff

```text
melanoma_context -> apoe_ferroptosis_resistance
melanoma_context -> apoe_immune_escape
```

The candidate probe:

```text
PROBE_APOE_REDUCTION
```

blocks those two baseline outcomes but induces:

```text
apoe_dissemination_release
```

The tests remove the probe and require the ferroptosis/immune outcomes to reappear while dissemination release is no longer induced.

Evidence:

```text
docs/status/MELANOMA_APOE_SIGNED_BOUNDARY_2026_08_31.md
```

## Expansion 2: GPX4/FSP1 niche-switch boundary

```text
metastatic_context -> ln_fsp1_escape
metastatic_context -> hemato_gpx4_escape
metastatic_context -> ferroptosis_handoff_gap
```

`C_FERROPTOSIS_NICHE_ENDPOINTS` blocks the two endpoint escape states but not the unresolved functional handoff gap.

Evidence:

```text
docs/status/MELANOMA_FERROPTOSIS_NICHE_SWITCH_2026_08_31.md
```

## Expansion 3: KDM5B reseeding dynamics

```text
therapy_pressure
  -> kdm5b_persister_reservoir
  -> kdm5b_reseed
```

`C_KDM5B_RESEED` blocks both encoded states. Removing that control in the test suite restores both reservoir and reseed reachability.

Evidence:

```text
docs/status/MELANOMA_KDM5B_RESEEDING_BOUNDARY_2026_08_31.md
```

## Expansion 4: classic MRD phenotype cluster

The remaining classic MRD phenotypes are represented alongside the already encoded NCSC route.

```text
SOX10-low / invasive
  -> C_SOX10_LOW
  -> sox10_dual_vulnerability_gap remains unresolved

CD36+ SMC
  -> C_SMC_METABOLIC
  -> smc_redistribution_gap remains unresolved

NCSC
  -> I_FAK_NCSC_CONTROL + C_MAPK_DYNAMIC

pigmented / MITF-high
  -> C_PIGMENTED
  -> pigmented_redistribution_gap remains unresolved
```

The three phenotype tests remove each abstract control and require its phenotype state to reappear while the corresponding implementation-safety gap remains explicit.

Evidence:

```text
docs/status/MELANOMA_SOX10_LOW_DUAL_VULNERABILITY_2026_08_31.md
docs/status/MELANOMA_CD36_SMC_PEROXISOME_UGCG_RESIDUAL_2026_08_31.md
docs/status/MELANOMA_PIGMENTED_MITF_OXPHOS_RESIDUAL_2026_08_31.md
```

This is state accounting, not MRD closure.

## Expansion 5: cross-state immune, redox, and translation cluster

### Extracellular adenosine immune escape

The encoded direct escape is:

```text
melanoma_context -> adenosine_immune_escape
```

The active functional control:

```text
C_ADENOSINE_LIGAND
```

blocks that direct encoded immune-escape state.

The separate state:

```text
adenosine_ligand_sink_gap
```

remains reachable because the repository does not contain a melanoma-specific matched certificate establishing one spatially admissible source-independent ligand sink that lowers intratumoral adenosine, restores functional antitumor immune activity, covers relevant production routes, and avoids a new dissemination/host-safety failure.

Evidence:

```text
docs/status/MELANOMA_ADENOSINE_LIGAND_SINK_2026_08_31.md
```

### CSE/H2S-persulfide cross-state persistence

The encoded survival state is:

```text
therapy_pressure -> cse_persister_survival
```

The active functional control:

```text
C_CSE_REDOX
```

blocks that direct encoded persister state.

The separate state:

```text
cse_state_mapping_gap
```

remains reachable because the retained evidence does not establish phenotype-wide dependency mapping, cross-genotype generality, or absence of state redistribution after CSE/H2S-persulfide control.

Evidence:

```text
docs/status/MELANOMA_CSE_PERSULFIDE_CROSS_STATE_RESIDUAL_2026_08_31.md
```

### eIF4A selective translation and adaptive mutability

The executable graph now distinguishes two direct functions:

```text
therapy_pressure -> eif4a_persister_survival
therapy_pressure -> eif4a_adaptive_mutability
```

The active functional control:

```text
C_TRANSLATION_PERSIST
```

blocks both encoded functions.

The separate state:

```text
eif4a_cross_state_gap
```

remains reachable because the retained evidence does not prove matched cross-state/cross-genotype suppression of both persister survival and resistance-generating mutability without redistribution into another uncovered state.

Evidence:

```text
docs/status/MELANOMA_EIF4A_TRANSLATION_ADAPTIVE_MUTABILITY_RESIDUAL_2026_08_31.md
```

## Current machine-checked expectation

With all currently encoded abstract controls/probes active, fixed-point reachability is expected to leave exactly:

```text
adenosine_ligand_sink_gap
apoe_dissemination_release
cse_state_mapping_gap
eif4a_cross_state_gap
ferroptosis_handoff_gap
pigmented_redistribution_gap
polk_stress_tolerance
smc_redistribution_gap
sox10_dual_vulnerability_gap
```

reachable among encoded malignant/gap states.

Therefore:

```text
claim := conditional
```

and `declared_unresolved` must equal that exact set.

## Fail-closed behavior

The tests now verify that:

```text
1. the full current conditional certificate passes;
2. a closed claim fails while any encoded malignant/gap state is reachable;
3. unresolved declarations must equal fixed-point reachability exactly;
4. ApoE reduction remains signed rather than monotone;
5. ferroptosis endpoint coverage does not imply handoff coverage;
6. KDM5B reseeding returns if C_KDM5B_RESEED is removed;
7. SOX10-low, SMC, and pigmented phenotype states return if their controls are removed;
8. the corresponding MRD implementation-safety gaps remain explicit;
9. adenosine immune escape returns if C_ADENOSINE_LIGAND is removed;
10. the melanoma ligand-sink gap remains even with abstract adenosine control active;
11. CSE persister survival returns if C_CSE_REDOX is removed;
12. the CSE state-mapping/generalization gap remains explicit;
13. eIF4A persister survival and adaptive mutability both return if C_TRANSLATION_PERSIST is removed;
14. the eIF4A cross-state/generalization gap remains explicit.
```

## Evidence-file locking

Every encoded edge and control carries one or more repository evidence paths. The verifier rejects empty or missing evidence references.

This checks graph/evidence consistency, not clinical efficacy and not the independent truth of external scientific claims beyond the retained evidence audit.

## What this does not prove

```text
DO_NOT_INFER :=
this certificate represents every melanoma resistance mechanism

DO_NOT_INFER :=
all direct encoded states are safely controllable in patients

DO_NOT_INFER :=
abstract functional controls identify unique drugs or schedules

DO_NOT_INFER :=
the listed unresolved states are the only biological survivors

DO_NOT_INFER :=
active controls/probes form a treatment regimen

DO_NOT_INFER :=
conditional machine verification implies a cancer cure
```

## Remaining executable boundary

The certificate now covers the major retained melanoma objects developed in this sequence, but it is still a partial research model.

```text
MISSING_OBJECT :=
identify which retained status objects are still absent from the executable
certificate, add them one bounded cluster at a time, and preserve fail-closed
fixed-point semantics for every new interaction or implementation gap.
```

## Boundary

```text
BOUNDARY :=
the executable melanoma graph now represents phenotype-state, niche-transition,
immune-environment, stress-metabolic, translation/evolution, and control-induced
escape objects, but nine encoded malignant/gap states remain reachable and
full retained-graph or clinical closure is not established
```

## Next bounded action

```text
NEXT_ACTIONS :=
1. Compile this cross-state expansion on canonical PR CI.
2. Repair only the first authoritative failure if one appears.
3. Merge only if all fail-closed tests pass.
4. Audit the retained status directory against certificate evidence references
   to find the first major already-retained melanoma object still unencoded.
```
