# Melanoma RAC1–FAK Coupled-Route Correction — 2026-08-31

## Status

`CONDITIONAL / LITERATURE-BOUNDED MODEL`

This document updates the melanoma resistance graph after adding an abstract PI3K/AKT survival-control constraint. It is not clinical guidance, a treatment recommendation, or evidence of a cure.

## Prior route encoding

The retained graph previously represented activated RAC1 as three approximately independent resistance routes:

```text
R7a RAC1 -> JNK/p38
R7b RAC1 -> YAP/TAZ -> TEAD
R7c RAC1 -> FAK
```

That encoding is too coarse for current evidence.

## Result

`RESULT := RAC1 ROUTES ARE FUNCTIONALLY COUPLED ACROSS MULTIPLE TESTED MAPKi-RESISTANT MELANOMA CONTEXTS`

A 2025 Oncogene study reports that Rac1-driven melanoma resistance is pleiotropic and includes:

```text
activated RAC1
  |- reduced dependence on BRAF/MEK
  |- alternative MAPK signaling through JNK and p38
  |- partial YAP/TAZ reliance
  |- a FAK dependency in undifferentiated melanoma cells
```

The evidence is broader than a single A375 implementation. The study tested:

```text
A375 RAC1 P29S
A375 VAV1/Rac1-GEF-driven resistance
A375 independently derived VRPP1/VRPP2/VRPP3 resistant populations
451Lu RAC1 P29S
2D growth assays
3D collagen growth
an A375 RAC1 P29S xenograft proof-of-concept
```

Across the tested Rac1-driven settings, combined RAF/MEK-clamp plus FAK inhibition controlled growth despite the pleiotropic resistance program. In the xenograft experiment, the combination produced substantial tumor-growth control and prolonged survival compared with the tested comparators.

The authors nevertheless state that the mechanistic basis of the FAK dependency remains unresolved. The study does not establish that every RAC1-mutant, RAC1-GEF-driven, differentiated, metastatic, brain-metastatic, or treatment-evolved melanoma state shares the same dependency.

## Structural correction

Do not model R7a, R7b and R7c as fully independent escape paths for the tested Rac1-driven MAPKi-resistant settings.

Replace them with a coupled phenotype object:

```text
R7_COUPLED :=
RAC1_active
  -> {
       JNK/p38 activation,
       partial YAP/TAZ dependence,
       residual ERK dependence,
       FAK-dependent cellular phenotype
     }
```

This means a simple edge-only hitting-set can over-count the number of independent controls required for the RAC1 family.

## Interaction with current controls

The current abstract control graph already includes:

```text
C2 := FAK/NCSC control
C3 := MAPK-reactivation control
```

For the experimentally tested RAC1-driven resistance family, evidence supports the composite abstraction:

```text
C_RAC1_FAK_MAPK_OBSERVED := C2 + C3
```

as a functional cover of the observed coupled phenotype.

The executable graph is therefore justified in blocking:

```text
rac1_coupled_observed
```

while separately retaining a scope state for untested generality.

## What is now retired

```text
RETIRE :=
"RAC1 + FAK evidence is only a single-cell-line / 2D observation"
```

The 2025 study includes multiple Rac1 implementations, two melanoma line backgrounds, 3D culture, and proof-of-concept xenograft evidence.

Also retain:

```text
RETIRE :=
R7a RAC1 -> JNK/p38
R7b RAC1 -> YAP/TAZ -> TEAD
R7c RAC1 -> FAK

as three universally independent mandatory control paths
```

## Remaining generality boundary

The unresolved object is now narrower:

```text
rac1_fak_mapk_generality_gap :=
possible RAC1-driven melanoma context outside the tested A375/451Lu,
undifferentiated/MAPKi-resistant, 2D/3D/xenograft evidence surface in which
FAK + MAPK control does not cover the coupled resistance phenotype
```

The following implication is not proved:

```text
forall melanoma contexts S,
  RAC1-driven resistance(S)
    -> coverable_by(FAK + dynamic MAPK control, S)
```

This includes uncertainty across:

```text
different lineage/differentiation states
additional RAC1-mutant or RAC1-GEF mechanisms
non-BRAF-V600 driver contexts
metastatic niches including brain
heavily treatment-evolved states
immune-competent contexts
```

Therefore:

```text
DO_NOT_INFER :=
observed multi-model / xenograft coverage => universal RAC1-family closure
```

## Relationship to SOX10-low state

The independently retained SOX10-low / TAZ-TEAD state remains distinct from RAC1-driven partial YAP/TAZ reliance.

```text
DO_NOT_COLLAPSE :=
SOX10-low TAZ/TEAD MRD into R7_COUPLED
```

The RAC1 route compression occurs because the tested RAC1 phenotype exhibits a FAK-dependent coupled program, not because every YAP/TAZ-dependent melanoma state is FAK-covered.

## Weakest missing object

```text
MISSING_OBJECT :=
a cross-context RAC1 melanoma certificate testing the FAK + MAPK composite in
RAC1-driven resistance outside the current A375/451Lu evidence surface, with
at least one materially different phenotype, genotype, or metastatic niche and
with functional growth/relapse readouts sufficient to determine whether the
observed FAK dependency generalizes.
```

A particularly informative next test would use a distinct RAC1-driven melanoma context rather than another derivative of the same A375 resistance system.

## Boundary

```text
BOUNDARY :=
FAK + MAPK control covers the observed multi-model RAC1 resistance phenotype,
including 3D and proof-of-concept xenograft evidence, but universal
cross-context RAC1-family closure remains unproved
```

## Evidence anchors

- A critical role of FAK signaling in Rac1-driven melanoma cell resistance to MAPK pathway inhibition, Oncogene (2025):
  - https://www.nature.com/articles/s41388-025-03603-w
  - https://pubmed.ncbi.nlm.nih.gov/41109929/
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC12602353/
- RAC1 P29S resistance to RAF inhibition and MAPK-targeted therapy:
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC4167745/
  - https://pubmed.ncbi.nlm.nih.gov/25056119/
- RAC1 P29S mesenchymal/SRF-MRTF resistance program:
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC6617390/
- SOX10-low / TAZ-TEAD minimal residual disease route, Nature Communications (2025):
  - https://www.nature.com/articles/s41467-025-64682-7
  - https://pubmed.ncbi.nlm.nih.gov/41193428/

## Next bounded action

```text
NEXT_ACTIONS :=
1. Keep rac1_coupled_observed blocked by C_RAC1_FAK_MAPK_OBSERVED.
2. Keep rac1_fak_mapk_generality_gap reachable.
3. Search for a distinct RAC1-driven melanoma genotype/phenotype/niche testing
   combined FAK + MAPK control.
4. Retire the generality gap only after materially independent context coverage.
```
