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

**Scale-compatibility result: blocked from v2 scoring.**

The frozen GSE78220 reference was built from GEO's `GSE78220_PatientFPKM.xlsx` matrix; the available cBioPortal Liu matrix is TPM. For sample (s), the relationship is

`TPM[g,s] = 10^6 × FPKM[g,s] / sum_j FPKM[j,s]`.

Recovering FPKM therefore requires the sample-specific `sum_j FPKM[j,s]` value under the same gene universe and quantification convention. TPM values alone do not identify that value. The unknown factor can differ by sample, and the frozen scorer applies each gene's development-reference ECDF to its raw expression value; a sample-specific scale factor can change those ECDF positions. There is no mathematically justified direct substitution of TPM for FPKM.

The Liu study's code repository also describes a separate raw-count matrix. That does not by itself establish equivalence to the frozen Cuffnorm FPKM matrix: a reconstruction would need a fixed, documented quantification/annotation procedure and independent evidence that its resulting values are compatible with the frozen reference. No such reconstruction or equivalence evidence is currently established.

No response-informed conversion or refitting is permitted. Current decision: **not comparable under v2 on the available TPM matrix**. Do not compute a v2 score from TPM. A future same-pipeline reconstruction would be a new preflight gate, not permission to score by assumption.

Status: **source/sample mapping and endpoint crosswalk passed; expression-scale compatibility remains unresolved, so the cohort is not eligible for locked v2 scoring.**

### Candidate B — Gide / Melanoma Institute Australia (PRJEB23709)

BioProject: https://www.ncbi.nlm.nih.gov/bioproject/PRJEB23709

The BioProject reports 91 SRA experiments and includes patients treated with anti-PD-1 monotherapy and anti-PD-1 plus anti-CTLA-4. A published secondary analysis reports 72 pretreatment anti-PD-1-monotherapy samples (45 R, 27 NR) after its own exclusions; it also notes that 30 of the 54 monotherapy patients had prior anti-CTLA-4. A separate reanalysis reports restricting to 41 patients with baseline samples and processing raw reads with STAR 2-pass, HTSeq-count, then an NCI/GDC-style FPKM procedure. These are useful provenance leads, but they do not supply a verified manifest for the exact frozen CR/PR-versus-PD endpoint, and they do not prove that the resulting FPKM values are numerically compatible with the frozen GSE78220 Cuffnorm reference. Sources: https://pmc.ncbi.nlm.nih.gov/articles/PMC8519947/ and https://discovery.ucl.ac.uk/id/eprint/10135694/1/s41467-021-25894-9.pdf

**Blocking items before scoring:**
1. **Cohort-level cross-check improved; accession-level reconciliation still open.** Cui et al. report 41 baseline Gide19 samples restricted to anti-PD-1 monotherapy and explicitly define R as CR/PR and NR as PD under RECIST 1.1; stable disease is excluded from AUC. The processed `mel_gide19_cli_data.csv` also contains 41 pretreatment rows with 19 coded responders, 16 nonresponders, and 6 stable-disease cases, which is numerically consistent with that published endpoint structure. However, the publication does not expose an accession-by-accession crosswalk in the material verified here, so do not claim that the 41 rows have been individually reconciled to the published cohort. Source: https://pmc.ncbi.nlm.nih.gov/articles/PMC7862369/
2. Need to separate anti-PD-1 monotherapy from combination therapy or predeclare a treatment-arm-stratified analysis; do not pool unlike regimens without a frozen rationale.
2.5. **Response-code provenance correction:** the `xmuyulab/ims_gene_signature` README's `1 = responder`, `0 = nonresponder`, and `-1 = stable disease` note is explicitly about its *survival data*, not a sufficient definition of the clinical response endpoint. The separate Gide19 baseline analysis by Cui et al. defines responders as CR/PR and nonresponders as PD under RECIST 1.1, and reports 41 Gide19 baseline patients. However, accession-level reconciliation of that 41-patient analysis with the processed 41 pretreatment rows (currently counted as 19 responder, 16 nonresponder, 6 stable disease) has not been demonstrated. Therefore the endpoint mapping for this exact matrix remains blocked; do not infer that the two 41-patient sets are identical. Source: https://pmc.ncbi.nlm.nih.gov/articles/PMC7862369/

