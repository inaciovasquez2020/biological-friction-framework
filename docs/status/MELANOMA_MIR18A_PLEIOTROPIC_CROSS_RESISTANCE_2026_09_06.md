# Melanoma miR-18a pleiotropic cross-resistance boundary — 2026-09-06

## Status

`CONDITIONAL / LITERATURE- AND PUBLIC-DATA-BOUNDED MODEL`

This document records a bounded structural correction from a 2026 melanoma cross-resistance study and its public GEO datasets. It is not clinical guidance, a treatment recommendation, or evidence of a cure.

## Question

Do the current melanoma graph objects already absorb the experimentally linked targeted-therapy and CD8+ T-cell resistance associated with miR-18a loss, or is a distinct pleiotropic cross-resistance scope state required?

## Public source surface

The study deposited three linked datasets under BioProject `PRJNA1223135`:

```text
GSE318353 := single-cell RNA-seq
GSE318354 := bulk RNA-seq
GSE318501 := genome-wide miRNA CRISPR screen
```

The GEO summaries state that miR-18a knockout causes resistance to BRAF inhibition and combined BRAF/MEK inhibition through increased YAP/Hippo-pathway signaling, while also increasing THBS1-CD47-associated T-cell tolerance.

## Result

`RESULT := ONE UPSTREAM miR-18a-DEFICIENT PROGRAM COUPLES TWO DISTINCT RESISTANCE ARMS NOT REPRESENTED BY THE CURRENT GRAPH`

The 2026 study identifies miR-18a deficiency as an upstream regulator of pleiotropic melanoma resistance and separates the downstream mechanisms as:

```text
miR-18a deficiency
  |- AJUBA-regulated Hippo/YAP derepression during MAPK inhibition
  |    -> BRAFi / BRAFi+MEKi resistance
  |
  `- enhanced THBS1-CD47 interaction
       -> impaired tumor-cell/CD8+ T-cell immunological synapse
       -> T-cell killing resistance
```

The paper therefore supports a common-upstream cross-resistance object, not a claim that MAPK inhibition itself directly causes THBS1-CD47 immune escape.

```text
DO_NOT_INFER :=
MAPK inhibition -> THBS1-CD47 immune escape
```

## Why this is not the existing dynamic-MAPK state

The current graph has a dynamic MAPK control that covers the retained MAPK-pulse and FAK-induced ERK-sensitive escape edges.

The miR-18a result contains a second, mechanistically separate CD8+ T-cell-resistance arm through THBS1-CD47. Blocking a MAPK-reactivation edge is therefore not evidence that the immune arm is eliminated.

```text
DO_NOT_INFER :=
C_MAPK_DYNAMIC
=> elimination of miR-18a-linked T-cell resistance
```

## Why this is not the existing adenosine immune state

The current immune graph includes extracellular adenosine immune escape and a ligand-sink scope gap. The miR-18a study instead identifies a THBS1-CD47-mediated impairment of the tumor-cell/CD8+ T-cell immunological synapse.

These are distinct molecular surfaces.

```text
DO_NOT_COLLAPSE :=
THBS1-CD47 T-cell resistance
into adenosine_immune_escape
```

## Why this is not the existing APOE immune state

The APOE state in the repository is tied to an APOE-centered signed tradeoff involving ferroptosis, immune escape and dissemination. The miR-18a study does not establish that its THBS1-CD47 immune mechanism is mediated by APOE or covered by the APOE reduction probe.

```text
DO_NOT_COLLAPSE :=
miR-18a pleiotropic cross-resistance
into apoe_immune_escape
```

## Experimental depth

The study combines:

```text
genome-wide miRNA CRISPR screening
A375 melanoma resistance models
bulk transcriptomics
single-cell transcriptomics
CD8+ T-cell co-culture assays
in-vivo experiments
longitudinal clinical datasets
```

The public GEO designs include wild-type, miR-18a-knockout, vemurafenib-resistant and CD8+ T-cell-resistant melanoma conditions. `GSE318354` includes biological replicates under vemurafenib treatment and CD8+ T-cell co-culture.

The study additionally integrated paired patient transcriptomic data from:

```text
61 BRAFi/MEKi-treated melanoma pairs
59 anti-PD-1/CTLA-4-treated melanoma pairs
```

and reported associations between inferred miR-18a activity changes and therapeutic outcomes. These clinical associations strengthen relevance but do not prove that one intervention closes both resistance arms.

## Functional rescue boundary

The study reports functional perturbations supporting the two arms, including restoration of miR-18a activity in resistant models and CD47-directed testing in the T-cell-resistance setting.

This does not establish a universally safe or sufficient combined control, and the two downstream branches remain mechanistically distinct.

```text
DO_NOT_PROMOTE :=
miR-18a restoration or CD47-directed perturbation
as a universal melanoma control
```

## Structural consequence

The smallest defensible graph correction is one unresolved pleiotropic state:

```text
mir18a_pleiotropic_cross_resistance_gap :=
a melanoma resistance program in which reduced miR-18a activity can support
both MAPKi resistance through AJUBA/Hippo/YAP signaling and CD8+ T-cell
resistance through THBS1-CD47, without evidence that the currently active
MAPK, adenosine, APOE or other retained controls jointly eliminate both arms
```

This is a coupling/scope state, not a new treatment target.

## Missing object

```text
MISSING_OBJECT :=
a matched functional certificate demonstrating that a defined control set
eliminates both miR-18a-linked resistance arms in the same melanoma context:

1. MAPKi-resistant residual burden/outgrowth,
2. CD8+ T-cell killing resistance,
3. direct AJUBA/YAP pathway readout,
4. direct THBS1-CD47 / immunological-synapse readout,
5. durable outgrowth or relapse endpoint,
6. no redistribution into another retained melanoma escape state.
```

## Boundary

```text
BOUNDARY :=
miR-18a deficiency is experimentally supported as a common upstream driver of
mechanistically distinct targeted-therapy and CD8+ T-cell resistance programs,
but universal dual-arm closure and a direct MAPKi-to-immune-escape transition
are not established
```

## Evidence anchors

- Wang et al., Advanced Science (2026), `Genome-Wide CRISPR Screen Identifies a microRNA Orchestrating Pleiotropic Resistance to Targeted Therapy and T Cell Immunity in Melanoma`.
  - https://pubmed.ncbi.nlm.nih.gov/42189126/
  - https://doi.org/10.1002/advs.202515158
- GEO single-cell dataset:
  - https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE318353
- GEO bulk RNA-seq dataset:
  - https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE318354
- GEO CRISPR-screen dataset:
  - https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE318501
- BioProject:
  - https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1223135

## Next bounded action

```text
NEXT_ACTIONS :=
1. Add mir18a_pleiotropic_cross_resistance_gap as one reachable malignant state.
2. Keep it unblocked by all current controls.
3. Synchronize the exact unresolved-state test inventory.
4. Re-run the verifier immediately.
5. Do not encode MAPKi -> immune escape as a causal transition.
```
