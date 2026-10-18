# GSE165745 evidence dossier: endpoint, assay scale, panel, and prediction boundary
Date: 2026-10-18

## Purpose
Record the available primary-source evidence for the exploratory melanoma Wnt score. This is a research audit, not a clinical validation report.

## Primary sources checked
1. GEO series GSE165745: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE165745
2. Original paper, DeVito et al., *Pharmacological Wnt ligand inhibition overcomes key tumor-mediated resistance pathways to anti-PD-1 immunotherapy*, Cell Reports 35 (2021), 109071, DOI 10.1016/j.celrep.2021.109071; PMC8148423; PMID 33951424: https://pmc.ncbi.nlm.nih.gov/articles/PMC8148423/
3. GEO series GSE280470, a later study explicitly including previously published GSE165745 samples with updated clinical data: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE280470
4. GEO sample pages, e.g. GSM5049353 and GSM5049357, which show processed sample tables and links to sample-level RCC.gz files:
   - https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM5049353
   - https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM5049357

## Confirmed cohort facts
- GSE165745 is public, submitted 2021-01-28 and last updated 2021-05-06 in the GEO record.
- There are 24 samples: GSM5049348–GSM5049359 are titled R001–R012 / Responder_001–Responder_012; GSM5049360–GSM5049371 are NR001–NR012 / Nonresponder_001–Nonresponder_012.
- The GEO series describes FFPE metastatic melanoma samples profiled before anti-PD-1 treatment with the NanoString nCounter Vantage 3D Human Wnt Pathways Panel (N2_WNT_Pth_v1.0), with custom immune markers including cytolytic T-cell markers and IDO1.
- The original paper's methods state that archival specimens were from treatment-naive patients receiving anti-PD-1 monotherapy (pembrolizumab or nivolumab) under clinical trial NCT02694965; pathology review and microdissection were performed when needed.
- The paper's Figure 1D describes 12 responders and 12 nonresponders. It reports panel-wide multiple-comparison adjustment using Benjamini–Yekutieli FDR control.
- GEO sample descriptions say the samples were analyzed with NanoString nSolver. This names the software but does not by itself specify the complete normalization/background-correction/transformation settings used for the exported values.
- GEO's sample data tables are labeled “Gene conts” and list 204 rows. Each sample also links an RCC.gz file. Sample values differ markedly in scale across sample pages, so the data contract must be established from the series matrix and raw RCC/nSolver exports rather than assuming all displayed values are directly comparable without checking.

## Published biology: what it does and does not support
The paper reports Wnt ligands and FZD receptors elevated in nonresponders and RNF43 higher in responders in the separate GSE78220 RNA-seq reanalysis. In the 24-sample NanoString analysis it reports evidence of elevated canonical and non-canonical Wnt signaling in nonresponders, including Wnt ligands, FZD receptors, LRP5, PYGO1, DVL1, DKK2 and SFRP2.
This supports investigating a Wnt-associated resistance hypothesis. It does NOT validate our specific arithmetic score (mean log1p of a selected resistance-associated gene list minus log1p(RNF43)), its weighting, its use of all genes present, its transformation, or any clinical cutoff. The paper's differential-expression analysis is not itself a locked, externally validated patient-level classifier.

## Score implementation audit
Current implementation is in `infra/ci/develop_melanoma_wnt_v1.py`.
- It uses GEO sample titles to assign outcome: R* = responder; NR* / nonresponder = nonresponder. The labels are therefore derived from deposited labels, not independently re-adjudicated clinical records.
- It uppercases `ID_REF` symbols and treats them as gene keys. A formal mapping to the platform's exact target/probe list and any alias handling is not yet recorded.
- It applies `log1p` to deposited `VALUE` fields, then takes the mean across genes. The sources checked so far do not establish that this transform is correct for the deposited values.
- The formula includes a biologically motivated but unvalidated gene list. It is not the paper's reported model.
- The code's threshold is the midpoint of the observed minimum and maximum scores, computed on the same 24 outcomes being evaluated. Although the AUROC is threshold-independent, the reported balanced accuracy at this data-derived threshold is descriptive and is not a valid locked-threshold performance estimate. Do not present it as a deployable cutoff.
- The executed AUROC for nonresponse is 0.5208333333 (n=24), approximately chance. Preserve this result; do not tune the score on this cohort.

