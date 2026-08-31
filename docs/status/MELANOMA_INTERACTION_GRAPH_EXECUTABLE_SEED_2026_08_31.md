# Melanoma interaction graph executable certificate — 2026-08-31

## Status

`EXECUTABLE / CONDITIONAL CERTIFICATE`

This document records the repository-native executable seed and first bounded expansion of the interaction-aware melanoma resistance invariant. It is a model-verification artifact, not clinical guidance, a treatment recommendation, or evidence of a cure.

## Result

`RESULT := INTERACTION-AWARE GRAPH CERTIFICATE EXPANDED TO THREE ADDITIONAL RETAINED BOUNDARIES`

The repository contains:

```text
infra/certificates/melanoma_interaction_graph.json
infra/ci/verify_melanoma_interaction_graph.py
tests/test_melanoma_interaction_graph.py
```

The certificate remains deliberately incomplete. It represents only evidence-bounded objects already retained in repository status documents.

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

The signed ApoE boundary is now executable.

Baseline ApoE-high context contributes two malignant outcomes in the encoded slice:

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

The probe is intentionally named `PROBE`, not a globally admissible treatment control. It machine-encodes the repository boundary that reducing extracellular ApoE can improve ferroptosis/immune directions while removing ApoE-mediated suppression of invasion/endothelial recruitment.

With the probe active, the first two ApoE outcomes are not reachable but:

```text
apoe_dissemination_release
```

is reachable.

The tests also remove the probe and verify the sign reversal:

```text
apoe_ferroptosis_resistance -> reachable
apoe_immune_escape          -> reachable
apoe_dissemination_release  -> not induced
```

Therefore the machine surface does not permit ApoE reduction to be credited as a monotone closure node.

Evidence lock:

```text
docs/status/MELANOMA_APOE_SIGNED_BOUNDARY_2026_08_31.md
```

## Expansion 2: GPX4/FSP1 niche-switch boundary

The ferroptosis layer is encoded as three residual objects:

```text
metastatic_context -> ln_fsp1_escape
metastatic_context -> hemato_gpx4_escape
metastatic_context -> ferroptosis_handoff_gap
```

The active endpoint control:

```text
C_FERROPTOSIS_NICHE_ENDPOINTS
```

blocks the encoded hypoxic-LN FSP1 endpoint and hematogenous GPX4 endpoint.

It does not block:

```text
ferroptosis_handoff_gap
```

because the repository evidence does not establish the continuous functional invariant:

```text
forall t in T_transition,
  D_GPX4(t) OR D_FSP1(t)
```

The tests explicitly verify that endpoint coverage does not silently upgrade into transition coverage.

Evidence lock:

```text
docs/status/MELANOMA_FERROPTOSIS_NICHE_SWITCH_2026_08_31.md
```

## Expansion 3: KDM5B reseeding dynamics

The KDM5B boundary is encoded dynamically rather than as one static expression node:

```text
therapy_pressure
  -> kdm5b_persister_reservoir
  -> kdm5b_reseed
```

The active functional control:

```text
C_KDM5B_RESEED
```

blocks both reservoir formation/survival and the represented reseeding transition in this abstraction.

The test suite then removes `C_KDM5B_RESEED` and requires both malignant states to become reachable again:

```text
kdm5b_persister_reservoir
kdm5b_reseed
```

This prevents the graph from collapsing KDM5B dynamics into a pigmented/MITF label or treating KDM5B expression itself as monotone.

Evidence lock:

```text
docs/status/MELANOMA_KDM5B_RESEEDING_BOUNDARY_2026_08_31.md
```

## Current machine-checked result

With the expanded active control/probe set, fixed-point reachability is expected to leave exactly:

```text
apoe_dissemination_release
ferroptosis_handoff_gap
polk_stress_tolerance
```

reachable among encoded malignant states.

Therefore the certificate remains:

```text
claim := conditional

declared_unresolved := [
  apoe_dissemination_release,
  ferroptosis_handoff_gap,
  polk_stress_tolerance
]
```

The verifier requires `declared_unresolved` to equal the complete reachable malignant set.

## Fail-closed behavior

The test suite now checks:

```text
1. the expanded conditional certificate passes;
2. claim := closed fails while any encoded malignant state remains reachable;
3. omitting reachable malignant states from declared_unresolved fails;
4. removing the ApoE reduction probe exposes ApoE ferroptosis + immune escape;
5. ApoE reduction exposes dissemination release rather than monotone closure;
6. ferroptosis endpoint control leaves the handoff gap reachable;
7. active KDM5B reseed control blocks its two encoded states;
8. removing KDM5B control restores both reservoir and reseed reachability.
```

## Evidence-file locking

Every baseline or induced edge and every control carries one or more repository evidence paths. The verifier rejects empty or missing evidence paths.

This verifies graph/evidence consistency, not the scientific truth of a paper or clinical efficacy.

## What this does not prove

```text
DO_NOT_INFER :=
this certificate represents every melanoma state or resistance route

DO_NOT_INFER :=
the three reachable states are the only biological survivors

DO_NOT_INFER :=
active controls or probes form a treatment regimen

DO_NOT_INFER :=
PROBE_APOE_REDUCTION is an admissible global melanoma control

DO_NOT_INFER :=
conditional machine verification implies clinical efficacy or cure
```

## Remaining executable boundary

```text
MISSING_OBJECT :=
continue expanding the certificate to already-retained melanoma objects while
preserving signed, dynamic, interaction-aware, evidence-linked semantics.
```

The next bounded expansion candidates are:

```text
SOX10-low / TAZ-TEAD + cIAP state control
CD36+ SMC peroxisome/UGCG state
pigmented MITF-high/OXPHOS state
adenosine immune escape
CSE/H2S-persulfide cross-state persistence
eIF4A translation/adaptive-mutability control
```

No new biological target should be introduced merely to enlarge the graph.

## Boundary

```text
BOUNDARY :=
the executable graph now tests Polκ antagonism, ApoE signed tradeoffs,
GPX4/FSP1 transition failure, and KDM5B reseeding dynamics, but full retained-
graph encoding remains incomplete and the certificate remains conditional
```

## Next bounded action

```text
NEXT_ACTIONS :=
1. Compile the expansion on canonical PR CI.
2. Repair only the first authoritative failure if one appears.
3. Merge only if the fail-closed tests pass.
4. Then add the next retained MRD-state cluster as one bounded expansion.
```
