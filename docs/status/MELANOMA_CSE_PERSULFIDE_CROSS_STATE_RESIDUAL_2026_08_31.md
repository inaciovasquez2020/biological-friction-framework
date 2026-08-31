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

The manuscript/released-script surface did not report `CTH` as a defining marker for any of the four groups. That literature-level absence was not treated as evidence that CTH was absent or unenriched. The deposited endpoint object has now been interrogated directly.

### Direct GSE299711 endpoint-object extraction

The public GEO `filelist.txt` identifies the exact endpoint object:

```text
SOURCE_ARCHIVE := GSE299711_RAW.tar
SOURCE_MEMBER  := GSM9044666_EP_Clonocluster.rds
MEMBER_SIZE    := 689218608 bytes
STATE_FIELD    := bc_group
ASSAY          := RNA
LAYER          := data
TARGET_GENE    := CTH
```

The uncompressed TAR member was located and range-extracted without downloading the full archive. The verified member byte interval is:

```text
header_offset := 1896608768
data_start    := 1896609280
data_end      := 2585827887
```

The retrieved object is a Seurat v5 object with an `Assay5` RNA assay. Its `data` layer contains 38,607 features and 2,565 endpoint cells; `CTH` is present in the Assay5 feature map. Cells were aligned to `bc_group` through the assay cell map before extracting normalized `CTH` values.

`RESULT := CTH EXPRESSION IS HETEROGENEOUS ACROSS MERLIN ENDPOINT BARCODE STATES; NO UNIFORM PERSISTER-STATE ENRICHMENT IS SUPPORTED BY THE DESCRIPTIVE MAP`

The direct descriptive endpoint map is:

| MeRLin endpoint group | n | CTH detection fraction | normalized mean | normalized median |
| --- | ---: | ---: | ---: | ---: |
| Barcode group 1 — stress-like | 999 | 0.52052052 | 0.21795571 | 0.12933725 |
| Barcode group 2 — neural-crest-like + lipid metabolism | 643 | 0.67340591 | 0.34331515 | 0.26612383 |
| Barcode group 3 — neural-crest-like + PI3K signaling | 256 | 0.52734375 | 0.19099902 | 0.12832013 |
| Barcode group 4 — ECM remodeling | 378 | 0.51058201 | 0.18793363 | 0.10122350 |
| Barcode group 5 — reference / non-persister-like | 267 | 0.56928839 | 0.34165966 | 0.32992894 |

There are also 22 endpoint cells labeled `NA` in `bc_group`; they are not used to define any of the five named state comparisons above.

The descriptive pattern is not a uniform increase across the four persister groups. Barcode group 2 has the highest CTH detection fraction (`0.6734`) and a normalized mean (`0.3433`) essentially equal to barcode group 5 (`0.3417`). Groups 1, 3, and 4 have lower normalized means than group 5 on this endpoint surface.

Therefore retire the earlier data-availability statement:

```text
RETIRE := CTH endpoint expression ranking is unavailable
```

but do not replace it with a functional-state conclusion:

```text
DO_NOT_INFER := transcript abundance => CSE functional dependency
DO_NOT_INFER := lower or non-enriched CTH transcript => absence of CSE dependency
DO_NOT_INFER := high CTH detection in barcode group 2 => unique CSE dependence of group 2
```

The endpoint object answers the descriptive expression-ranking question only. It does not establish differential-expression significance by itself and does not test what happens to each barcode state after CSE perturbation.

The state-mapping gap therefore remains reachable, but its missing object is now narrower:

```text
MISSING_OBJECT :=
state-resolved CTH/CSE perturbation within the same MeRLin endpoint barcode
states, with functional persister-survival and survivor-redistribution readouts,
together with formal differential-expression testing where expression enrichment
rather than dependency is being claimed.
```

Even a statistically significant expression contrast would not retire `cse_state_mapping_gap` without state-resolved functional dependency and redistribution evidence.

## Cross-state residual object

```text
R_CSE_CROSS_STATE :=
therapy-induced redox/metabolic persister survival that is not certified by
phenotype-state coverage alone
```

The direct MeRLin endpoint map means this object should not be interpreted as claiming uniformly high `CTH` transcript across all persister states. `cross-state` here refers to the unresolved scope of the functional stress-survival mechanism, not a demonstrated pan-state expression signature.

## Boundary

```text
BOUNDARY :=
CSE/H2S-persulfide buffering is an evidence-backed BRAF-V600E persister
vulnerability, but the MeRLin endpoint CTH transcript map is heterogeneous and
state-resolved functional CSE dependency / survivor redistribution remain unproved
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
1. Keep `cse_state_mapping_gap` reachable; do not credit descriptive CTH expression as functional closure.
2. Run formal endpoint CTH differential-expression contrasts for groups 1-4 versus group 5 only if an expression-enrichment claim is needed.
3. Search for or require state-resolved CSE perturbation with barcode-state survivor and redistribution readouts.
4. If no such experiment exists, retain the functional state-mapping boundary and move to the next executable unresolved state.
```
