# Melanoma CSE/H2S-persulfide cross-state residual — 2026-08-31

## Status

`CONDITIONAL / LITERATURE-BOUNDED MODEL`

This document records a bounded structural result for a melanoma drug-tolerant-persister / minimal-residual-disease escape graph. It is not clinical guidance, a treatment recommendation, or evidence of a cure.

## Question

After representing the four classic Rambow MRD phenotypes at the abstraction level, is there a newer survival program that cuts across phenotype identity and therefore remains outside a purely state-based hitting set?

## Result

`RESULT := AN IMMEDIATE CSE/H2S-PERSULFIDE STRESS-SURVIVAL PROGRAM REMAINS A CROSS-STATE RESIDUAL`

Cell Metabolism (2025) reported that BRAF-V600E inhibition triggers rapid metabolic reprogramming in melanoma persister cells, including an immediate increase in cystathionine-gamma-lyase (CSE) activity/expression.

The supported route is:

```text
BRAF-V600E inhibition
  -> oxidative / cystine-rich stress state
  -> increased CSE-dependent cysteine/cystine catabolism
  -> H2S + persulfide production
  -> protein-thiol protection + mitochondrial energy support
  -> drug-tolerant persister survival
  -> proliferative relapse
```

CSE inhibition combined with BRAF-targeted therapy reduced proliferative relapse in culture models and increased progression-free survival in xenografted mice. CSE induction was also reported in patient samples during BRAF-V600E-targeted therapy.

## Why this is not another Rambow state

The CSE result is described as a rapid stress-response/metabolic program in drug-tolerant persisters rather than as one of the four transcriptional MRD phenotypes.

Therefore a graph that contains only:

```text
invasive / SOX10-low
SMC / CD36+
NCSC
pigmented / MITF-high
```

can still miss a cross-cutting survival mechanism that may be shared by more than one phenotype.

```text
DO_NOT_INFER :=
coverage(four MRD phenotype labels) => coverage(all persister survival programs)
```

## Relationship to existing metabolic controls

### Pigmented MITF-high / OXPHOS control

The CSE program supports mitochondrial energy production, but the cited study does not establish that it is restricted to the MITF-high / PPARGC1A-high pigmented state.

Therefore:

```text
DO_NOT_COLLAPSE := CSE/H2S-persulfide survival into C_PIGMENTED
```

### CD36+ SMC peroxisome/UGCG control

The SMC route is based on peroxisome-dependent lipid metabolism and UGCG-mediated ceramide buffering. The CSE route is a cysteine/transsulfuration/redox-buffering program.

```text
DO_NOT_COLLAPSE := CSE/H2S-persulfide survival into C_SMC_METABOLIC
```

### GPX4/FSP1 ferroptosis boundary

Persulfide-mediated thiol protection is redox-protective, but the 2025 CSE paper is not a direct GPX4/FSP1 niche-switch experiment and does not prove that CSE dependence is equivalent to either ferroptosis-surveillance dependency.

```text
DO_NOT_COLLAPSE := CSE/H2S-persulfide survival into R_FERROPTOSIS_SWITCH
```

## Weakest functional repair

The graph should represent the survival function rather than a named inhibitor:

```text
C_CSE_REDox :=
prevent CSE-dependent H2S/persulfide stress buffering from sustaining
BRAF-V600E drug-tolerant melanoma persisters under targeted-therapy pressure
```

An experimentally supported implementation class is CSE interference during BRAF-V600E inhibition, but no specific compound is promoted to a universal control.

## Genotype boundary

The direct Cell Metabolism result is specifically centered on BRAF-V600E-targeted therapy.

```text
DO_NOT_INFER :=
CSE dependence is universal across NRAS-, NF1-, BRAF-non-V600E-, or
immunotherapy-only melanoma persisters
```

This is the first major scope boundary for the route.

## State-mapping boundary

The paper establishes CSE as vital to the studied persister population but does not provide a matched four-state MRD atlas assigning functional CSE dependency separately to:

```text
pigmented
SMC
NCSC
invasive / SOX10-low
```

Therefore:

```text
MISSING_OBJECT :=
a matched single-cell / functional-dependency map showing which melanoma MRD
states require CSE/H2S-persulfide buffering, whether the dependency is shared
across states, and whether CSE control redistributes survivors into another
state rather than eliminating the persister reservoir.
```

## 2026 lineage-tracing / single-cell state-mapping audit

Li et al. (Molecular Cancer, 2026) provide a newer public lineage-tracing and single-cell surface for targeted-therapy persisters. Their MeRLin study integrates clonal barcoding with scRNA-seq in the BRAF-V600E WM4237-1 melanoma model under BRAFi/MEKi pressure and reports four recurrent-tumor persister-associated programs:

```text
barcode group 1 -> stress-like
barcode group 2 -> neural-crest-like + lipid metabolism
barcode group 3 -> neural-crest-like + PI3K signaling
barcode group 4 -> ECM remodeling
```

The study reports approximately 200 persister-enriched marker genes across groups 1-4 and deposits raw and processed scRNA-seq data under GEO accession `GSE299711` (with bulk RNA-seq under `GSE299589`). The public analysis code is available at `https://github.com/Yeqing95/MeRLin`.