## Clinical endpoint: still unresolved
GEO titles establish the deposited binary labels but not the full clinical definition. The exact response criteria (e.g. RECIST version or another adjudication method), assessment window, duration/confirmation rules, clinical follow-up, and missing/unevaluable case handling were not established by the GEO fields reviewed. The original paper refers to responders/nonresponders but these exact operational details need to be extracted from Table S2 and any linked clinical metadata before claiming endpoint reproducibility.

## Normalization / assay scale: still unresolved
The paper says nSolver was used. In the methods examined, it does not specify the exact nSolver normalization configuration for this cohort: background subtraction, positive-control normalization, housekeeping gene selection/normalization, threshold settings, any transformations, and export field semantics. The GEO `VALUE` field must not be assumed to be raw counts or a known log scale solely from the column label. Raw RCC.gz files are linked at the sample level; retrieve all 24 and compare their raw target counts and QC/control attributes to the processed GEO values. If reconstructing normalization requires nSolver-specific algorithms or reference selection not fully documented, mark it non-reproducible from public artifacts rather than guessing.

## Supplementary tables
The paper explicitly refers to Tables S1 and S2 for the GSE78220 reanalysis and the 24-sample NanoString analysis, respectively. The full supplementary files are listed on the PMC article page. Their exact table contents and all per-gene effect sizes/p-adjusted values have not yet been extracted into this dossier. Therefore, the published gene-level support for each member of our proposed score is not yet fully crosswalked.

## GSE280470 overlap
GSE280470's GEO description explicitly states that it includes previously published GSE165745 samples with updated clinical data. This is potentially useful for reconciling labels and clinical annotations, but the overlapping patients must not be counted as independent external validation. Any genuinely new cases must be identified by sample/patient identity before evaluating.

## Exact next work required
1. Retrieve the full paper supplements and extract Tables S1 and S2, including all genes, effect directions, effect sizes, raw p-values, adjusted p-values, and clinical characteristics relevant to response.
2. Download all 24 sample RCC.gz files plus the series matrix. Record SHA-256 checksums, sample-ID crosswalk, RCC QC/control metadata, target counts, and mapping to GEO `VALUE`.
3. Determine and document which `VALUE` table each sample exposes, whether the series matrix contains the same values, and whether samples are on a common processed scale. Do not apply `log1p` until justified.
4. Retrieve GSE280470's updated clinical data and construct an overlap map to GSE165745. Use it only to audit or correct clinical metadata, not as an independent test for shared cases.
5. Lock the endpoint definition and gene/probe mapping. Then decide whether the current score has enough pre-specified evidence to retain. Any change must be versioned as a new candidate, not overwrite the v1 result.
6. If still scientifically justified, validate on a genuinely independent, compatible anti-PD-1 monotherapy cohort; compare against prevalence and simple baselines, report confidence intervals and calibration, and do not claim clinical utility without prospective/decision-impact evidence.

## Decision record
`STATUS := PRIMARY_SOURCE_AUDIT_PARTIAL`
`CURRENT_AUROC := 0.5208333333`
`SCORE_V1 := FROZEN`
`LOG1P_JUSTIFICATION := UNRESOLVED`
`ENDPOINT_REPRODUCIBILITY := UNRESOLVED`
`INDEPENDENT_VALIDATION := NOT_ESTABLISHED`
`CLINICAL_UTILITY := NOT_ESTABLISHED`
`PR_DISPOSITION := KEEP_DRAFT_AND_UNMERGED`

No claim is made that all primary sources or supplements have been fully downloaded; the remaining retrieval tasks above are explicit.
