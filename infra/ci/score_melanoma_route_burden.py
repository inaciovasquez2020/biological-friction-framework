import argparse
import csv
import gzip
import json
import math
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


def _open_text(path):
    path = Path(path)
    if path.suffix == ".gz":
        return gzip.open(path, "rt", encoding="utf-8", newline="")
    return open(path, "r", encoding="utf-8", newline="")


def _to_float(token):
    try:
        value = float(token)
    except (TypeError, ValueError):
        return None
    return value if math.isfinite(value) else None


def _canonical_gene(token):
    return token.strip().strip('"').upper()


def read_wide_expression_matrix(path):
    """Read gene-by-sample TSV/TSV.GZ without any outcome/clinical columns.

    The first column is a gene symbol and every remaining column is one sample.
    Non-finite non-route expression values are ignored for that sample's percentile
    reference distribution. Every frozen route gene must occur exactly once and be
    finite in every scored sample.
    """
    with _open_text(path) as handle:
        rows = list(csv.reader(handle, delimiter="\t"))

    if not rows or len(rows[0]) < 2:
        raise ValueError("expression matrix must contain a gene column and >=1 sample")

    samples = [cell.strip().strip('"') for cell in rows[0][1:]]
    if any(not sample for sample in samples) or len(set(samples)) != len(samples):
        raise ValueError("sample names must be non-empty and unique")

    by_sample = {sample: [] for sample in samples}
    route_values = {sample: {} for sample in samples}
    seen_genes = set()

    for row_number, row in enumerate(rows[1:], start=2):
        if not row or all(not cell.strip() for cell in row):
            continue
        if len(row) != len(samples) + 1:
            raise ValueError(f"row {row_number} width does not match header")

        gene = _canonical_gene(row[0])
        if not gene:
            raise ValueError(f"row {row_number} has empty gene symbol")
        if gene in seen_genes:
            raise ValueError(f"duplicate gene symbol: {gene}")
        seen_genes.add(gene)

        for sample, token in zip(samples, row[1:]):
            value = _to_float(token)
            if value is not None:
                by_sample[sample].append(value)
            if gene in ROUTE_DIRECTIONS:
                if value is None:
                    raise ValueError(f"non-finite route value for {gene}/{sample}")
                route_values[sample][gene] = value

    missing = sorted(set(ROUTE_DIRECTIONS) - seen_genes)
    if missing:
        raise ValueError(f"missing frozen route genes: {missing}")

    for sample in samples:
        if not by_sample[sample]:
            raise ValueError(f"sample {sample} has no finite expression values")
        missing_sample = sorted(set(ROUTE_DIRECTIONS) - set(route_values[sample]))
        if missing_sample:
            raise ValueError(f"sample {sample} missing route values: {missing_sample}")

    return samples, by_sample, route_values


def within_sample_percentile(values, target):
    """Empirical midrank percentile frozen by the route-burden definition."""
    finite = [value for value in values if math.isfinite(value)]
    if not finite or not math.isfinite(target):
        raise ValueError("percentile requires finite values and finite target")
    less = sum(value < target for value in finite)
    equal = sum(value == target for value in finite)
    if equal == 0:
        raise ValueError("target must be present in the sample expression values")
    return (less + 0.5 * equal) / len(finite)


def score_sample(values, route_values):
    percentiles = {
        gene: within_sample_percentile(values, route_values[gene])
        for gene in ROUTE_DIRECTIONS
    }
    spokes = {
        gene: (1.0 - percentiles[gene] if direction == "low" else percentiles[gene])
        for gene, direction in ROUTE_DIRECTIONS.items()
    }
    burden = max(spokes.values())
    response_score = 1.0 - burden
    return {
        "route_percentiles": percentiles,
        "signed_spokes": spokes,
        "route_burden": burden,
        "s_pd1": response_score,
    }


def score_matrix(path):
    samples, by_sample, route_values = read_wide_expression_matrix(path)
    return {
        "status": "outcome_blind_score_only",
        "feature_version": "MELANOMA_ROUTE_BURDEN_PREDICTIVE_FEATURE_2026_09_06",
        "route_directions": ROUTE_DIRECTIONS,
        "samples": {
            sample: score_sample(by_sample[sample], route_values[sample])
            for sample in samples
        },
        "claim_boundary": (
            "Scores are frozen outcome-blind route-proxy features only; they do not establish "
            "predictive validity, treatment selection, clinical efficacy, or cure."
        ),
    }


def main():
    parser = argparse.ArgumentParser(
        description="Compute frozen melanoma malignant-route burden scores from a gene-by-sample TSV."
    )
    parser.add_argument("matrix", type=Path)
    args = parser.parse_args()
    print(json.dumps(score_matrix(args.matrix), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
