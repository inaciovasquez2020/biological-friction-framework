# Melanoma Wnt input-audit implementation follow-up — 2026-10-18

## Work completed

Added `infra/ci/audit_melanoma_wnt_inputs.py` and `tests/test_melanoma_wnt_input_audit.py` to PR #100's existing research branch.

The utility:
- inventories candidate RCC/GZ files recursively and records SHA-256 hashes;
- hashes and structurally inspects supported Table S2 tabular formats, while marking unsupported formats as hash-only;
- refuses to infer cohort independence from nonmatching IDs unless a shared patient-identity crosswalk has been verified;
- refuses score calculation unless expression scale/preprocessing and sample/response mapping are explicitly marked verified;
- refuses to silently omit required genes, replace a missing RNF43 value with zero, or apply log1p to negative values.

## Source facts confirmed in public records

- GSE165745 is a 24-sample NanoString Wnt-panel cohort: R001–R012 are responders and NR001–NR012 are nonresponders. GEO lists a 90.0 KB `GSE165745_RAW.tar` archive containing RCC files. The individual GEO sample pages expose processed values labelled “Gene conts”; these values include fractional numbers, so they must not be described as untouched integer counts.
- GEO's sample processing text says the samples were analyzed on the NanoString nCounter Max with the nCounter Vantage 3D Human Wnt Pathways Panel and analysis was performed using nSolver. This does not, by itself, specify the exact normalization/transformation settings used for the deposited values.
- GSE280470 lists 39 samples and a 150.0 KB RCC archive. Its series description explicitly says it includes previously published GSE165745 samples with updated clinical data. Thus, it is not an independent validation cohort unless a patient-level crosswalk resolves overlap.
- The 2021 DeVito et al. paper supports group-level Wnt pathway differences and identifies Tables S1/S2 as associated with its analyses. The exact contents and hashes of the supplement files have not been captured in this audit.

## Important limitations

- The remote RCC archive and the supplementary PDF were not downloaded or parsed in this execution. No raw-to-deposited numerical reconciliation has been completed.
- The new unit tests were committed but have not been run by CI: no workflow run was returned for the test commit. Do not describe these tests as passing.
- No score was recalculated, no transformation was selected, and no clinical validity claim was added.
- The existing 24-sample AUROC of 0.5208 remains a near-chance descriptive result, not evidence of a usable clinical prediction tool.

## Gate decision

**BLOCKED — input provenance and cohort crosswalk remain unresolved.** The new utility is a guardrail for a later local/source-data audit; it is not itself evidence that the underlying data have passed validation.
