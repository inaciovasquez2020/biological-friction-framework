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

That encoding is now too coarse for current evidence.

## Result

`RESULT := RAC1 ROUTES ARE FUNCTIONALLY COUPLED IN TESTED MAPKi-RESISTANT MELANOMA MODELS`

A 2025 Oncogene study reports that Rac1-driven melanoma resistance is pleiotropic and includes:

```text
activated RAC1
  |- reduced dependence on BRAF/MEK
  |- alternative MAPK signaling through JNK and p38
  |- partial YAP/TAZ reliance
  |- a FAK dependency in undifferentiated melanoma cells
```

The study tested multiple Rac1-driven BRAF-inhibitor-resistant A375 and 451Lu models, including RAC1 P29S and Rac1-GEF/VAV1-driven states. Combined RAF/MEK-clamp plus FAK inhibition controlled growth across the tested 2D and 3D cell models. A proof-of-concept A375 RAC1 P29S xenograft experiment also showed substantial tumor-growth control and prolonged survival with combined RAF/MEK and FAK pathway inhibition.

The authors explicitly state that the mechanistic basis of the FAK dependency remains unresolved and that additional in-vivo single-agent/pharmacodynamic experiments are needed.

## Structural correction

Do not model R7a, R7b and R7c as fully independent escape paths for Rac1-driven MAPKi resistance.

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

In the tested Rac1-driven models, evidence supports the possibility that the pair:

```text
C2 + C3
```

can suppress growth despite JNK/p38 activation and partial YAP/TAZ reliance.

However, the evidence is not sufficient to promote that observation to a universal closure theorem across all RAC1-mutant, RAC1-GEF-driven, differentiated, undifferentiated, metastatic, and treatment-evolved melanoma states.

Therefore:

```text
DO_NOT_INFER :=
R7a and R7b are universally closed merely because FAK + MAPK controls are present
```

## Conditional route reduction

```text
Conditional

IF RAC1_FAK_DEPENDENCY_GENERALIZES
across the modeled Rac1-driven resistant states,
THEN
  R7a/R7b/R7c may be represented by the coupled R7_COUPLED object
  and treated as functionally intercepted by C2 + C3.
ELSE
  an alternative JNK/p38 or YAP/TAZ escape may remain reachable.
```

## Next clean survivor under that condition

If the above coupling generalizes, the next clean retained escape not already represented by C2, C3, or the new PI3K/AKT constraint is:

```text
R8 := SOX10-low persister -> TAZ -> TEAD
```

This route is independently supported by 2025 melanoma minimal-residual-disease work showing that SOX10 loss up-regulates a TAZ-dependent TEAD program; active TAZ is sufficient to confer tolerance to BRAF/MEK pathway inhibition, and TEAD inhibition delays acquired resistance from MRD in melanoma models.

R8 is not assumed to be equivalent to RAC1-driven YAP/TAZ resistance. It is retained as a distinct SOX10-low persister-state route.

## Weakest missing object

```text
MISSING_OBJECT :=
evidence that the FAK dependency observed in tested Rac1-driven MAPKi-resistant
melanoma models generalizes across the Rac1 states represented by R7_COUPLED,
with sufficient in-vivo/context coverage to justify treating C2 + C3 as a
functional cover of that resistance family.
```

## Boundary

```text
BOUNDARY :=
¬ universal closure(RAC1-driven JNK/p38 + YAP/TAZ resistance by FAK + MAPK control)
```

and, conditionally:

```text
IF RAC1_FAK_DEPENDENCY_GENERALIZES
THEN FIRST_CLEAN_SURVIVOR := SOX10-low -> TAZ -> TEAD
```

## Evidence anchors

- A critical role of FAK signaling in Rac1-driven melanoma cell resistance to MAPK pathway inhibition, Oncogene (2025):
  - https://www.nature.com/articles/s41388-025-03603-w
  - https://pubmed.ncbi.nlm.nih.gov/41109929/
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
1. Treat R7 as a coupled conditional object rather than three independent paths.
2. Keep C2 + C3 coverage of R7 conditional on FAK-dependency generalization.
3. Advance to R8 SOX10-low -> TAZ -> TEAD as the next clean survivor under that condition.
4. Test whether any existing control already functionally intercepts R8.
5. Do not interpret preclinical pathway coverage as a treatment recommendation.
```
