# Poźniak auxiliary uploads: bulk expression and source documentation audit

Date: 2026-11-15
Status: **SOURCE_FILES_INSPECTED / BULK_TECHNICAL_AUDIT_PASS / PAIRED_PATIENT_CD36_OPEN**

## Exact uploaded inputs

| Uploaded file | Bytes | SHA-256 |
|---|---:|---|
| `Bulk_rna_raw_counts.tsv` | 6,897,879 | `a2512499371daa72eca94e720808a0ba40aa37db0c7575c17e6b25d5acaf0f87` |
| `Pozniak_README_v5.txt` | 2,128 | `4bc28f7609e417f74c9875ab8baa213423e6f08a7ec0735534fd653c90ad4945` |
| `Pozniak_README_v6.txt` | 2,170 | `53874d36a5d4587b42337d54261475344386038b6f68c4e430d220e1ba977346` |
| `spaceranger_scripts.txt` | 2,419 | `4fb30488ae75d55c7cbdb16bca5d4b8bb298a717baa2dd36f615a020914297c1` |

Full source files were user-supplied during this session; this repository note does not embed raw expression matrices.

## Bulk TSV technical audit

- 57,316 rows with unique gene identifiers; 18 experimental columns; all 1,031,688 numeric entries finite and nonnegative; zero malformed row widths.
- 267,520 entries have noninteger values, so the name `raw_counts` must **not** be taken as proof of literal integer read counts. The generating/quantification pipeline and replicate provenance remain unverified.
- All seven frozen-marker genes are present: KDM5B, CD36, MITF, MTHFD2, NGFR, NT5E and SOX10. Also present: CD68, CD163, LST1 and TYROBP. Gene presence is **not** evidence of a macrophage compartment in these bulk experimental columns.
- Column names describe experimental perturbations of MaMel, MM011 and MM099 systems (NT, Doxy+, DMSO, ARV, siSCR, siTCF4). None are labeled with the `GCxx` clinical patient identifiers from `data/pozzniak_clinical_keys_2026_11_15.csv`. No specimen-to-patient linkage has been authenticated.
- Column-wise total reported quantities range approximately 12,567,452.826 to 43,970,663.117. This alone is not an assay normalization or cell-source deconvolution.

**Purely descriptive CD36 quantities**, computed as `10^6 * CD36_column_value / sum_all_genes_in_column` (NOT FPKM, TPM, validated CPM, biological fold changes or clinical response features):

| Group | Number of columns | Range per million reported quantities |
|---|---:|---:|
| MaMel_NT | 2 | 6.118–6.144 |
| MaMel_Doxy+ | 2 | 3.628–3.731 |
| MM011_NT | 3 | 0.071–0.577 |
| MM011_Doxy+ | 3 | 0.131–0.986 |
| MM099_DMSO | 2 | 0.462–0.660 |
| MM099_ARV | 2 | 0–0.080 |
| MM099_siSCR | 2 | 0.797–1.537 |
| MM099_siTCF4 | 2 | 1.393–1.728 |

Do not assign significance or experimental replicability without experimental design, batch information and preprocessing specification. This TSV is not evidence that paired patient-level malignant/macrophage expression is available.

## Readme comparison and spatial scripts

- The v5 and v6 READMEs differ in their G07 descriptions: v6 additionally mentions Space Ranger count outputs. Both describe malignant cell count matrices with `Malignant_clusters` metadata and an entire-TME matrix; both document patient ID, sample ID, BT/OT timepoint and grouped response in the malignant RDS. These statements describe files not included in the current upload.
- The Space Ranger scripts list six spatial runs with `refdata-gex-GRCh38-2020-A`, `--localcores=8`, and `--localmem=64`. These are processing commands, not proof of successful execution or matched baseline single-cell annotation. No spatial output was uploaded.

## Decisions and next gate

1. Preserve `14` patient-level clinical eligibility records and the known exclusion of `scrCMA109` from the authors' malignant analysis script; neither establishes paired CD36 availability.
2. Do not score BFF v2 or fit a CD36 response predictor from cell-line bulk expression.
3. Before downloading large objects, obtain a compact, genuine exported Seurat/RDS metadata table showing `orig.ident`/patient, BT/OT, cell label (malignant/macrophage) and number of cells per matched biopsy. A source-authenticated pseudobulk CD36 extract would be sufficient for a first feasibility assessment; avoid re-hosting entire objects.
4. Confirm the exact count assay, cell annotation logic, and harmonization/normalization method. No clinical prediction, cellular-source correction, or immunotherapy effect is established by these uploads.

```text
BULK_FILE_HASHED_AND_PARSED := PASS
BULK_GENE_ROW_COUNT := 57316
BULK_EXPERIMENT_COLUMN_COUNT := 18
BULK_NONFINITE_VALUES := 0
BULK_FRACTIONAL_VALUES := 267520
BULK_CLINICAL_PATIENT_MATCH := NOT_ESTABLISHED
RDS_SINGLE_CELL_OBJECTS := NOT_UPLOADED
CELL_RESOLVED_PAIRED_CD36 := OPEN
PATIENT_LEVEL_PREDICTION := NOT_RUN
FROZEN_V2 := UNCHANGED
```
