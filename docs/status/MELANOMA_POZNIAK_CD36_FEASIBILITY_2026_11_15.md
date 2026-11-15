# Cell-resolved melanoma CD36 source audit: Poźniak lead and competing datasets

Date: 2026-11-15  
Status: **PUBLIC SOURCE IDENTIFIED / EXACT PATIENT CROSSWALK OPEN / NO PATIENT ANALYSIS**

## Objective

Determine whether a common, patient-matched pretreatment sample supplies malignant-cell and macrophage CD36, anti-PD-1 monotherapy and a source-grounded CR/PR versus PD endpoint, without touching frozen melanoma v2.

## Highest-priority source: Poźniak et al. (2024)

- Primary paper: Poźniak et al., *A TCF4-dependent gene regulatory network confers resistance to immunotherapy in melanoma*, *Cell* 187, 166–183.e25 (2024), DOI https://doi.org/10.1016/j.cell.2023.11.037 .
- Public original data repository: https://doi.org/10.48804/GSAXBN ; KU Leuven dataset title *Dissecting the melanoma ecosystem one cell at the time during immunotherapy*.
- KU Leuven's data record explicitly lists **Entire_TME.rds** (approximately 2.5 GB), **Malignant_cells.rds** (approximately 824.4 MB), **GC_all_immune_sharing.rds** (approximately 945.2 MB), and a small **Pozniak_README_v6.txt**. It describes count matrices for malignant and whole-tumor-microenvironment cells, and links clinical metadata to original article Table S1.
- Chakraborty et al., *Genome Medicine*, 2026, https://doi.org/10.1186/s13073-026-01794-9, independently analyzed a 23-patient Poźniak cohort, its macrophage compartment and pre/early-treatment biopsies. Their paper reports mixed anti-PD-1 monotherapy and anti-PD-1/anti-CTLA-4 regimens, clinical response per RECIST v1.1, and an exploratory patient-level LA-TAM difference among treatment-naive responders/nonresponders (p=0.0083).
- **Key caveat:** exact baseline anti-PD-1-monotherapy subset membership, individual patient IDs, cell type CD36 values, whether malignant and macrophage cells were actually recovered from *each* eligible sample, and endpoint CR/PR/PD membership are **not established** by the source page or abstract alone. A generic favorable/unfavorable label must not be silently mapped to the frozen endpoint.
- No source-data RDS downloaded in this audit. Large objects are not justified before the small clinical Table S1/sample manifest preflight and consent/license assessment.

## Other candidates / why not promoted

- **Zhang et al., Theranostics (2024)**, https://www.thno.org/v14p2127.htm : a neoadjuvant anti-PD-1 scRNA-seq cohort with **11 patients** (3 PD, 8 *non-progressive disease*), pre/post biopsies and malignant/myeloid compartments. Data provenance HRA005837 https://bigd.big.ac.cn/gsa . **NPD is not synonymous with CR/PR**, and the paper says raw data may require author request; exact endpoint and public extractability are unresolved.
- **Jerby-Arnon et al. GSE115978**, https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE115978 : processed counts (49.1 MB), TPM (227.4 MB) and cell annotation (98.9 KB) are publicly listed. Pre-ICI cases plus resistant post-ICI cases and anti-PD1/anti-CTLA4 mixing exist; a 2025 reanalysis reports 16 pre-treatment response-labeled biopsies but their actual therapy for this stratum is listed as unknown. No arm-verified patient subset has been accepted.
- **Sade-Feldman GSE120575** includes clinical response but sorted CD45+ immune cells: it cannot alone supply tumor-intrinsic CD36.
- **Di Pietro GSE294273**, https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE294273 : 12 public single-cell samples across untreated, ICI-resistant and ICI-responsive groups. These are not an independently verified pretreatment PD1-monotherapy CR/PR-vs-PD cohort.

## Executable-gate correctness finding

Previous preflight implementation incorrectly required `malignant_cd36_source != macrophage_cd36_source`. This is a **false-negative**: a valid same-biopsy RNA count dataset often contains both compartments, so source file identifiers may be identical. The necessary structural distinction is the **annotated cell labels**, not the provenance file identifier.

The revised `infra/ci/melanoma_cd36_preflight.py` accepts equal source identifiers and requires nonempty `malignant_cell_label` and `macrophage_cell_label` that differ. Its test file now contains a shared-source acceptance case and identical-label rejection. **This remains a self-attested manifest gate:** distinct strings, positive yes flags, and a URL are not independent proof that a patient, sample, assay, response or cell label is genuine.

## Fail-closed status

```text
POZNIAK_SOURCE_REPOSITORY_FOUND := TRUE
POZNIAK_COUNT_OBJECTS_LISTED := TRUE
POZNIAK_RAW_DATA_DOWNLOADED := FALSE
POZNIAK_TREATMENT_AND_SAMPLE_CROSSWALK := OPEN
POZNIAK_CELL_RESOLVED_CD36_COMPUTED := FALSE
POZNIAK_CLINICAL_PREDICTION_COMPUTED := FALSE
SINGLE_CELL_SIGNAL_SCALE_TO_FROZEN_V2_FPKM := NOT_ESTABLISHED
PREFLIGHT_SOURCE_IDENTIFIER_FALSE_NEGATIVE := CORRECTED_IN_CODE
EXACT_HEAD_PYTHON_TESTS := NOT_RUN
FROZEN_V2_NEGATIVE_EXTERNAL_VALIDATION := UNCHANGED
BFF_RETROSPECTIVE_CLINICAL_VALIDATION := OPEN
```

### Next decisive action

Retrieve only the clinical Table S1 / lightweight sample README and record exact study patient ID, biopsy ID, timepoint, regimen, RECIST outcome, malignant/macrophage cell availability and original source reference. Determine the eligible *patient* count **before** any of the ~0.8–2.5 GB Seurat downloads. If this fails, return a blocked source crosswalk, not a synthetic score.
