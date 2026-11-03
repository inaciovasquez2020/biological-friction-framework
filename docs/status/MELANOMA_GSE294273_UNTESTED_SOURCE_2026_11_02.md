# GSE294273 — external melanoma scRNA-seq candidate (source registration only)

Date: 2026-11-02  
Status: **REGISTERED / UNTESTED / NO SCORE COMPUTED**  
Source: [NCBI GEO GSE294273](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE294273)  
BioProject: PRJNA1248923

## Authenticated public metadata

- GEO series title: *Tumor-resident T cells and dendritic cells form an in situ archetype for immunotherapy response in melanoma [scRNA-seq]*.
- Public since June 8, 2026; accession metadata last updated September 21, 2026.
- Human melanoma single-cell RNA-seq, platform GPL24676 (Illumina NovaSeq 6000).
- Twelve **samples**: four untreated, four ICI-resistant, four ICI-responsive. This source description is **not** evidence that all twelve are independent patients.
- Public supplementary processed data: `GSE294273_RAW.tar`, approximately 742.5 MB, comprising MTX/TSV.
- Personally identifiable raw human sequencing data are described by GEO as controlled-access through the European Genome-phenome Archive (EGA).
- The source study also discusses spatial data across a larger sample collection, but this accession represents the twelve scRNA-seq samples only.

## Proposed bounded research use

Register this series as a **candidate for exploratory, cohort-aware biological interaction-graph analysis** of tumor-resident T-cell and dendritic-cell associations in ICI-responsive versus resistant melanoma. Any source claims about interaction mechanisms must be treated as published hypotheses/observations, not as discoveries validated by this repository.

## Required preflight before any calculation

1. Obtain and verify the publicly distributed processed MTX/TSV archive; record its actual byte digest, sample metadata, cell filtering, normalization, and gene annotation.
2. Reconcile sample IDs, unique patient identities, treatment exposure/timing, and study-defined outcome labels using original accession metadata and linked study; do not assume `ICI-resistant` means frozen `PD` or `ICI-responsive` means frozen `CR/PR`.
3. Establish whether baseline pretreatment anti-PD-1 monotherapy samples exist and meet the original frozen endpoint protocol.
4. Do **not** apply the frozen GSE78220 seven-gene FPKM-ECDF v2 scorer to single-cell counts, MTX entries, TPM, pseudobulk, or transformed expression without a predeclared and independently justified cross-assay scale-compatibility demonstration.
5. If an interaction-graph exploratory test is performed, freeze its patient-level aggregation, cell composition handling, null model, and uncertainty protocol before consulting clinical response labels; label it **new exploratory analysis**, not v2 external validation.

## Locked legacy evidence remains unchanged

The prior [GSE91061 frozen v2 validation](MELANOMA_GSE91061_V2_EXTERNAL_VALIDATION_2026_10_18.md) did not meet its promotion gate (AUROC 0.4913; Brier score worse than prevalence-only). The [second-cohort feasibility gate](MELANOMA_SECOND_COHORT_FEASIBILITY_GATE_2026_10_18.md) requires a source-grounded sample/response manifest and expression-scale comparability. Neither result is overridden by registration of this new GEO accession.

```text
GSE294273_SOURCE_IDENTIFIED := TRUE
GSE294273_DATA_DOWNLOADED := FALSE
GSE294273_ARCHIVE_SHA256 := NOT_RECORDED
GSE294273_PATIENT_ENDPOINT_MAPPING := NOT_ESTABLISHED
GSE294273_V2_SCALE_COMPATIBILITY := NOT_ESTABLISHED
GSE294273_MODEL_SCORED := FALSE
GSE294273_INDEPENDENT_VALIDATION := FALSE
RETROSPECTIVELY_VALIDATED_PREDICTIVE_MODEL := FALSE
CLINICAL_UTILITY := NOT_ESTABLISHED
```

**BOUNDARY:** Registration of public data is not the empirical reproduction, predictive validation, mechanism proof, clinical recommendation, treatment-selection evidence, or cure claim.
