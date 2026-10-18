#!/usr/bin/env python3
"""Outcome-blind source and signature audit for the ITM PC4 melanoma dataset.

This utility does not score the frozen route-burden model, fit a model, or run survival
analysis. It checks input identity, cohort accounting, and overlap between supplied PC4
signatures and the seven frozen route markers.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

ROUTE_DIRECTIONS = {
    "KDM5B": "high",
    "CD36": "high",
    "MITF": "high",
    "MTHFD2": "high",
    "NGFR": "high",
    "NT5E": "high",
    "SOX10": "low",
}
PC4_DIRECTIONS = {"positive", "negative"}


def _delimiter(path: Path) -> str:
    return "\t" if path.suffix.lower() in {".tsv", ".tab"} else ","


def _read_dicts(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle, delimiter=_delimiter(path))
        if not reader.fieldnames:
            raise ValueError(f"{path}: missing header")
        return [{str(k).strip(): (v or "").strip() for k, v in row.items()} for row in reader]


def read_expression_inventory(path: Path) -> tuple[list[str], set[str]]:
    """Read the gene-by-sample header and first-column gene symbols, not expression values."""
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle, delimiter=_delimiter(path))
        try:
            header = next(reader)
        except StopIteration as exc:
            raise ValueError("expression matrix is empty") from exc
        if len(header) < 2:
            raise ValueError("expression matrix requires a gene column and at least one sample")
        samples = [value.strip().strip('"') for value in header[1:]]
        if any(not value for value in samples) or len(samples) != len(set(samples)):
            raise ValueError("expression matrix sample IDs must be non-empty and unique")
        genes: set[str] = set()
        for line_number, row in enumerate(reader, start=2):
            if not row or all(not value.strip() for value in row):
                continue
            if len(row) != len(header):
                raise ValueError(f"expression matrix row {line_number} width differs from header")
            gene = row[0].strip().strip('"').upper()
            if not gene:
                raise ValueError(f"expression matrix row {line_number} has an empty gene symbol")
            if gene in genes:
                raise ValueError(f"duplicate gene symbol in expression matrix: {gene}")
            genes.add(gene)
    return samples, genes


def read_signature(path: Path) -> dict[str, str]:
    rows = _read_dicts(path)
    if not rows:
        raise ValueError("signature file has no rows")
    required = {"gene_symbol", "pc4_direction"}
    if not required.issubset(rows[0]):
        raise ValueError("signature file requires gene_symbol and pc4_direction columns")
    signature: dict[str, str] = {}
    for row in rows:
        gene = row["gene_symbol"].upper()
        direction = row["pc4_direction"].lower()
        if not gene:
            raise ValueError("signature contains an empty gene symbol")
        if direction not in PC4_DIRECTIONS:
            raise ValueError(f"{gene}: pc4_direction must be positive or negative")
        if gene in signature:
            raise ValueError(f"duplicate signature gene: {gene}")
        signature[gene] = direction
    return signature


def read_sample_manifest(path: Path, sample_column: str, patient_column: str) -> list[dict[str, str]]:
    rows = _read_dicts(path)
    if not rows:
        raise ValueError("sample manifest has no rows")
    if not {sample_column, patient_column}.issubset(rows[0]):
        raise ValueError(
            f"manifest requires columns {sample_column!r} and {patient_column!r}"
        )
    seen: set[str] = set()
    for row in rows:
        sample = row[sample_column]
        patient = row[patient_column]
        if not sample or not patient:
            raise ValueError("manifest sample and patient IDs must be non-empty")
        if sample in seen:
            raise ValueError(f"duplicate sample ID in manifest: {sample}")
        seen.add(sample)
    return rows


def audit(
    matrix_path: Path,
    signature_path: Path,
    manifest_path: Path,
    sample_column: str = "sample_id",
    patient_column: str = "patient_id",
    expected_positive_genes: int = 36,
    expected_negative_genes: int = 56,
) -> dict:
    samples, matrix_genes = read_expression_inventory(matrix_path)
    signature = read_signature(signature_path)
    manifest = read_sample_manifest(manifest_path, sample_column, patient_column)

    matrix_ids = set(samples)
    manifest_ids = {row[sample_column] for row in manifest}
    patients_by_sample = {row[sample_column]: row[patient_column] for row in manifest}
    patients = set(patients_by_sample.values())

    positive = {gene for gene, direction in signature.items() if direction == "positive"}
    negative = {gene for gene, direction in signature.items() if direction == "negative"}
    route_genes = set(ROUTE_DIRECTIONS)
    matrix_signature = set(signature) & matrix_genes
    route_in_matrix = route_genes & matrix_genes
    exact_overlap = route_genes & set(signature)
    direction_consistent = {
        gene for gene in exact_overlap
        if (ROUTE_DIRECTIONS[gene] == "high" and signature[gene] == "positive")
        or (ROUTE_DIRECTIONS[gene] == "low" and signature[gene] == "negative")
    }
    direction_conflict = exact_overlap - direction_consistent

    counts_by_patient: dict[str, int] = {}
    for patient in patients_by_sample.values():
        counts_by_patient[patient] = counts_by_patient.get(patient, 0) + 1

    return {
        "audit_version": "ITM_PC4_ROUTE_OVERLAP_AUDIT_V1",
        "inputs": {
            "matrix": str(matrix_path),
            "signature": str(signature_path),
            "manifest": str(manifest_path),
        },
        "cohort_accounting": {
            "matrix_sample_columns": len(samples),
            "manifest_rows": len(manifest),
            "matrix_samples_missing_manifest": sorted(matrix_ids - manifest_ids),
            "manifest_samples_missing_matrix": sorted(manifest_ids - matrix_ids),
            "unique_patients_in_manifest": len(patients),
            "patients_with_multiple_aois": {
                patient: count for patient, count in sorted(counts_by_patient.items()) if count > 1
            },
            "sample_manifest_matrix_identity_pass": matrix_ids == manifest_ids,
        },
        "signature_accounting": {
            "signature_gene_count": len(signature),
            "pc4_positive_gene_count": len(positive),
            "pc4_negative_gene_count": len(negative),
            "expected_pc4_positive_gene_count": expected_positive_genes,
            "expected_pc4_negative_gene_count": expected_negative_genes,
            "signature_size_gate_pass": (
                len(positive) == expected_positive_genes
                and len(negative) == expected_negative_genes
            ),
            "signature_genes_present_in_matrix": len(matrix_signature),
            "signature_genes_absent_from_matrix": sorted(set(signature) - matrix_genes),
        },
        "frozen_route_overlap": {
            "route_marker_count": len(route_genes),
            "route_markers_present_in_matrix": sorted(route_in_matrix),
            "route_markers_absent_from_matrix": sorted(route_genes - matrix_genes),
            "exact_route_pc4_overlap": sorted(exact_overlap),
            "direction_consistent_overlap": sorted(direction_consistent),
            "direction_conflict_overlap": sorted(direction_conflict),
            "route_marker_pc4_assignment": {
                gene: {
                    "frozen_route_direction": ROUTE_DIRECTIONS[gene],
                    "pc4_direction": signature.get(gene),
                    "present_in_matrix": gene in matrix_genes,
                }
                for gene in sorted(route_genes)
            },
        },
        "decision": {
            "input_identity_gate_pass": matrix_ids == manifest_ids,
            "signature_size_gate_pass": (
                len(positive) == expected_positive_genes
                and len(negative) == expected_negative_genes
            ),
            "ready_for_signature_overlap_interpretation": (
                matrix_ids == manifest_ids
                and len(positive) == expected_positive_genes
                and len(negative) == expected_negative_genes
            ),
            "frozen_v2_scoring_performed": False,
            "survival_analysis_performed": False,
            "claim_boundary": (
                "Signature overlap is descriptive only. This audit does not establish "
                "biological equivalence, prognosis, anti-PD-1 response prediction, clinical "
                "utility, treatment selection, efficacy, or cure. Do not score log2CPM data "
                "with the frozen FPKM ECDF reference."
            ),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--matrix", type=Path, required=True, help="gene-by-AOI CSV/TSV matrix")
    parser.add_argument("--signature", type=Path, required=True, help="gene_symbol,pc4_direction CSV/TSV")
    parser.add_argument("--manifest", type=Path, required=True, help="sample_id,patient_id CSV/TSV")
    parser.add_argument("--sample-column", default="sample_id")
    parser.add_argument("--patient-column", default="patient_id")
    parser.add_argument("--expected-positive-genes", type=int, default=36)
    parser.add_argument("--expected-negative-genes", type=int, default=56)
    parser.add_argument("--output", type=Path, help="optional JSON receipt path")
    args = parser.parse_args()

    result = audit(
        args.matrix,
        args.signature,
        args.manifest,
        sample_column=args.sample_column,
        patient_column=args.patient_column,
        expected_positive_genes=args.expected_positive_genes,
        expected_negative_genes=args.expected_negative_genes,
    )
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
