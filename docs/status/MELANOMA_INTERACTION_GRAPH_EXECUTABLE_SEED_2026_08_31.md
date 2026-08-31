# Melanoma interaction graph executable certificate — 2026-08-31

## Status

`EXECUTABLE / CONDITIONAL CERTIFICATE`

This document records the repository-native executable seed and bounded expansions of the interaction-aware melanoma resistance invariant. It is a model-verification artifact, not clinical guidance, a treatment recommendation, or evidence of a cure.

## Result

`RESULT := INTERACTION-AWARE CERTIFICATE NOW INCLUDES SIGNED, NICHE, RESEEDING, AND CLASSIC MRD-STATE BOUNDARIES`

The repository contains:

```text
infra/certificates/melanoma_interaction_graph.json
infra/ci/verify_melanoma_interaction_graph.py
tests/test_melanoma_interaction_graph.py
```

The certificate remains deliberately incomplete and represents only evidence-bounded objects already retained in repository status documents.

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

The signed ApoE boundary is executable.

```text
melanoma_context -> apoe_ferroptosis_resistance
melanoma_context -> apoe_immune_escape
```

A candidate reduction probe is represented as:

```text
PROBE_APOE_REDUCTION
  blocks apoe_ferroptosis_resistance
  blocks apoe_immune_escape
  induces apoe_dissemination_release
```

The probe is intentionally not promoted to a globally admissible treatment control.

With the probe active:

```text
apoe_dissemination_release -> reachable
```

The tests remove the probe and verify the opposite signed pattern:

```text
apoe_ferroptosis_resistance -> reachable
apoe_immune_escape          -> reachable
apoe_dissemination_release  -> not induced
```

Evidence lock:

```text
docs/status/MELANOMA_APOE_SIGNED_BOUNDARY_2026_08_31.md
```

## Expansion 2: GPX4/FSP1 niche-switch boundary

The ferroptosis layer is represented by:

```text
metastatic_context -> ln_fsp1_escape
metastatic_context -> hemato_gpx4_escape
metastatic_context -> ferroptosis_handoff_gap
```

The active endpoint control:

```text
C_FERROPTOSIS_NICHE_ENDPOINTS
```

blocks the encoded FSP1-dominant lymph-node endpoint and GPX4-dominant hematogenous endpoint, but deliberately does not block:

```text
ferroptosis_handoff_gap
```

because the repository evidence does not establish continuous functional coverage through reoxygenation and niche transition.

Evidence lock:

```text
docs/status/MELANOMA_FERROPTOSIS_NICHE_SWITCH_2026_08_31.md
```

## Expansion 3: KDM5B reseeding dynamics

The KDM5B boundary is dynamic:

```text
therapy_pressure
  -> kdm5b_persister_reservoir
  -> kdm5b_reseed
```

The active functional control:

```text
C_KDM5B_RESEED
```

blocks both encoded states in the current abstraction. Tests remove that control and require both states to become reachable again.

Evidence lock:

```text
docs/status/MELANOMA_KDM5B_RESEEDING_BOUNDARY_2026_08_31.md
```

## Expansion 4: classic MRD phenotype cluster

Three additional Rambow-associated phenotype objects are now represented alongside the already encoded NCSC route.

### SOX10-low / invasive MRD

```text
therapy_pressure -> sox10_low_mrd
therapy_pressure -> sox10_dual_vulnerability_gap
```

The active abstract state control:

```text
C_SOX10_LOW
```

blocks `sox10_low_mrd`.

It does not block:

```text
sox10_dual_vulnerability_gap
```

because TEAD-directed and cIAP-directed vulnerabilities have matched-model support but no head-to-head certificate establishing redundancy, complementarity, or absence of a common survivor.

Evidence lock:

```text
docs/status/MELANOMA_SOX10_LOW_DUAL_VULNERABILITY_2026_08_31.md
```

### CD36+ starved-like melanoma cell state

```text
therapy_pressure -> smc_cd36_persister
therapy_pressure -> smc_redistribution_gap
```

The active abstract state control:

```text
C_SMC_METABOLIC
```

blocks the encoded CD36+ SMC persister state.

It does not block:

