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

## RNA-only state maps are not an admissible closure proxy

The 2026 adaptive-mutability study directly separates transcript abundance from the functional translation output that matters for this branch.

In A375 melanoma cells surviving BRAFi/MEKi pressure, 53BP1 protein increased reversibly, whereas `TP53BP1` mRNA did not show a significant treatment-level increase; the paper notes only a less-than-twofold increase in two of six replicates. The study therefore identifies translational regulation, not a simple transcript-abundance increase, as the operative mechanism. The same paper reuses the earlier polysome-profiling evidence to identify 53BP1 as a selectively translated NHEJ component.

Therefore an RNA-only single-cell atlas can classify melanoma cell states, but it cannot by itself certify or refute the eIF4A/53BP1 dependency.

```text
INADMISSIBLE_PROXY :=
state-resolved EIF4A1 or TP53BP1 RNA abundance alone
=> state-resolved C_TRANSLATION_PERSIST dependency

DO_NOT_INFER :=
flat / low EIF4A1 RNA across MRD states
=> absence of eIF4A dependence

DO_NOT_INFER :=
flat / low TP53BP1 RNA across MRD states
=> absence of 53BP1 translational upregulation or NHEJ mutability
```

This makes a purely transcriptomic reuse of the MeRLin endpoint object insufficient for retiring `eif4a_cross_state_gap`. The correct state-resolved surface must measure translation/protein output or functional dependency.

A useful admissible hierarchy is:

```text
STATE_LABEL_ONLY              := insufficient
RNA_ABUNDANCE_ONLY            := insufficient
STATE + TRANSLATION/PROTEIN    := mechanistically informative
STATE + eIF4A PERTURBATION     := functional dependency surface
STATE + eIF4A PERTURBATION
      + relapse/outgrowth      := closure-relevant surface
```

This is a methodological boundary, not evidence that the eIF4A dependency is uniform across all states.

## Current missing object

The 2026 adaptive-mutability study already supplies an in-vivo acquired-resistance endpoint in the tested BRAF-V600 context. In A375 xenografts, adding eFT226 to BRAFi/MEKi prolonged control: median progression under BRAFi/MEKi alone was 49 days, whereas only 20% of the combination group had relapsed by day 70. The same intervention reduced 53BP1 translation, NHEJ activity, and drug-tolerant-cell mutability.

```text
ESTABLISHED :=
in the tested BRAF-V600 A375 residual-disease model,
eIF4A inhibition + BRAFi/MEKi suppresses the 53BP1/NHEJ adaptive-mutability
program and delays acquired resistance in vivo
```

Therefore a generic request to prove `prevents resistant-clone emergence in vivo` is no longer the weakest missing object. What remains unresolved is whether this function applies across the retained melanoma residual-state graph rather than only the tested BRAF-V600 drug-tolerant population.

```text
MISSING_OBJECT :=
a matched lineage-and-state certificate showing whether C_TRANSLATION_PERSIST:

1. suppresses selective persister translation and 53BP1/NHEJ adaptive mutability
   within each major retained melanoma MRD state,
2. preserves the demonstrated in-vivo resistance-delay effect when those states
   coexist in the same residual population,
3. does not simply redistribute surviving cells into another uncovered state,
4. preserves the immune / metastatic / ferroptosis boundaries already retained,
5. generalizes beyond the tested BRAF-V600 context before any universal claim.

MINIMUM_STATE_RESOLVED_READOUTS :=
state identity
AND eIF4A perturbation
AND translation/protein output (for example 53BP1 protein or polysome/ribosome occupancy)
AND functional NHEJ/mutability or persister-survival output
AND relapse/outgrowth in the matched residual population
```

An RNA-only state-expression ranking does not satisfy this object.

## Boundary

```text
BOUNDARY :=
eIF4A-dependent selective translation is supported as a distinct melanoma
persister-survival and adaptive-mutability vulnerability, but RNA-only state
maps cannot test this post-transcriptional dependency and universal cross-state /
cross-genotype closure remains unproved
```

## Evidence anchors

- Shen et al., Nature Communications (2019), `An epitranscriptomic mechanism underlies selective mRNA translation remodelling in melanoma persister cells`.
  - https://www.nature.com/articles/s41467-019-13360-6
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC6915789/
  - https://pubmed.ncbi.nlm.nih.gov/31844050/
  - GEO superseries: GSE137726
- Fabbri et al., EMBO Molecular Medicine (2026), `Selective mRNA translation determines adaptative mutability of melanoma cells to anti-BRAF/MEK combination therapy`.
  - https://pubmed.ncbi.nlm.nih.gov/42477455/
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC13470486/
  - https://doi.org/10.1038/s44321-026-00479-5
  - ProteomeXchange/PRIDE: PXD068007
- Boussemart et al., Nature (2014), `eIF4F is a nexus of resistance to anti-BRAF and anti-MEK cancer therapies`.
  - https://pubmed.ncbi.nlm.nih.gov/25079330/
  - https://www.nature.com/articles/nature13572

## Next bounded action

```text
NEXT_ACTIONS :=
1. Keep eif4a_cross_state_gap reachable.
2. Do not use scRNA transcript abundance as a surrogate for the eIF4A/53BP1
   post-transcriptional dependency.
3. Search for state-resolved melanoma translatome/proteome or eIF4A-perturbation
   data that can be aligned to major persister phenotypes.
4. Retire the gap only after a functional state-resolved dependency / survivor
   certificate, not an RNA-expression map alone.
```
