# Melanoma eIF4A translation / adaptive-mutability residual — 2026-08-31

## Status

`CONDITIONAL / LITERATURE-BOUNDED MODEL`

This document records a bounded structural result for a melanoma drug-tolerant-persister / acquired-resistance graph. It is not clinical guidance, a treatment recommendation, or evidence of a cure.

## Question

Can the selective mRNA-translation program seen in BRAF-V600 melanoma persisters be absorbed into already retained controls such as MAPK, PI3K/AKT, mTOR-ATF4-MTHFD2, KDM5B reseeding, or state-specific metabolic controls?

## Result

`RESULT := NO — THE eIF4A-DEPENDENT TRANSLATION PROGRAM REMAINS A DISTINCT CROSS-STATE RESIDUAL`

Two melanoma results, separated by several years, establish two different functions for the same broad translation-control layer.

### 1. Persister-survival function

Shen et al. (Nature Communications, 2019) showed that BRAFi/MEKi-tolerant BRAF-V600 melanoma persisters undergo a reversible selective mRNA-translation program despite globally reduced protein synthesis.

A subset of mRNAs becomes more efficiently translated and is enriched for:

```text
mTORC2 / AKT-related regulators
epigenetic regulators
other persister-survival outputs
```

The program is associated with increased 5-prime-UTR m6A enrichment on highly translated mRNAs.

eIF4A1 disruption reduced the selectively translated proteins, reduced phospho-AKT and histone-acetylation outputs, and prevented persister emergence / persister-derived colony formation in the tested melanoma cell systems.

Importantly, direct eIF4A-directed interference was more effective in the reported screen than individually targeting downstream mTORC2, CREBBP, or KDM6-associated outputs.

Therefore:

```text
DO_NOT_INFER :=
control(PI3K/AKT) OR control(one epigenetic output)
=> control(selective translation program)
```

### 2. Adaptive-mutability function

Fabbri et al. (EMBO Molecular Medicine, 2026) added a second, mechanistically distinct role.

Under BRAFi/MEKi pressure, drug-tolerant BRAF-V600 melanoma cells increase error-prone non-homologous end joining (NHEJ)-associated mutability through selective translation of 53BP1.

The reported route is:

```text
BRAFi/MEKi pressure
  -> drug-tolerant melanoma state
  -> eIF4A-dependent 5-prime-UTR translation of 53BP1
  -> increased error-prone NHEJ / adaptive mutability
  -> higher probability of resistance-conferring genetic evolution
  -> acquired resistance
```

Specific interference with 53BP1 5-prime-UTR-driven translation reduced NHEJ and mutability.

Two eIF4A-directed small molecules delayed acquisition of BRAFi/MEKi resistance in BRAF-V600 melanoma cell lines and xenograft models by reducing drug-tolerant-cell mutability.

This adds an in-vivo-validated evolutionary function that is not equivalent to any single downstream survival pathway.

## Absorption test against the current graph

### MAPK control

The 2019 persister study reports that eIF4A interference affected persister outputs without suppressing MAPK activity.

```text
DO_NOT_INFER := C_MAPK => C_TRANSLATION_PERSIST
```

### PI3K/AKT control

Selective translation regulates multiple outputs at once, including RICTOR/mTORC2-AKT and epigenetic programs. The 2026 53BP1/NHEJ mutability branch is not a PI3K/AKT survival branch.

```text
DO_NOT_INFER := C_PI3K_AKT => control(53BP1 adaptive mutability)
```

### mTOR-ATF4-MTHFD2 control

The retained ISR/MTHFD2 object concerns stress-response / one-carbon / DNA-repair support under RAF/MEK pressure. The new 53BP1 route concerns translation-controlled error-prone NHEJ and adaptive mutation generation.

```text
DO_NOT_COLLAPSE := R_TRANSLATION_MUTABILITY into C_ISR_MTHFD2
```

### KDM5B reseeding control

KDM5B captures reversible slow-cycling reservoir dynamics. eIF4A-dependent selective translation is a mechanistically distinct post-transcriptional program and additionally alters mutation supply.

