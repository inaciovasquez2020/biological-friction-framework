# Melanoma interaction graph executable certificate — 2026-08-31

## Status

`EXECUTABLE / CONDITIONAL CERTIFICATE`

This document records the repository-native executable interaction-aware melanoma resistance certificate. It is a model-verification artifact, not clinical guidance, a treatment recommendation, or evidence of a cure.

## Executable surface

```text
infra/certificates/melanoma_interaction_graph.json
infra/ci/verify_melanoma_interaction_graph.py
tests/test_melanoma_interaction_graph.py
```

The verifier checks evidence paths, computes fixed-point reachability after baseline and control-induced edges, and fails closed:

```text
claim := conditional
  => declared_unresolved must equal every reachable malignant/gap state

claim := closed
  => no malignant/gap state may remain reachable
```

## Encoded control families

The current certificate contains already-retained repository evidence for:

```text
RTK / PI3K survival
mTOR / ATF4 / MTHFD2 persistence
NCSC -> FAK / MAPK evolutionary redirection
dynamic ERK-pulse escape
ApoE signed tradeoffs
GPX4 / FSP1 metastatic-niche switching
KDM5B persister reseeding
SOX10-low MRD
CD36+ SMC MRD
pigmented / MITF-high MRD
extracellular adenosine immune escape
CSE / H2S-persulfide persistence
eIF4A persister survival + adaptive mutability
RAC1 coupled FAK/MAPK resistance
```

No new biological target is introduced by the executable representation; the graph only machine-encodes boundaries already retained in `docs/status`.

## Control-induced and signed interactions

### PI3K/mTOR -> Polκ antagonism

```text
I_PI3K_SURVIVAL_CONTROL -> polk_stress_tolerance
I_MTOR_ISR_CONTROL      -> polk_stress_tolerance
```

`polk_stress_tolerance` remains unresolved. The certificate does not treat Polκ as a proved melanoma mutator route.

Evidence:

```text
docs/status/MELANOMA_MTOR_POLK_ANTAGONISTIC_COUPLING_2026_08_31.md
```

### ApoE signed probe

```text
PROBE_APOE_REDUCTION
  blocks apoe_ferroptosis_resistance
  blocks apoe_immune_escape
  induces apoe_dissemination_release
```

The probe is not promoted to a globally admissible melanoma control. Tests remove it and require the opposite signed outcomes to reappear.

Evidence:

```text
docs/status/MELANOMA_APOE_SIGNED_BOUNDARY_2026_08_31.md
```

## Dynamic/niche boundaries

### GPX4/FSP1

```text
C_FERROPTOSIS_NICHE_ENDPOINTS
  blocks ln_fsp1_escape
  blocks hemato_gpx4_escape
  does not block ferroptosis_handoff_gap
```

The handoff gap remains because continuous functional coverage during reoxygenation/LN-to-blood transition is unproved.

Evidence:

```text
docs/status/MELANOMA_FERROPTOSIS_NICHE_SWITCH_2026_08_31.md
```

### KDM5B

```text
therapy_pressure
  -> kdm5b_persister_reservoir
  -> kdm5b_reseed
```

`C_KDM5B_RESEED` blocks both encoded states. Removing it in tests restores both states.

Evidence:

```text
docs/status/MELANOMA_KDM5B_RESEEDING_BOUNDARY_2026_08_31.md
```

## Classic MRD phenotype accounting

```text
SOX10-low / invasive
  -> C_SOX10_LOW
  -> sox10_dual_vulnerability_gap remains

CD36+ SMC
  -> C_SMC_METABOLIC
  -> smc_redistribution_gap remains

NCSC
  -> I_FAK_NCSC_CONTROL + C_MAPK_DYNAMIC

pigmented / MITF-high
  -> C_PIGMENTED
  -> pigmented_redistribution_gap remains
```

The abstract controls block the direct encoded phenotype states; the uncertainty/redistribution states remain reachable. Removing each abstract state control in tests restores its direct phenotype state.

Evidence:

```text
docs/status/MELANOMA_SOX10_LOW_DUAL_VULNERABILITY_2026_08_31.md
docs/status/MELANOMA_CD36_SMC_PEROXISOME_UGCG_RESIDUAL_2026_08_31.md
docs/status/MELANOMA_NCSC_FAK_MAPK_ROUTE_COMPRESSION_2026_08_31.md
docs/status/MELANOMA_PIGMENTED_MITF_OXPHOS_RESIDUAL_2026_08_31.md
```

This is four-state accounting, not MRD closure.

## Cross-state immune/metabolic/evolutionary programs

### Adenosine

```text
C_ADENOSINE_LIGAND
  blocks adenosine_immune_escape
  does not block adenosine_ligand_sink_gap
```

