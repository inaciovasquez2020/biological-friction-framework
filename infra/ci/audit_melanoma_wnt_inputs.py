#!/usr/bin/env python3
"""Fail-closed input audit for the research-only GSE165745 Wnt candidate.

This utility does not download data, infer patient identity, normalize expression,
or establish clinical validity. It records file provenance and refuses to score
unless the caller explicitly supplies evidence that the expression scale and
sample/response mapping have been resolved.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd

RESISTANCE_GENES = (
    "WNT2B", "WNT5A", "WNT7B", "WNT8B", "FZD1", "FZD2", "FZD4",
    "FZD5", "FZD7", "FZD8", "FZD10", "LRP5", "LRP6", "DKK2",
    "SFRP2", "SFRP4", "PYGO1", "DVL1",
)
REFERENCE_GENE = "RNF43"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def inventory_files(root: Path, suffixes: Iterable[str] = (".rcc", ".gz")) -> list[dict]:
    """Recursively inventory candidate raw files, including hashes."""
    if not root.is_dir():
        raise FileNotFoundError(f"Not a directory: {root}")
    normalized = {suffix.lower() for suffix in suffixes}
    records = []
    for path in sorted(p for p in root.rglob("*") if p.is_file()
                       and any(p.name.lower().endswith(s) for s in normalized)):
        records.append({
            "relative_path": str(path.relative_to(root)),
            "size_bytes": path.stat().st_size,
            "sha256": sha256_file(path),
        })
    return records


def inspect_table(path: Path) -> dict:
    """Hash a supplement and inspect supported tabular formats without guessing."""
    if not path.is_file():
        raise FileNotFoundError(f"Table file not found: {path}")
    suffix = path.suffix.lower()
    result = {"path": str(path), "size_bytes": path.stat().st_size,
              "sha256": sha256_file(path), "format": suffix}
    if suffix in {".xlsx", ".xls"}:
        book = pd.ExcelFile(path)
        result["sheets"] = book.sheet_names
        frame = pd.read_excel(path, sheet_name=0)
    elif suffix in {".csv", ".tsv", ".txt"}:
        sep = "\t" if suffix in {".tsv", ".txt"} else ","
        frame = pd.read_csv(path, sep=sep)
    else:
        result["parse_status"] = "hash_only_unsupported_format"
        return result
    result.update({
        "parse_status": "parsed",
        "rows": int(frame.shape[0]),
        "columns": int(frame.shape[1]),
        "column_names": [str(c) for c in frame.columns],
    })
    return result


def reconcile_ids(
    first_ids: Iterable[str],
    second_ids: Iterable[str],
    *,
    identity_crosswalk_verified: bool,
) -> dict:
    """Compare IDs only when they are known to be canonical, shared identifiers."""
    a = {str(x).strip() for x in first_ids if pd.notna(x) and str(x).strip()}
    b = {str(x).strip() for x in second_ids if pd.notna(x) and str(x).strip()}
    overlap = sorted(a & b)
    if not identity_crosswalk_verified:
        status = "unresolved_identifier_crosswalk"
    elif overlap:
        status = "overlap_detected"
    else:
        status = "no_overlap_detected_under_verified_crosswalk"
    return {
        "n_unique_first": len(a),
        "n_unique_second": len(b),
        "overlap_ids": overlap,
        "status": status,
        "independence_established": status == "no_overlap_detected_under_verified_crosswalk",
    }


def calculate_frozen_score(
    expression: pd.DataFrame,
    *,
    gene_column: str = "Gene",
    scale_verified: bool = False,
    sample_mapping_verified: bool = False,
    transform: str = "none",
) -> pd.Series:
    """Calculate the frozen score only after source-scale and sample mapping gates pass.

    Input is a long-form table: one gene per row and one numeric column per sample.
    No genes are silently dropped; no missing RNF43 value is replaced with zero.
    """
    if not scale_verified:
        raise ValueError("Blocked: expression scale/preprocessing has not been verified.")
    if not sample_mapping_verified:
        raise ValueError("Blocked: sample IDs and response labels have not been verified.")
    if transform not in {"none", "log1p"}:
        raise ValueError("transform must be 'none' or 'log1p'; no automatic selection.")
    if gene_column not in expression.columns:
        raise ValueError(f"Missing gene identifier column: {gene_column}")
    genes = expression[gene_column].astype(str)
    if genes.duplicated().any():
        duplicates = sorted(genes[genes.duplicated(keep=False)].unique())
        raise ValueError(f"Duplicate gene rows require explicit resolution: {duplicates}")
    required = list(RESISTANCE_GENES) + [REFERENCE_GENE]
    present = set(genes)
    missing = [gene for gene in required if gene not in present]
    if missing:
        raise ValueError(f"Blocked: required genes missing: {missing}")
    sample_columns = [c for c in expression.columns if c != gene_column]
    if not sample_columns:
        raise ValueError("No sample expression columns found.")
    values = expression.set_index(gene_column)[sample_columns].apply(
        pd.to_numeric, errors="raise"
    )
    if not np.isfinite(values.to_numpy(dtype=float)).all():
        raise ValueError("Expression matrix contains NaN or infinite values.")
    if transform == "log1p":
        if (values < 0).any().any():
            raise ValueError("log1p blocked: negative expression values are present.")
        values = np.log1p(values)
    score = values.loc[list(RESISTANCE_GENES)].mean(axis=0) - values.loc[REFERENCE_GENE]
    score.name = "frozen_wnt_score"
    return score


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rcc-dir", type=Path)
    parser.add_argument("--table-s2", type=Path)
    parser.add_argument("--output", type=Path, default=Path("melanoma_wnt_input_audit.json"))
    args = parser.parse_args()
    report: dict = {
        "purpose": "research-only input provenance audit",
        "clinical_use": False,
        "score_recalculated": False,
        "gates": {
            "expression_scale_verified": False,
            "sample_response_crosswalk_verified": False,
            "independent_validation_established": False,
        },
    }
    if args.rcc_dir:
        files = inventory_files(args.rcc_dir)
        report["rcc_inventory"] = {
            "root": str(args.rcc_dir),
            "count": len(files),
            "files": files,
            "status": "inventory_only_not_raw_vs_processed_reconciliation",
        }
    if args.table_s2:
        report["table_s2"] = inspect_table(args.table_s2)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