```text
smc_redistribution_gap
```

because the retained evidence does not establish that selective SMC control prevents transition or redistribution into NCSC, invasive/SOX10-low, or pigmented residual states.

Evidence lock:

```text
docs/status/MELANOMA_CD36_SMC_PEROXISOME_UGCG_RESIDUAL_2026_08_31.md
```

### Pigmented / MITF-high MRD

```text
therapy_pressure -> pigmented_mitf_persister
therapy_pressure -> pigmented_redistribution_gap
```

The active abstract state control:

```text
C_PIGMENTED
```

blocks the encoded MITF-high/pigmented persister state.

It does not block:

```text
pigmented_redistribution_gap
```

because the retained evidence does not establish transition-safe elimination without increasing another MRD phenotype.

Evidence lock:

```text
docs/status/MELANOMA_PIGMENTED_MITF_OXPHOS_RESIDUAL_2026_08_31.md
```

## Four-state accounting status

At the current abstraction level, the four classic MRD phenotype families are represented as:

```text
SOX10-low / invasive -> C_SOX10_LOW + unresolved dual-vulnerability gap
CD36+ SMC            -> C_SMC_METABOLIC + unresolved redistribution gap
NCSC                  -> I_FAK_NCSC_CONTROL + C_MAPK_DYNAMIC
pigmented / MITF-high -> C_PIGMENTED + unresolved redistribution gap
```

This is state accounting, not closure.

```text
DO_NOT_INFER :=
four phenotype families represented => melanoma MRD closed
```

## Current machine-checked result

With the current active controls/probe, fixed-point reachability is expected to leave exactly:

```text
apoe_dissemination_release
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

and `declared_unresolved` must equal that complete set.

## Fail-closed behavior

The tests now verify:

```text
1. the current conditional certificate passes;
2. claim := closed fails while any encoded malignant/gap state is reachable;
3. unresolved declarations must exactly match fixed-point reachability;
4. ApoE reduction remains signed rather than monotone;
5. ferroptosis endpoint control does not close the handoff gap;
6. KDM5B reseeding reappears when its functional control is removed;
7. SOX10-low state reappears when C_SOX10_LOW is removed;
8. SOX10 dual-vulnerability uncertainty remains even with abstract state control;
9. CD36+ SMC state reappears when C_SMC_METABOLIC is removed;
10. the SMC redistribution gap remains with abstract state control active;
11. pigmented/MITF-high state reappears when C_PIGMENTED is removed;
12. the pigmented redistribution gap remains with abstract state control active.
```

## Evidence-file locking

Every encoded edge and control carries repository evidence paths. The verifier rejects missing or empty evidence references.

This validates graph/evidence consistency, not clinical efficacy or the truth of external biology beyond the retained evidence audit.

## What this does not prove

```text
DO_NOT_INFER :=
this certificate represents every melanoma state or resistance route

DO_NOT_INFER :=
the listed reachable states/gaps are the only real biological survivors

DO_NOT_INFER :=
active controls or probes form a treatment regimen

DO_NOT_INFER :=
abstract state control proves a safe or universal molecular implementation

DO_NOT_INFER :=
conditional machine verification implies clinical efficacy or cure
```

## Remaining executable boundary

```text
MISSING_OBJECT :=
continue expanding only already-retained melanoma objects while preserving
signed, dynamic, state-transition, interaction-aware, evidence-linked semantics.
```

Next bounded candidates:

```text
adenosine immune escape
CSE/H2S-persulfide cross-state persistence
eIF4A translation/adaptive-mutability control
```

No new biological target should be introduced merely to enlarge the graph.

## Boundary

```text
BOUNDARY :=
the executable graph now represents the classic four-state MRD accounting plus
ApoE, Polκ, GPX4/FSP1, and KDM5B interaction boundaries, but transition-safe and
implementation-safe closure remains unproved and the certificate is conditional
```

## Next bounded action

```text
NEXT_ACTIONS :=
1. Compile this MRD-cluster expansion on canonical PR CI.
2. Repair only the first authoritative failure if one appears.
3. Merge only if the fail-closed tests pass.
4. Then add the next cross-state immune/metabolic cluster.
```
