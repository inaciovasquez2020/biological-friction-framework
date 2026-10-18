# GSE165745 validation gate follow-up — 2026-10-18

Status: BLOCKED, research-only.

- Current fixed score: mean(log1p of 18 Wnt-associated genes) minus log1p(RNF43), as implemented in `infra/ci/develop_melanoma_wnt_v1.py`.
- Existing result: AUROC 0.5208333333 for nonresponse, n=24; near chance.
- GEO GSE165745 contains 24 labeled samples and links RCC files, but exact nSolver normalization and endpoint criteria remain unresolved.
- GEO GSE280470 explicitly includes previously published GSE165745 samples with updated clinical data. Do not treat the 39 samples as an independent validation cohort until overlap is mapped.
- The score is biologically motivated by group-level findings in DeVito et al., but it is not the paper's validated classifier. The exact composite score and cutoff are not validated.
- Source inventory workflow exists, but no completed artifact was available in the current audit. Do not claim raw archives or supplementary Tables S1/S2 have been extracted.

Next required evidence: (1) source-level Table S2 and preprocessing details; (2) checksummed series matrix and RCC archive inventory; (3) exact sample/clinical crosswalk between GSE165745 and GSE280470; (4) only then, unchanged-score reproduction. No tuning on the 24 cases. Keep PR #100 draft/unmerged; no clinical use.

Sources: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE165745 ; https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE280470 ; https://pmc.ncbi.nlm.nih.gov/articles/PMC8148423/