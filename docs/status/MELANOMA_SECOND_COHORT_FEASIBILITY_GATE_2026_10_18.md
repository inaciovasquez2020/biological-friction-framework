# Second independent melanoma cohort — feasibility gate (2026-10-18)

## Decision

**Do not compute or report a second-cohort v2 validation metric yet.** The GSE91061 test failed. A second cohort is necessary for replication, but it must have an expression scale compatible with the frozen GSE78220 ECDF reference, a source-grounded patient/sample manifest, and the exact frozen CR/PR-versus-PD endpoint. Do not refit the v2 reference or coefficients using a candidate validation cohort.

## Candidate audit

### Candidate A — Liu / DFCI metastatic melanoma, Nature Medicine 2019 (mel_dfci_2019)

Public study page: https://www.cbioportal.org/study/summary?id=mel_dfci_2019

The cBioPortal study reports RNA-seq expression for 121 of 144 profiled patients. The original paper provides an RNA-seq TPM matrix as Supplementary Data 2. Published reanalyses report 47 CR/PR responders, 72 SD/PD nonresponders, and 2 heterogeneous responses among the 121 expression-profiled patients.

**Blocking items before scoring:**
1. The frozen GSE78220 reference was built from the GEO GSE78220_PatientFPKM.xlsx matrix. The Liu supplement is TPM. TPM and FPKM are not guaranteed to be a single global strictly increasing transform across samples; TPM introduces sample-specific scaling. Applying the frozen ECDF directly to TPM without proving measurement compatibility would make the score technically computable but the validation interpretation unsound.
2. The 47/72/2 published grouping combines SD with PD in the nonresponder class, while the frozen v2 primary endpoint is CR/PR versus PD and explicitly excludes SD. The clinical response table must be obtained and joined to the expression matrix to identify PD-only patients; do not substitute the published binary grouping.
3. Verify patient identifiers, response annotation, duplicate specimens, missing seven-gene values, and the exact set of patients represented in the expression matrix before opening outcomes to scoring.

Status: **promising cohort; not yet eligible for locked v2 scoring.**

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
