# Melanoma CD36 cell-resolved validation: cohort feasibility audit (2026-11-15)

**STATUS: SOURCE_AUDIT_PASS / STRUCTURAL_PREFLIGHT_IMPLEMENTED / PATIENT_LEVEL_VALIDATION_OPEN**

## Research target

Determine whether melanoma-cell CD36 and macrophage CD36 carry distinguishable, out-of-cohort evidence about anti-PD-1 response. **Do not** refit the frozen seven-marker route-burden v2 predictor. Treat any cell-resolved successor as a new exploratory model with its own preregistration and external validation.

## Verified source inventory

1. **Chakraborty et al., Genome Medicine, published 2026-11-03**: https://doi.org/10.1186/s13073-026-01794-9 . The study integrates immune-only Sade-Feldman scRNA-seq (32 patients), 19 Tirosh melanoma tumors including malignant and macrophage cells, an independent six-patient spatial cohort (three ICI responders and three nonresponders), and bulk-RNA validation (N=334). It reports lipid-associated tumor-associated macrophages (LA-TAMs), CD36 among lipid scavenging markers, and response-associated immune neighborhoods. These cohorts have **different patient groups and experimental roles**: their counts must not be pooled or treated as one matched patient-level malignant/immune/response dataset.
2. **Di Pietro et al., Nature Communications (2026)**: https://doi.org/10.1038/s41467-026-74076-y . GEO GSE294273 https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE294273 contains 12 public processed single-cell samples (4 untreated, 4 ICI-resistant, 4 ICI-responsive); the source article additionally reports other experimental modalities and clinical cohorts. Controlled access applies to raw identifiable sequencing data. The GEO groups alone do not certify pretreatment anti-PD-1 monotherapy sampling, independent patients, CD36 tumor/macrophage cell types, or the CR/PR-vs-PD endpoint.
3. **Frozen BFF v2**: `docs/status/MELANOMA_GSE91061_V2_EXTERNAL_VALIDATION_2026_10_18.md` reports AUROC 0.4913043478 and failure of the original independent validation gate. No new dataset can retroactively promote it.

## What is actually solved

The mathematical mixture theorem and exact rational tests are in `docs/status/MELANOMA_CD36_CELL_SOURCE_IDENTIFIABILITY_2026_11_15.md` and `tests/test_cell_source_identifiability.py`.

A **new structural gate** now lives at `infra/ci/melanoma_cd36_preflight.py` with `tests/test_melanoma_cd36_preflight.py`. It admits only self-described:
- unique patient and sample identities (one pretreatment sample per patient per study);
- pretreatment anti-PD-1 monotherapy and CR/PR-or-PD endpoint;
- separate malignant/macrophage CD36 source identifiers and assay identifiers;
- explicitly asserted sample/endpoint/treatment/cell-label provenance.

The script reports deterministic JSON and exits code 2 on blocked manifests. Its PASS is **not independent authentication**: the `yes` values and `source_url` are caller-provided statements that still require separate manual/source-level verification. The gate does **not** estimate tumor-cell CD36, verify actual cell-type assignment, check expression-scale compatibility, perform predictive scoring, or validate any clinical claim.

### Bounded tests and resource policy

Run using only Python standard library, no dataset downloads:

```bash
python3 -B -m unittest discover -s tests -p 'test_melanoma_cd36_preflight.py' -v
```

Five synthetic regression tests passed in an isolated Python environment. CI on the new branch and Mac-authoritative reproduction are **NOT_RUN**. The tiny fixtures are invented test metadata, not patient records.

## OPEN: weakest required object

One publicly traceable, **pretreatment, patient-linked paired malignant/macrophage CD36 manifest** from an admissible anti-PD-1 monotherapy cohort, with verified response labels and adequate assay compatibility. A cohort may instead fail and be marked `INELIGIBLE`. In particular:

- The Sade-Feldman immune-cell cohort cannot by itself identify malignant-cell CD36.
- The Tirosh malignant/immune cohort cannot be assumed to carry the same treatment-response labels as a separate Sade-Feldman cohort.
- GSE294273 requires sample-to-patient and treatment-timing metadata before its cell-resolved output can be called a pretreatment response cohort.
- Bulk transcriptomic deconvolution is an inferred quantity, not direct paired cell-type measurement.
- Normalized scRNA counts/TPM/FPKM cannot automatically be used as linear signal fractions or combined with the frozen v2 Cuffnorm FPKM reference.

## Next bounded actions

1. Inspect author-released sample manifests and supplement for an exact within-patient malignant/macrophage linkage, anti-PD-1 monotherapy, pretreatment time, and CR/PR/PD outcomes.
2. Produce a source-cited patient/sample crosswalk and assay/annotation manifest **without reading response scores**.
3. Run the structural preflight; manually authenticate every `yes` against primary metadata.
4. Independently assess cell-source and assay scale compatibility; if any required field is missing, stop with `BLOCKED`.
5. Only then preregister a new source-aware feature and independent patient-level evaluation.

```text
PRIMARY_SOURCE_AUDIT := PASS
MANIFEST_PREFLIGHT_TESTS := COMPUTATION_PASS_SYNTHETIC
REMOTE_EXACT_HEAD_CI := NOT_RUN
MATCHED_PRETREATMENT_CELL_RESOLVED_COHORT := NOT_ESTABLISHED
CLINICAL_MODEL_VALIDATION := OPEN
FROZEN_V2_PREDICTOR := UNCHANGED
```