At the manuscript/released-script surface audited here, `CTH` is not reported as a defining marker for any of the four groups and no explicit CTH-by-barcode-group analysis is present in the public scripts. This is not evidence that CTH is absent or unenriched; it means the requested expression ranking is not established by the reported marker summaries alone.

```text
DO_NOT_INFER :=
CTH not listed among reported discriminative markers
  => CTH is absent from a persister state
```

The same study establishes that the four programs are transcriptionally distinct and can coexist across resistant models, making it an appropriate expression-mapping dataset, but expression mapping is still weaker than functional dependency mapping.

A separate 2026 MeRLin melanoma-metastasis lineage-tracing preprint reports neural-crest-like and lipid-metabolism metastatic programs across organs. Its underlying raw/processed scRNA-seq data are stated to become publicly available upon peer-reviewed publication, so it is not presently an independent public expression matrix for resolving CTH state enrichment.

Therefore the state-mapping status does not change:

```text
RESULT := CTH/CSE PHENOTYPE ENRICHMENT NOT YET PROVED

MISSING_OBJECT :=
queryable cell-level CTH expression statistics linked to the MeRLin persister
barcode groups (at minimum detection fraction, normalized expression, and
between-group differential expression), followed by matched CSE perturbation
within those states to determine dependency rather than expression alone.
```

### Exact executable reduction from the released MeRLin analysis

The public MeRLin source now narrows the expression-mapping input to a concrete processed object and metadata field:

```text
SOURCE_OBJECT := EP_Clonocluster.rds
STATE_FIELD   := bc_group
ASSAY         := RNA
LAYER         := data
TARGET_GENE   := CTH
TARGET_STATES := Barcode group 1..4
REFERENCE     := Barcode group 5
```

The released endpoint analysis performs barcode-group differential expression on this object with Seurat. It uses `FindAllMarkers(..., group.by = "bc_group", logfc.threshold = 0.8, min.pct = 0.3, only.pos = TRUE)` for group signatures and also compares each persister group with barcode group 5. The publication reports the stricter discriminative-marker surface as fold change at least 2, detection in at least 50% of cells, and FDR below 0.05.

For `CTH`, the weakest state-mapping computation is therefore fully specified:

```text
for g in Barcode group 1..4:
    detection_fraction[g] := fraction of cells in g with RNA[CTH] > 0
    normalized_mean[g]    := mean normalized RNA-layer CTH expression in g

pairwise_DE := CTH differential expression for each persister group vs group 5
cross_group := CTH differential expression among groups 1..4
```

No `CTH` enrichment result is asserted until those values are read from the processed object or an equivalent exported matrix preserving `bc_group`.

```text
MISSING_OBJECT :=
EP_Clonocluster.rds from the deposited GSE299711 processed data, or an
equivalent cell-by-gene processed expression matrix with cell-level `bc_group`
metadata sufficient to compute CTH detection fraction, normalized expression,
and differential expression for endpoint barcode groups 1-4.
```

This reduces the unresolved expression question from a general literature search to one named dataset object and one named metadata field. It does not reduce the functional-dependency boundary.

Even a positive expression map would not retire `cse_state_mapping_gap` without state-resolved functional dependency and redistribution evidence.

## Cross-state residual object

```text
R_CSE_CROSS_STATE :=
therapy-induced redox/metabolic persister survival that is not certified by
phenotype-state coverage alone
```

This object is orthogonal to the statement that the four classic Rambow states are represented.

## Boundary

```text
BOUNDARY :=
CSE/H2S-persulfide buffering is an evidence-backed BRAF-V600E persister
vulnerability, but its phenotype coverage and genotype generality are not proved
```

## Evidence anchors

- Borbenyi-Galambos et al., Cell Metabolism (2025), `Realigned transsulfuration drives BRAF-V600E-targeted therapy resistance in melanoma`.
  - https://pubmed.ncbi.nlm.nih.gov/40037361/
  - https://doi.org/10.1016/j.cmet.2025.01.021
- Shah et al., Cancer Science (2026), `MAPK Inhibitor-Tolerant Persister Cells in Melanoma: Mechanisms and Therapeutic Vulnerabilities`.
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC13394650/
- Li et al., Molecular Cancer (2026), `Clonal dynamics shaped by diverse drug-tolerant persister states in melanoma resistance`.
  - https://doi.org/10.1186/s12943-026-02622-9
  - GEO: GSE299711 / GSE299589
  - https://github.com/Yeqing95/MeRLin
- `Single-cell lineage tracing maps clonal and transcriptional dynamics in melanoma metastasis` (2026 preprint).
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC13104815/

## Next bounded action

```text
NEXT_ACTIONS :=
1. Retrieve `EP_Clonocluster.rds` from GSE299711, or an equivalent processed matrix preserving `bc_group`.
2. Compute CTH detection fraction and normalized expression for endpoint barcode groups 1-4.
3. Test CTH differential expression for groups 1-4 and against group 5 without treating expression as dependency.
4. Keep cse_state_mapping_gap unresolved unless state-resolved CSE perturbation proves functional coverage and survivor redistribution.
```
