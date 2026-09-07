import argparse
import csv
import json
import math
from pathlib import Path

FEATURE_VERSION = "MELANOMA_ROUTE_BURDEN_V2_DEFINITION_2026_09_06"
ROUTE_DIRECTIONS = {
    "KDM5B": "high",
    "CD36": "high",
    "MITF": "high",
    "MTHFD2": "high",
    "NGFR": "high",
    "NT5E": "high",
    "SOX10": "low",
}


def _finite_float(token):
    try:
        value = float(token)
    except (TypeError, ValueError):
        return None
    return value if math.isfinite(value) else None


def read_route_matrix(path):
    """Read only the frozen route genes from a gene-by-sample TSV."""
    with open(Path(path), "r", encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle, delimiter="\t")
        try:
            header = next(reader)
        except StopIteration as exc:
            raise ValueError("expression matrix is empty") from exc
        if len(header) < 2:
            raise ValueError("expression matrix requires gene column and >=1 sample")
        samples = [str(value).strip().strip('"') for value in header[1:]]
        if any(not sample for sample in samples) or len(set(samples)) != len(samples):
            raise ValueError("sample names must be non-empty and unique")

        route_rows = {}
        seen = set()
        for row_number, row in enumerate(reader, start=2):
            if not row or all(not str(cell).strip() for cell in row):
                continue
            if len(row) != len(header):
                raise ValueError(f"row {row_number} width does not match header")
            gene = str(row[0]).strip().strip('"').upper()
            if not gene:
                raise ValueError(f"row {row_number} has empty gene symbol")
            if gene in seen:
                raise ValueError(f"duplicate gene symbol: {gene}")
            seen.add(gene)
            if gene not in ROUTE_DIRECTIONS:
                continue
            values = []
            for sample, token in zip(samples, row[1:]):
                value = _finite_float(token)
                if value is None:
                    raise ValueError(f"non-finite route value for {gene}/{sample}")
                values.append(value)
            route_rows[gene] = dict(zip(samples, values))

    missing = sorted(set(ROUTE_DIRECTIONS) - set(route_rows))
    if missing:
        raise ValueError(f"missing frozen route genes: {missing}")
    return samples, route_rows


def fit_reference(path, reference_samples):
    """Fit v2 marker ECDF references from sample IDs only; no outcome input exists."""
    samples, route_rows = read_route_matrix(path)
    reference_samples = [str(sample) for sample in reference_samples]
    if not reference_samples or len(set(reference_samples)) != len(reference_samples):
        raise ValueError("reference_samples must be non-empty and unique")
    unknown = sorted(set(reference_samples) - set(samples))
    if unknown:
        raise ValueError(f"unknown reference samples: {unknown}")

    route_reference = {
        gene: sorted(route_rows[gene][sample] for sample in reference_samples)
        for gene in ROUTE_DIRECTIONS
    }
    return {
        "feature_version": FEATURE_VERSION,
        "reference_samples": reference_samples,
        "route_directions": dict(ROUTE_DIRECTIONS),
        "route_reference": route_reference,
        "claim_boundary": (
            "Outcome-blind development reference only; no predictive validity, treatment "
            "selection, efficacy, or cure is established."
        ),
    }


def ecdf_midrank(reference_values, value):
    reference = [float(item) for item in reference_values]
    if not reference or not all(math.isfinite(item) for item in reference):
        raise ValueError("ECDF reference must be non-empty and finite")
    value = float(value)
    if not math.isfinite(value):
        raise ValueError("ECDF query value must be finite")
    less = sum(item < value for item in reference)
    equal = sum(item == value for item in reference)
    return (less + 0.5 * equal) / len(reference)


def score_route_values(route_values, reference):
    if reference.get("feature_version") != FEATURE_VERSION:
        raise ValueError("reference feature version mismatch")
    if reference.get("route_directions") != ROUTE_DIRECTIONS:
        raise ValueError("reference route directions mismatch")
    route_reference = reference.get("route_reference", {})
    if set(route_reference) != set(ROUTE_DIRECTIONS):
        raise ValueError("reference does not contain exactly the frozen route genes")
    if set(route_values) != set(ROUTE_DIRECTIONS):
        raise ValueError("sample does not contain exactly the frozen route genes")

    ecdf = {
        gene: ecdf_midrank(route_reference[gene], route_values[gene])
        for gene in ROUTE_DIRECTIONS
    }
    spokes = {
        gene: (1.0 - ecdf[gene] if direction == "low" else ecdf[gene])
        for gene, direction in ROUTE_DIRECTIONS.items()
    }
    burden = sum(spokes.values()) / len(spokes)
    return {
        "route_ecdf": ecdf,
        "signed_spokes": spokes,
        "route_burden_v2": burden,
        "s_pd1_v2": 1.0 - burden,
    }


def score_matrix(path, reference, sample_ids=None):
    """Apply a previously frozen reference; this function never refits it."""
    samples, route_rows = read_route_matrix(path)
    if sample_ids is None:
        selected = list(samples)
    else:
        selected = [str(sample) for sample in sample_ids]
        if len(set(selected)) != len(selected):
            raise ValueError("sample_ids must be unique")
        unknown = sorted(set(selected) - set(samples))
        if unknown:
            raise ValueError(f"unknown scoring samples: {unknown}")

    result = {}
    for sample in selected:
        route_values = {gene: route_rows[gene][sample] for gene in ROUTE_DIRECTIONS}
        result[sample] = score_route_values(route_values, reference)
    return {
        "status": "frozen_v2_reference_applied",
        "feature_version": FEATURE_VERSION,
        "reference_samples": list(reference["reference_samples"]),
        "samples": result,
        "claim_boundary": (
            "Scores reuse a frozen development reference only; they do not establish predictive "
            "validity, treatment selection, efficacy, or cure."
        ),
    }


def main():
    parser = argparse.ArgumentParser(description="Fit/apply frozen melanoma route-burden v2 ECDF scorer.")
    sub = parser.add_subparsers(dest="command", required=True)

    fit = sub.add_parser("fit-reference")
    fit.add_argument("matrix", type=Path)
    fit.add_argument("--samples", required=True, help="comma-separated development reference sample IDs")

    score = sub.add_parser("score")
    score.add_argument("matrix", type=Path)
    score.add_argument("reference", type=Path)
    score.add_argument("--samples", help="optional comma-separated sample IDs")

    args = parser.parse_args()
    if args.command == "fit-reference":
        result = fit_reference(args.matrix, [item for item in args.samples.split(",") if item])
    else:
        reference = json.loads(args.reference.read_text(encoding="utf-8"))
        selected = None if not args.samples else [item for item in args.samples.split(",") if item]
        result = score_matrix(args.matrix, reference, selected)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