```text
DO_NOT_COLLAPSE := R_TRANSLATION_MUTABILITY into C_KDM5B_RESEED
```

### State-specific metabolic controls

Pigmented/OXPHOS, CD36+ SMC/peroxisome-UGCG, CSE/H2S-persulfide, and GPX4/FSP1 boundaries concern distinct metabolic / ferroptosis functions. None establishes control of selective mRNA translation or 53BP1-dependent adaptive mutability.

## Functional repair

The graph should retain a functional requirement rather than a named compound:

```text
C_TRANSLATION_PERSIST :=
prevent therapy-induced selective translation from simultaneously:

1. sustaining drug-tolerant persister survival programs, and
2. increasing adaptive mutability that seeds genetically acquired resistance
```

An experimentally supported implementation class is interference with the eIF4A/eIF4F translation-initiation layer, but no particular inhibitor is promoted as a universal or clinically appropriate control.

## Stronger structural consequence

This route changes the graph from a pure survival-hitting problem into a survival-plus-evolution problem.

A cell can be temporarily contained by pathway control yet still remain dangerous if it increases the rate at which new genetically resistant descendants are generated.

Therefore define:

```text
SURVIVAL_CONTROL := prevent residual-cell persistence
EVOLUTION_CONTROL := prevent residual cells from increasing resistance-generating mutability

ADEQUATE_PERSISTER_CONTROL :=
SURVIVAL_CONTROL AND EVOLUTION_CONTROL
```

The eIF4A/53BP1 result provides direct melanoma evidence that these two requirements are not interchangeable.

## Scope boundary

The strongest direct evidence is centered on BRAF-V600 melanoma under BRAFi/MEKi pressure.

```text
DO_NOT_INFER :=
this exact eIF4A / 53BP1 adaptive-mutability dependency is universal across
NRAS, NF1, KIT, triple-wild-type, immunotherapy-only, or every metastatic niche
```

The older eIF4F literature does show broader links to resistance and translation control, including BRAF- and NRAS-mutant melanoma, but this does not prove universal persister-state closure.

## Current missing object

```text
MISSING_OBJECT :=
a matched lineage-and-state certificate showing whether C_TRANSLATION_PERSIST:

1. suppresses selective persister translation,
2. suppresses 53BP1/NHEJ adaptive mutability,
3. prevents resistant-clone emergence in vivo,
4. remains effective across the major retained melanoma MRD states,
5. does not simply redistribute surviving cells into another uncovered state,
6. preserves the immune / metastatic / ferroptosis boundaries already retained.
```

## Boundary

```text
BOUNDARY :=
eIF4A-dependent selective translation is supported as a distinct melanoma
persister-survival and adaptive-mutability vulnerability, but universal
cross-state / cross-genotype closure is not proved
```

## Evidence anchors

- Shen et al., Nature Communications (2019), `An epitranscriptomic mechanism underlies selective mRNA translation remodelling in melanoma persister cells`.
  - https://www.nature.com/articles/s41467-019-13360-6
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC6915789/
  - https://pubmed.ncbi.nlm.nih.gov/31844050/
- Fabbri et al., EMBO Molecular Medicine (2026), `Selective mRNA translation determines adaptative mutability of melanoma cells to anti-BRAF/MEK combination therapy`.
  - https://pubmed.ncbi.nlm.nih.gov/42477455/
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC13470486/
  - https://doi.org/10.1038/s44321-026-00479-5
- Boussemart et al., Nature (2014), `eIF4F is a nexus of resistance to anti-BRAF and anti-MEK cancer therapies`.
  - https://pubmed.ncbi.nlm.nih.gov/25079330/
  - https://www.nature.com/articles/nature13572

## Next bounded action

```text
NEXT_ACTIONS :=
1. Add C_TRANSLATION_PERSIST as a distinct functional control requirement.
2. Recompute the residual graph treating both survival and adaptive mutability
   as quantities that must remain controlled.
3. Search for the first surviving evolutionary escape route that can generate
   acquired resistance despite the current survival-control set.
4. Prefer a route with direct melanoma functional and in-vivo evidence.
```
