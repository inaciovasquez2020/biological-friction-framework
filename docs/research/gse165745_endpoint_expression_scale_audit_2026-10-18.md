# GSE165745 endpoint and expression-scale audit (2026-10-18)

## Evidence reviewed

- GEO series GSE165745 identifies 24 FFPE metastatic melanoma samples, 12 labeled responders and 12 nonresponders, measured before anti-PD-1 treatment using the NanoString nCounter Vantage 3D Human Wnt Pathways Panel plus custom immune markers. The series cites PMID 33951424.
- GEO sample records state analysis was performed with NanoString nSolver. The public records also expose processed per-sample VALUE tables and supplementary RCC files.
- The associated paper, “Pharmacological Wnt ligand inhibition overcomes key tumor-mediated resistance pathways to anti-PD-1 immunotherapy,” reports Wnt ligands/FZD receptors and selected pathway components higher in nonresponders, and RNF43 higher in responders. The paper describes false-discovery-rate correction for its panel-wide differential-expression analysis.
- GEO GSE280470 explicitly says it includes previously published GSE165745 samples with updated clinical data. Those overlapping samples are not an independent validation set.

## What is established

1. The deposited cohort is a small, balanced, pretreatment anti-PD-1 monotherapy cohort.
2. The pathway hypothesis has published biological support.
3. The fixed score's direction is inspired by the paper's reported group-level findings, but the exact composite score is not the published, validated classifier.
4. The current run's AUROC for nonresponse is 0.5208 on n=24. Preserve this result unchanged.

## Unresolved data contract

The current implementation applies `log1p` to the deposited values. The GEO descriptions establish use of nSolver but do not, in the inspected fields, specify the exact normalization steps, background correction, housekeeping/reference normalization, or whether the matrix values are already transformed. A GEO sample page labels its data table “Gene counts,” but that label alone does not establish that the values are untransformed counts. Therefore, `log1p` is not yet justified.

Before any score change, retrieve and inspect:
- all 24 sample-level processed values and the series matrix column alignment;
- the original paper's supplement (especially the exact per-gene differential-expression results and preprocessing details);
- the 24 RCC files or nSolver export if available, to establish whether the GEO VALUEs are raw, background-corrected, normalized, or transformed;
- the response definition and timing, including how response was classified and whether clinical updates in GSE280470 alter any original labels.

## Decision

`STATUS := ENDPOINT_AND_SCALE_AUDIT_PARTIAL`

`SCORE_CHANGE := NOT_AUTHORIZED`

`INDEPENDENT_VALIDATION := NOT_ESTABLISHED`

`CLINICAL_USE := NOT_SUPPORTED`

Do not tune the formula against these 24 samples. Do not treat GSE280470's overlapping GSE165745 cases as independent validation. Keep PR #100 as draft and unmerged until the data contract is resolved.
