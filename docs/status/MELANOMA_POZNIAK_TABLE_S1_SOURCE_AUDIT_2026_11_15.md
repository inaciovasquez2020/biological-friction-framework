# Poźniak Table S1 retrieval and endpoint-method audit (2026-11-15)

**Status: PRIMARY DATA CATALOG INSPECTED / PATIENT TABLE NOT_RETRIEVED / FROZEN RESPONSE CROSSWALK OPEN**

## Source inventory inspected in this round

1. Original published article: Poźniak et al., *Cell* 187 (2024), 166–183.e25, DOI https://doi.org/10.1016/j.cell.2023.11.037 ; accessible primary article page https://www.cell.com/article/S0092867423013223/pdf . The study encompasses anti-PD-1 monotherapy and combination treatment, with both pretreatment and early on-treatment biopsies.
2. KU Leuven RDR, V8 dataset DOI https://doi.org/10.48804/GSAXBN . The dataset description explicitly identifies **Table S1 of the paper** as the full clinical metadata source.
3. Author analysis source https://github.com/MarineLab/Pozniak-et-al_TCF4_paper : `GC_ALL.R` uses `read_excel("/Meta_data_GEX_RESPONSE_2.0-25-08-2021.xlsx")` (line 660); `GC_ALL_MALIGNANT.R` line 196; `MALIGNANT_BT.R` line 149. These scripts confirm a metadata join but **do not provide the workbook contents or a validated RECIST/SD/PD crosswalk**.
4. KU Leuven RDR V8 lists `Pozniak_README_v6.txt`, 2.1 KB, file-id 224838, MD5 `0223b9fe806db07797246e6542083c0a`, with public catalog preview at https://rdr.kuleuven.be/file.xhtml?fileId=224838&toolType=PREVIEW&version=8.0 . The preview landing page displays metadata but did not expose its text to the audit. A direct retrieval was not accomplished. **Do not claim that README was read.**
5. RDR catalog also lists 2.5 GB `Entire_TME.rds` and 824.4 MB `Malignant_cells.rds`. Neither was downloaded. There is no need to download before verifying the small clinical metadata table.
6. Secondary integrated single-cell dataset publication https://pmc.ncbi.nlm.nih.gov/articles/PMC11754430/ describes binary `Combined_outcome` labels `Favourable/Unfavourable`, not a patient-resolved RECIST CR/PR/SD/PD table. These labels cannot recover the distinctions required by the BFF frozen endpoint.

## Decisive endpoint-method issue

Even an apparently admissible `response = CR` may represent **pathological complete response** rather than RECIST v1.1 complete response. The original study describes differing assessment rules for some surgically resected patients. A string-only CR/PR/PD gate is therefore insufficient.

The structural manifest preflight `infra/ci/melanoma_cd36_preflight.py` now requires a nonempty `endpoint_method` field equal to `RECIST_v1.1`, rejecting the `pathologic_response` category. Synthetic regression examples were added to `tests/test_melanoma_cd36_preflight.py`.

**Important:** This gate only checks claimed text; an unverified manifest can lie. A PASS is not independent confirmation of endpoint method. Clinical eligibility demands an auditable original row-to-identifier source crosswalk.

## Exact current obstruction

We cannot provide individual `patient_id, biopsy_id, regimen, timepoint, RECIST category` rows from the reviewed primary-source material. Therefore we cannot certify any positive number of matched eligible patients; the source-based upper bound of 15 in `MELANOMA_POZNIAK_PATIENT_CROSSWALK_BOUND_2026_11_15.md` remains in force.

The appropriate small-data route is the journal's original supplementary **Table S1** (or the original referenced Excel workbook with verified provenance). Inspect that table before any multi-gigabyte sequencing transfer or predictor scoring.

```text
ORIGINAL_RDR_V8_CATALOG := INSPECTED
README_V6_METADATA := INSPECTED
README_V6_CONTENT := NOT_RETRIEVED
ORIGINAL_TABLE_S1_ROWS := NOT_RETRIEVED
PATIENT_RECIST_CROSSWALK := OPEN
ENDPOINT_METHOD_GATE := IMPLEMENTED
NEW_GATE_EXACT_HEAD_TESTS := NOT_RUN
PATIENT_LEVEL_EXPRESSION_ANALYSIS := NOT_RUN
FROZEN_V2 := UNCHANGED
CLINICAL_VALIDATION := OPEN
```