2.6. **Published response definitions are not interchangeable.** Cui et al. describe the 41-patient Gide19 baseline cohort, restrict it to anti-PD-1 monotherapy, use RECIST 1.1 response categories (CR/PR versus PD, with SD excluded from AUC), and state that Gide19 raw RNA-seq was processed with STAR/RSEM to gene-level FPKM followed by log2 transformation ([Cui et al., 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC7862369/)). Other reanalyses report a Gide cohort split of 22 responders and 19 nonresponders ([example review/reanalysis](https://pmc.ncbi.nlm.nih.gov/articles/PMC8907429/)); such counts can reflect a different response rule, including treatment-duration-based grouping, rather than the frozen CR/PR-versus-PD endpoint. This is a concrete reason not to infer endpoint equivalence from the shared label “Gide19,” cohort size, or matching counts alone. The processed matrix currently has 19 coded responders, 16 coded nonresponders, and 6 SD. Until each accession's clinical code is reconciled to the exact RECIST category and treatment arm, the endpoint gate remains **FAIL / unresolved**. The published STAR/RSEM/log2-FPKM workflow is a provenance lead, not proof of compatibility with the frozen GSE78220 Cuffnorm reference.

3. The processed `xmuyulab/ims_gene_signature` Gide matrix is accessible: 20,294 gene rows by 91 sample columns; the seven frozen v2 genes are present, and the 41 pretreatment accessions in its clinical table match expression columns. The repository loader explicitly describes the data as quantile-normalized and log2-transformed, and conditionally applies `log2(x + 1)` when a dataset maximum exceeds 500. These checks establish parseability and accession joins, not equivalence to the frozen GSE78220 Cuffnorm FPKM reference. The matrix is therefore eligible for provenance inspection but not v2 scoring. Raw-read reprocessing would require a fixed, documented pipeline and independent evidence of compatibility with the frozen reference.
4. Resolve whether each sample is bulk RNA-seq or single-cell-derived in the particular source surface being used; the same accession is described differently in secondary studies.

Status: **potentially independent, but data/endpoint processing burden is materially higher.**

### Candidate B2 — MGH GSE115821

GEO: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE115821

GEO provides a featureCounts raw-count matrix, not the frozen GSE78220 Cuffnorm FPKM values. Sample metadata include pretreatment and on-treatment biopsies, repeat biopsies for some patients, anti-PD-1 and anti-CTLA-4 exposure, and study-specific response labels (R/NR). A recent secondary analysis reports only 37 baseline samples for a related analysis, with 3 responders and 34 nonresponders; those labels and inclusion rules are not automatically the frozen CR/PR-versus-PD endpoint.

**Decision:** not ready for frozen v2 scoring. It would require a patient-level baseline-only manifest, exact response reconstruction, treatment/prior-therapy audit, and a defensible expression-scale reconstruction. The very small responder count also makes performance estimates unstable.

### Candidate C — MGH GSE168204

GEO: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE168204

GEO lists 27 samples and a featureCounts raw-count matrix. Its sample annotations use study-specific R/NR labels, and published analyses include pretreatment and on-treatment biopsies.

**Decision:** not the immediate replication cohort. The sample count is small, repeated timepoints must be separated at patient level, and R/NR cannot be assumed equivalent to the frozen CR/PR-versus-PD endpoint without reconstructing the underlying response definitions. It may be useful only if patient-level endpoint compatibility can be established from source metadata.

## Comparative conclusion after the next-candidate search

No candidate located in this pass is ready for a valid second v2 score:
- **Liu/DFCI:** source mapping and CR/PR-versus-PD endpoint crosswalk passed, but the available matrix is TPM and is not invertible to FPKM without sample-specific scaling information; separate raw counts do not establish same-pipeline compatibility.
- **Gide/PRJEB23709:** a secondary analysis provides candidate baseline counts (72 pretreatment anti-PD-1-monotherapy samples, 45 R/27 NR), and another reports a reproducible raw-read-to-FPKM pipeline on 41 baseline patients. This makes Gide the best next candidate for a *non-scoring provenance audit*, but not yet a valid v2 score: endpoint mapping, prior anti-CTLA-4 handling, sample manifest, and numerical compatibility with the frozen Cuffnorm reference remain unverified. Anti-PD-1 combination samples must stay separate.
- **MGH GSE115821 / GSE168204:** public count matrices, but timepoint/repeated-biopsy issues and R/NR labels or low responder counts prevent immediate frozen-endpoint replication.

This is a data-compatibility stop, not evidence that no other cohort exists. The current v2 validation program has one completed independent test (GSE91061), and it failed the prespecified promotion gate. A second score should not be produced merely to fill the replication requirement.

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
