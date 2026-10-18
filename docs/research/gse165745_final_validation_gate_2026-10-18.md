# GSE165745 final validation gate — 2026-10-18

## Decision

**STOP: research-only prototype; clinical validation not established. Keep PR #100 unmerged.**

This is a bounded validation gate, not a claim that the source-level audit is complete. The fixed score is implemented and its existing CI evaluation ran, but available evidence does not justify clinical use.

## Verified facts

- GEO identifies GSE165745 as a NanoString nCounter Vantage 3D Human Wnt Pathways Panel study of pretreatment metastatic melanoma FFPE samples, with 24 samples: 12 responders and 12 nonresponders.
- GEO lists `GSE165745_RAW.tar` as a 90.0 KB TAR of RCC files.
- The linked DeVito et al. paper reports group-level differences in Wnt ligands/receptors/regulators and reports panel-wide Benjamini–Yekutieli correction for its differential-expression analysis. That does not validate this repo's fixed composite score.
- The current fixed-score CI result is AUROC 0.5208333333333334 for nonresponse on the same 24 cases. This is near chance and is not evidence of useful discrimination.
- GSE280470 is a 39-sample follow-up/reanalysis cohort that includes previously published GSE165745 samples with updated clinical data. It must not be treated as independent validation until sample overlap is explicitly reconciled.

## Not established

- Exact nSolver normalization settings, background correction, housekeeping/reference-gene treatment, and transformation used to produce the displayed GEO values.
- Whether applying `log1p` to the deposited GEO `VALUE` scale is justified.
- A locked decision threshold suitable for future patients. The midpoint of the observed score range is in-sample and descriptive only.
- Patient-level reconciliation across GSE165745 and GSE280470, including updated response endpoint definitions and timing.
- Independent-cohort performance, calibration, clinical utility, or patient-care safety.

## Source retrieval and workflow status

The repository contains a source-inventory workflow intended to download series matrices and raw RCC archives, hash them, inventory RCC XML structure, and upload a report even if a source fails. Parser/failure-handling tests were added to that workflow. The available GitHub connector in this audit session did not expose the push-triggered source-inventory run or its artifact, and outbound network access from the execution container failed at DNS resolution. Therefore **the inventory workflow's download and RCC parsing outcome is not verified here**. This limitation is recorded rather than filled with assumptions.

The article's supplementary Tables S1/S2 are identified by the paper but were not successfully extracted and reconciled in this pass. No claim is made that the original preprocessing or sample-level crosswalk has been reconstructed.

## Final recommendation

Do not tune the fixed score on GSE165745. Do not use it to guide treatment. Do not call it a validated clinical prediction tool. Keep the implementation as an explicitly exploratory research prototype and preserve the near-chance result.

Further work should resume only if the actual RCC/supplementary source artifacts and reliable clinical crosswalk can be obtained. If those inputs remain inaccessible or lack the required preprocessing/endpoint information, the correct scientific outcome is a documented blocked/negative validation—not another model fit.