The gap represents the missing melanoma-specific matched source-independent ligand-sink certificate.

Evidence:

```text
docs/status/MELANOMA_ADENOSINE_LIGAND_SINK_2026_08_31.md
```

### CSE/H2S-persulfide

```text
C_CSE_REDOX
  blocks cse_persister_survival
  does not block cse_state_mapping_gap
```

The gap preserves state-mapping, genotype-generalization, and redistribution uncertainty.

Evidence:

```text
docs/status/MELANOMA_CSE_PERSULFIDE_CROSS_STATE_RESIDUAL_2026_08_31.md
```

### eIF4A selective translation

```text
C_TRANSLATION_PERSIST
  blocks eif4a_persister_survival
  blocks eif4a_adaptive_mutability
  does not block eif4a_cross_state_gap
```

The gap preserves missing matched cross-state/cross-genotype coverage.

Evidence:

```text
docs/status/MELANOMA_EIF4A_TRANSLATION_ADAPTIVE_MUTABILITY_RESIDUAL_2026_08_31.md
```

## RAC1 coupled-route expansion

The retained RAC1 result is not encoded as three independent JNK/p38, YAP/TAZ, and FAK routes. It is encoded as the coupled observed phenotype:

```text
therapy_pressure -> rac1_coupled_observed
```

with a composite functional control:

```text
C_RAC1_FAK_MAPK_OBSERVED
```

that blocks the tested coupled phenotype. This control represents the evidence-supported combination of FAK-pathway and MAPK-pathway control in the tested RAC1-driven resistant melanoma models; it does not assert that FAK or MAPK control alone is sufficient.

A separate baseline state remains reachable:

```text
rac1_fak_mapk_generality_gap
```

because the retained evidence does not establish universal closure across all RAC1-mutant, RAC1-GEF-driven, differentiated, undifferentiated, metastatic, and treatment-evolved melanoma contexts.

Tests remove `C_RAC1_FAK_MAPK_OBSERVED` and require `rac1_coupled_observed` to reappear while `rac1_fak_mapk_generality_gap` remains reachable in both cases.

Evidence:

```text
docs/status/MELANOMA_RAC1_FAK_COUPLED_ROUTE_2026_08_31.md
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
rac1_fak_mapk_generality_gap
smc_redistribution_gap
sox10_dual_vulnerability_gap
```

Therefore:

```text
claim := conditional
```

and `declared_unresolved` must equal that exact ten-state set.

## Fail-closed behavior

The test suite verifies that:

```text
1. the current conditional certificate passes;
2. claim := closed fails while any encoded malignant/gap state is reachable;
3. declared_unresolved must exactly match fixed-point reachability;
4. ApoE remains signed rather than monotone;
5. GPX4/FSP1 endpoint coverage does not imply handoff coverage;
6. KDM5B reseeding returns if its functional control is removed;
7. classic MRD phenotype states return if their controls are removed;
8. MRD implementation/redistribution gaps remain explicit;
9. adenosine, CSE, and eIF4A direct states return when their controls are removed;
10. their scope/generalization gaps remain explicit;
11. RAC1 observed coupled escape returns when its composite control is removed;
12. RAC1 FAK/MAPK generality uncertainty remains reachable even with observed-route control active.
```

## Evidence-file locking

Every encoded edge/control carries repository evidence paths. The verifier rejects missing or empty evidence references.

This checks graph/evidence consistency. It does not independently prove the external scientific literature or clinical efficacy.

## What this does not prove

```text
DO_NOT_INFER := this certificate represents every melanoma resistance mechanism
DO_NOT_INFER := abstract controls identify unique drugs, doses, or schedules
DO_NOT_INFER := active controls/probes form a treatment regimen
DO_NOT_INFER := the ten encoded unresolved states are the only biological survivors
DO_NOT_INFER := conditional machine verification implies clinical efficacy or cure
```

## Boundary

```text
BOUNDARY :=
the executable melanoma graph now includes all major independent melanoma status
objects currently retained in this 2026-08-31 sequence, including RAC1 coupled
resistance, but ten encoded malignant/gap states remain reachable and the
certificate remains conditional
```

Supporting/refinement documents such as the ApoE 1D7 bridge and the earlier CD73 source-layer note are not duplicated as independent graph routes when their operative boundary is already represented by the signed ApoE and ligand-level adenosine objects.

## Next bounded action

```text
NEXT_ACTIONS :=
1. Compile the RAC1 expansion on canonical PR CI.
2. Repair only the first authoritative failure if one appears.
3. Merge only if the fail-closed tests pass.
4. After merge, audit whether any retained independent melanoma status object is
   still absent; if none is found, stop expanding breadth and attack the first
   unresolved executable state instead.
```
