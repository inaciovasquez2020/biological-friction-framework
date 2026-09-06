# Melanoma miR-18a matched-state overlap audit — 2026-09-06

## Status

`CONDITIONAL / PUBLIC-DATA-BOUNDED NEGATIVE OVERLAP AUDIT`

This note sharpens the existing `mir18a_pleiotropic_cross_resistance_gap`. It does not add a treatment, control, or cure claim.

## Question

Do the public miR-18a datasets directly demonstrate that the AJUBA/Hippo/YAP MAPKi-resistance program and the THBS1-CD47 T-cell-resistance program occupy the same melanoma cell state, such that the existing pleiotropic gap can be reduced further?

## Public source surface

```text
GSE318353 := single-cell RNA-seq of WT, miR-18a-KO, A375-VR, and A375-TR melanoma cells
GSE318354 := bulk RNA-seq under VEM and CD8+ T-cell challenge contexts
Wang et al. Advanced Science (2026) := functional, single-cell, in-vivo, and clinical analysis
```

## Result

```text
RESULT := MATCHED-CLONE DUAL RESISTANCE SUPPORTED;
          MATCHED-SINGLE-CELL DUAL-PROGRAM STATE NOT CERTIFIED
```

The study generated independent miR-18a-knockout melanoma monoclonal lines and showed that miR-18a depletion confers both VEM/BRAF-pathway resistance and resistance to CD8+ T-cell-mediated killing in separate functional challenge assays. Re-expression of miR-18a restored sensitivity in both contexts.

Therefore the following is supported:

```text
miR-18a-deficient melanoma clone
  -> can exhibit MAPKi resistance under MAPK-pathway challenge
  -> can exhibit T-cell-killing resistance under immune challenge
```

This materially strengthens the common-upstream pleiotropy claim.

## Single-cell limit

`GSE318353` jointly profiles control, miR-18a-KO, A375-VR, and A375-TR cells and resolves 13 transcriptional melanoma clusters. The paper reports that Hippo, ECM-receptor, PI3K-AKT, TGF-beta and related pathway enrichments occur in specific clusters across the perturbed conditions.

However, the public analysis does not establish a cell-resolved certificate of the form:

```text
same resistant melanoma cell/state
  AND AJUBA/YAP-high MAPKi-resistance program
  AND THBS1-CD47-high immune-resistance program
```

The VR and TR models are independently selected resistance conditions, and the bulk dataset likewise measures MAPK-drug and T-cell challenge contexts separately. These designs support shared upstream miR-18a deficiency and heterogeneous downstream resistance programs, but not simultaneous co-residence of both complete downstream programs in one transcriptionally defined resistant state.

## Author-stated causal boundary

The study explicitly treats the downstream resistance mechanisms as distinct and states that the independence, causal relationship, and mutual dependence of Hippo and TGF-beta-associated signaling in miR-18a-induced resistance require additional experiments.

Therefore:

```text
DO_NOT_INFER :=
AJUBA/YAP activation <=> THBS1-CD47 activation
```

and:

```text
DO_NOT_INFER :=
one downstream arm is a sufficient proxy for the other
```

## Supplementary-table and deposited-data audit

The public article exposes a 24-table supporting workbook and identifies the RNA-seq/target-prediction tables used to construct the treatment-context signatures. The rendered paper assigns bulk RNA-seq measurements to Tables S6-S7, target predictions to Tables S8-S9, and context-specific target sets to Tables S10-S13. Those tables support treatment-context signature construction; they are not reported as a cluster-by-gene certificate demonstrating a single scRNA-seq state jointly positive for both complete downstream resistance arms.

The GEO record for `GSE318353` deposits condition-separated 10x count matrices for:

```text
WT
miR-18a KO
A375-TR
A375-VR
```

but does not deposit a canonical processed cluster-annotation table that maps each cell to the 13 published states together with validated AJUBA/YAP and THBS1-CD47 program labels. The published single-cell result is therefore pathway enrichment in specific clusters, not a deposited matched-state dual-program certificate.

A raw-count reanalysis could test transcriptional co-expression or module-score overlap, but it would still not by itself establish YAP activation because the load-bearing YAP evidence in the study includes phosphorylation and nuclear-localization measurements. Likewise, THBS1-CD47 immune escape is functionally supported by T-cell killing, CD47 blockade, and synapse-related experiments rather than RNA abundance alone.

Therefore the supplementary and deposited-data surface does not justify promotion of:

```text
same_cell_transcriptional_overlap
=> same_cell_functional_dual_resistance
```

or:

```text
YAP1 mRNA abundance
=> AJUBA/YAP pathway activation
```

## Structural consequence

No executable graph change is justified.

The existing state remains the correct fail-closed object:

```text
mir18a_pleiotropic_cross_resistance_gap
```

but its boundary is now narrower:

```text
SUPPORTED :=
common miR-18a-deficient clones can functionally resist both targeted-therapy
and CD8+ T-cell challenges in separate assays

UNPROVED :=
the same transcriptionally defined resistant state simultaneously carries
both complete downstream programs, or that the two downstream arms are
causally coupled / mutually dependent
```

## Weakest missing object

```text
MISSING_OBJECT :=
a matched cell-state certificate from the same resistant population showing:

1. cell-resolved AJUBA/YAP/Hippo activation,
2. cell-resolved THBS1-CD47/TGF-beta-associated immune-evasion activity,
3. co-occurrence of both signatures in the same melanoma cells or rigorously
   mapped state rather than across separately selected VR and TR populations,
4. functional confirmation that the co-positive state resists both MAPKi and
   CD8+ T-cell killing,
5. perturbation evidence resolving whether the two downstream arms are
   independent, coupled, or hierarchically related.
```

## Boundary

```text
BOUNDARY :=
matched-clone pleiotropic resistance is supported, but matched-single-cell
co-residence and causal coupling of the AJUBA/YAP and THBS1-CD47 resistance
programs remain unproved
```

## Evidence anchors

- Wang et al., Advanced Science (2026), `Genome-Wide CRISPR Screen Identifies a microRNA Orchestrating Pleiotropic Resistance to Targeted Therapy and T Cell Immunity in Melanoma`.
  - https://pubmed.ncbi.nlm.nih.gov/42189126/
  - https://doi.org/10.1002/advs.202515158
- GEO single-cell dataset:
  - https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE318353
- GEO bulk RNA-seq dataset:
  - https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE318354

## Next bounded action

```text
NEXT_ACTIONS :=
1. Preserve the existing graph state unchanged.
2. Do not infer functional YAP activation from scRNA abundance alone.
3. Resume this gap only if a matched cell-state assay or deposited processed annotation directly links both functional arms in the same resistant population.
```
