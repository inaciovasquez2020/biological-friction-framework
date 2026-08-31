import argparse
import csv
import gzip
import json
import math
import re
from collections import defaultdict
from pathlib import Path

TARGETS = {
    "BIRC3": {"BIRC3", "ENSG00000023445"},
    "JUND": {"JUND", "ENSG00000130522"},
    "JUN": {"JUN", "ENSG00000177606"},
    "FOSL2": {"FOSL2", "ENSG00000075426"},
}

GSE259388_PATTERN = re.compile(
    r"(?:GSM\d+_)?(?P<clone>218|421)_(?P<treatment>siCTRL|siTAZ1|siTAZ2|siYAP1|siYAP2)_(?P<rep>[123])\.txt(?:\.gz)?$",
    re.IGNORECASE,
)


def _open_text(path):
    path = Path(path)
    if path.suffix == ".gz":
        return gzip.open(path, "rt", encoding="utf-8", newline="")
    return open(path, "r", encoding="utf-8", newline="")


def _canonical_gene(token):
    token = token.strip().strip('"')
    if token.startswith("ENSG"):
        token = token.split(".", 1)[0]
    upper = token.upper()
    for symbol, aliases in TARGETS.items():
        if upper in aliases:
            return symbol
    return None


def _to_float(token):
    try:
        value = float(token)
    except (TypeError, ValueError):
        return None
    return value if math.isfinite(value) else None


def read_target_values(path):
    """Read one normalized-count table and return the four target values.

    The parser deliberately makes few format assumptions: a target may appear as a
    gene symbol or versioned/unversioned Ensembl id anywhere in a row, but exactly
    one finite numeric value must remain on that row. Ambiguous rows fail closed.
    """
    found = {}
    with _open_text(path) as handle:
        reader = csv.reader(handle, delimiter="\t")
        for row in reader:
            if not row or (row[0].startswith("#") if row else False):
                continue
            symbols = {_canonical_gene(cell) for cell in row}
            symbols.discard(None)
            if not symbols:
                continue
            assert len(symbols) == 1, f"ambiguous target-gene row in {path}: {row}"
            symbol = next(iter(symbols))
            numeric = [value for cell in row if (value := _to_float(cell)) is not None]
            assert len(numeric) == 1, (
                f"expected exactly one normalized numeric value for {symbol} in {path}; "
                f"found {len(numeric)}"
            )
            assert symbol not in found, f"duplicate target gene {symbol} in {path}"
            found[symbol] = numeric[0]

    missing = sorted(set(TARGETS) - set(found))
    assert not missing, f"missing target genes in {path}: {missing}"
    return found


def _mean(values):
    assert values, "cannot average empty values"
    return sum(values) / len(values)


def _ratio_record(control_values, treated_values):
    control = _mean(control_values)
    treated = _mean(treated_values)
    return {
        "control_mean": control,
        "treated_mean": treated,
        "ratio": (treated + 1.0) / (control + 1.0),
        "log2_ratio_pseudocount1": math.log2((treated + 1.0) / (control + 1.0)),
        "n_control": len(control_values),
        "n_treated": len(treated_values),
    }


def analyze_gse259388(samples_dir):
    grouped = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    matched_files = []
    for path in sorted(Path(samples_dir).iterdir()):
        match = GSE259388_PATTERN.search(path.name)
        if not match:
            continue
        clone = match.group("clone")
        treatment = match.group("treatment")
        values = read_target_values(path)
        matched_files.append(path.name)
        for gene, value in values.items():
            grouped[clone][treatment][gene].append(value)

    assert matched_files, "no GSE259388 matched sample files found"
    result = {}
    for clone in ("218", "421"):
        assert clone in grouped, f"missing clone {clone}"
        result[clone] = {}
        for treatment in ("siTAZ1", "siTAZ2", "siYAP1", "siYAP2"):
            assert treatment in grouped[clone], f"missing {clone} {treatment}"
            result[clone][treatment] = {}
            for gene in TARGETS:
                controls = grouped[clone]["siCTRL"][gene]
                treated = grouped[clone][treatment][gene]
                assert len(controls) == 3, f"expected 3 {clone} siCTRL replicates for {gene}"
                assert len(treated) == 3, f"expected 3 {clone} {treatment} replicates for {gene}"
                result[clone][treatment][gene] = _ratio_record(controls, treated)

    return {
        "dataset": "GSE259388",
        "status": "descriptive_only",
        "matched_files": matched_files,
        "contrasts": result,
        "interpretation_boundary": (
            "Normalized-count ratios are descriptive and do not establish differential-expression "
            "significance, mechanistic redundancy, or residual-survivor closure."
        ),
    }


def _read_wide_matrix(path):
    with _open_text(path) as handle:
        rows = list(csv.reader(handle, delimiter="\t"))
    assert rows and len(rows[0]) >= 2, "empty or malformed wide matrix"
    header = [cell.strip().strip('"') for cell in rows[0]]
    values = {gene: {} for gene in TARGETS}
    for row in rows[1:]:
        if not row:
            continue
        symbol = next((_canonical_gene(cell) for cell in row if _canonical_gene(cell)), None)
        if symbol is None:
            continue
        assert len(row) == len(header), f"row/header width mismatch for {symbol}"
        for column, cell in zip(header[1:], row[1:]):
            value = _to_float(cell)
            assert value is not None, f"non-numeric value for {symbol}/{column}"
            values[symbol][column] = value
    missing = sorted(gene for gene, data in values.items() if not data)
    assert not missing, f"missing target genes in matrix: {missing}"
    return values


def _infer_teadi_group(column):
    token = column.upper().replace(".", "").replace("-", "").replace("_", "")
    clone = "218" if "218" in token else "421" if "421" in token else None
    if "DMSO" in token:
        treatment = "DMSO"
    elif "9643" in token:
        treatment = "OPN9643"
    elif "9652" in token:
        treatment = "OPN9652"
    else:
        treatment = None
    return clone, treatment


def analyze_gse259389(matrix_path):
    values = _read_wide_matrix(matrix_path)
    grouped = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    for gene, columns in values.items():
        for column, value in columns.items():
            clone, treatment = _infer_teadi_group(column)
            if clone and treatment:
                grouped[clone][treatment][gene].append(value)

    result = {}
    for clone in ("218", "421"):
        result[clone] = {}
        for treatment in ("OPN9643", "OPN9652"):
            result[clone][treatment] = {}
            for gene in TARGETS:
                controls = grouped[clone]["DMSO"][gene]
                treated = grouped[clone][treatment][gene]
                assert len(controls) >= 3, f"need >=3 {clone} DMSO replicates for {gene}"
                assert len(treated) >= 3, f"need >=3 {clone} {treatment} replicates for {gene}"
                result[clone][treatment][gene] = _ratio_record(controls, treated)

    return {
        "dataset": "GSE259389",
        "status": "descriptive_only",
        "contrasts": result,
        "interpretation_boundary": (
            "Normalized-count ratios are descriptive and do not establish differential-expression "
            "significance, mechanistic redundancy, or residual-survivor closure."
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--gse259388-dir", type=Path)
    group.add_argument("--gse259389-matrix", type=Path)
    args = parser.parse_args()

    if args.gse259388_dir:
        result = analyze_gse259388(args.gse259388_dir)
    else:
        result = analyze_gse259389(args.gse259389_matrix)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
