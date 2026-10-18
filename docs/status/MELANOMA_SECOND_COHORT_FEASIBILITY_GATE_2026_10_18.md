# Second independent melanoma cohort — feasibility gate (2026-10-18)

## Decision

**Do not compute or report a second-cohort v2 validation metric yet.** The GSE91061 test failed. A second cohort is necessary for replication, but it must have an expression scale compatible with the frozen GSE78220 ECDF reference, a source-grounded patient/sample manifest, and the exact frozen CR/PR-versus-PD endpoint. Do not refit the v2 reference or coefficients using a candidate validation cohort.

## Candidate audit

### Candidate A — Liu / DFCI metastatic melanoma, Nature Medicine 2019 (mel_dfci_2019)

Public study page: https://www.cbioportal.org/study/summary?id=mel_dfci_2019

The cBioPortal study reports RNA-seq expression for 121 of 144 profiled patients. The original paper provides an RNA-seq TPM matrix as Supplementary Data 2. Published reanalyses report 47 CR/PR responders, 72 SD/PD nonresponders, and 2 heterogeneous responses among the 121 expression-profiled patients.

**Preflight receipt:** workflow run https://github.com/inaciovasquez2020/biological-friction-framework/actions/runs/39086990875; artifact `mel-dfci-v2-cohort-preflight`; pinned source commit `7a4b4ec142f76ac04db22834232b23142d25bd2a`.

Verified by the non-scoring preflight:
- 121 TPM expression sample columns match 121 clinical sample IDs and map to 121 unique patients.
- All seven required genes are present; no patient has multiple expression samples in the matrix.
- Source response counts: 16 Complete Response, 31 Partial Response, 56 Progressive Disease, 16 Stable Disease, and 2 Mixed Response.
- Frozen endpoint crosswalk: 47 CR/PR responders, 56 PD nonresponders, and 18 excluded SD/mixed cases.
- The initial preflight had an endpoint-label bug that excluded Complete/Partial Response. It was corrected, covered by five regression tests, and the corrected preflight passed.

**Remaining blocker before scoring:**
1. The frozen GSE78220 reference was built from GEO's `GSE78220_PatientFPKM.xlsx` matrix. The Liu matrix is TPM. TPM and FPKM are not guaranteed to be a single global strictly increasing transform across samples; TPM introduces sample-specific scaling. Applying the frozen ECDF directly to TPM without proving measurement compatibility would make the score technically computable but the validation interpretation unsound.

No response-informed conversion or refitting is permitted. If scale compatibility cannot be established independently, record **not comparable under v2** and do not score this cohort.

Status: **source/sample mapping and endpoint crosswalk passed; expression-scale compatibility remains unresolved, so the cohort is not eligible for locked v2 scoring.**

### Candidate B — Gide / Melanoma Institute Australia (PRJEB23709)

BioProject: https://www.ncbi.nlm.nih.gov/bioproject/PRJEB23709

The BioProject reports 91 SRA experiments and includes patients treated with anti-PD-1 monotherapy and anti-PD-1 plus anti-CTLA-4. Published reports describe 73 pretreatment tumors in related analyses, with treatment arms having different responder counts.

**Blocking items before scoring:**
1. Need a reproducible patient/sample manifest and exact mapping of pretreatment biopsies to response labels.
2. Need to separate anti-PD-1 monotherapy from combination therapy or predeclare a treatment-arm-stratified analysis; do not pool unlike regimens without a frozen rationale.
3. Available public records primarily identify sequence experiments. The processed expression matrix, reference annotation, and sample identity mapping need to be verified. Reprocessing raw FASTQ would require a fixed pipeline and should not silently replace the frozen v2 reference scale.
4. Resolve whether each sample is bulk RNA-seq or single-cell-derived in the particular source surface being used; the same accession is described differently in secondary studies.

Status: **potentially independent, but data/endpoint processing burden is materially higher.**

### Candidate C — MGH GSE168204

GEO: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE168204

GEO lists 27 samples and a featureCounts raw-count matrix. Its sample annotations use study-specific R/NR labels, and published analyses include pretreatment and on-treatment biopsies.

**Decision:** not the immediate replication cohort. The sample count is small, repeated timepoints must be separated at patient level, and R/NR cannot be assumed equivalent to the frozen CR/PR-versus-PD endpoint without reconstructing the underlying response definitions. It may be useful only if patient-level endpoint compatibility can be established from source metadata.

## Locked next-step requirements

Before any second cohort is scored, retain an auditable preflight receipt with:
- source URL and checksum for each expression and clinical file;
- exact expression unit / quantification method and justification for compatibility with the frozen GSE78220 FPKM reference;
- seven-gene ID mapping and missingness audit;
- sample-to-patient mapping and one pretreatment sample per patient;
- response-label crosswalk preserving CR/PR, PD, and excluded SD/unknown/mixed categories;
- treatment regimen and any cohort-overlap audit;
- explicit pass/fail decision before computing outcome metrics.

Do not estimate or optimize a conversion from candidate expression to the development reference using response labels. If expression compatibility cannot be demonstrated without refitting the frozen reference, the correct outcome is **not comparable under v2**; a separately versioned model and new calibration would be a different study, not replication of this v2.

## Claim boundary

GSE91061 failed its prespecified promotion gate. No second independent cohort has yet replicated v2. Neither this feasibility note nor any candidate dataset establishes predictive validity, treatment selection, clinical utility, efficacy, or cure.
