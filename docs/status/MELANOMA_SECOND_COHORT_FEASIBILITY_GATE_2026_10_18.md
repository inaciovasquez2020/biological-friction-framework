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

The BioProject contains 91 SRA runs across anti-PD-1 monotherapy and anti-PD-1 plus anti-CTLA-4 treatment. A non-scoring accession crosswalk is now available in two public reanalysis repositories:

- `xmuyulab/ims_gene_signature/data/mel_gide19_cli_data.csv` (clinical run accession, `pre/on`, response code).
- `yuexujiang/IRnet/data/Gide/clinic.txt` and `qiluzhou/TMEImmune/TMEImmune/data/Gide/patient_df.txt` (run accession, response, and patient/sample alias or drug/target).

**Accession-level result:** all 41 `pre` rows in the processed Gide19 clinical table match a run accession in the IRnet table, and each maps to a `PD1_<patient-number>_PRE` alias. The corresponding TMEImmune table independently lists those same accessions as `AntiPD1` / `PD1`. No pretreatment accession was unmatched. This supports the sample-level mapping and anti-PD-1 monotherapy assignment for these 41 rows; it is materially stronger than matching cohort counts alone.

**Response-label crosswalk:** the processed clinical table contains 19 code-1 rows, 16 code-0 rows, and 6 code-`-1` rows among those 41 pretreatment samples. In the binary secondary reanalysis, the six code-`-1` stable-disease samples are collapsed into response code 0 alongside the 16 code-0 samples. Therefore the secondary binary label must not be treated as a faithful three-class endpoint. Cui et al. define the intended endpoint as CR/PR versus PD under RECIST 1.1, excluding SD from AUC (https://pmc.ncbi.nlm.nih.gov/articles/PMC7862369/). The accessions and treatment aliases are now reconciled across processed source tables, and the three-way code structure is consistent with that endpoint design. However, the secondary tables do not expose each patient's original RECIST category as a separate field; exact primary-source CR/PR-versus-PD verification remains **conditional on the published code semantics**, not independently proven by the alias crosswalk alone.

**Expression-scale gate remains blocked.** The processed matrix has 20,294 gene rows by 91 sample columns, includes all seven frozen v2 genes, and the 41 pretreatment accessions join to expression columns. However, the loader describes quantile-normalized/log2-transformed expression and conditionally applies `log2(x + 1)` when a dataset maximum exceeds 500. Cui et al. report a STAR/RSEM gene-level FPKM workflow followed by log transformation. These different processing descriptions do not establish numerical compatibility with the frozen GSE78220 Cuffnorm FPKM ECDF reference. Do not substitute the processed matrix directly into frozen v2 scoring.

**Preflight decision:** sample accession and treatment-arm crosswalk = **PASS for the 41 pretreatment rows**; exact primary RECIST mapping = **CONDITIONAL**; frozen-reference expression-scale compatibility = **FAIL / unresolved**. Gide remains ineligible for frozen v2 scoring regardless of the endpoint crosswalk result. Do not refit the v2 reference or estimate a response-informed conversion. If compatibility cannot be established by a fixed, independently justified processing route, record `NOT_COMPARABLE_UNDER_V2`.

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
