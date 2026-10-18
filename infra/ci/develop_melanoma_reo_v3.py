#!/usr/bin/env python3
"""Develop and externally test a seven-gene REO melanoma response candidate.

Development uses only Liu/DFCI mel_dfci_2019. The locked external cohort is
GSE91061 pretreatment, using the already frozen CR/PR-versus-PD endpoint.
This is research-only and must not be used for treatment decisions.
"""
from __future__ import annotations

import csv
import gzip
import hashlib
import importlib.util
import io
import json
import math
import random
import tempfile
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PREFLIGHT_PATH = ROOT / "preflight_mel_dfci_v2_cohort.py"
VALIDATION_PATH = ROOT / "validate_gse91061_melanoma_v2.py"

LIU_BASE = (
    "https://media.githubusercontent.com/media/cBioPortal/datahub/"
    "7a4b4ec142f76ac04db22834232b23142d25bd2a/public/mel_dfci_2019/"
)
LIU_FILES = {
    "patient": "data_clinical_patient.txt",
    "sample": "data_clinical_sample.txt",
    "expression": "data_mrna_seq_tpm.txt",
}
GSE91061_SERIES_URL = (
    "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE91nnn/GSE91061/"
    "matrix/GSE91061_series_matrix.txt.gz"
)
GSE91061_FPKM_URL = (
    "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE91nnn/GSE91061/"
    "suppl/GSE91061_BMS038109Sample.hg19KnownGene.fpkm.csv.gz"
)
GENES = ("KDM5B", "CD36", "MITF", "MTHFD2", "NGFR", "NT5E", "SOX10")
ENTREZ_TO_SYMBOL = {
    "10765": "KDM5B",
    "948": "CD36",
    "4286": "MITF",
    "10797": "MTHFD2",
    "4804": "NGFR",
    "4907": "NT5E",
    "6663": "SOX10",
}
PAIRS = tuple((GENES[i], GENES[j]) for i in range(len(GENES)) for j in range(i + 1, len(GENES)))
RIDGE_LAMBDA = 1.0
BOOTSTRAP_ITERATIONS = 10000
BOOTSTRAP_SEED = 20261018
MODEL_VERSION = "MELANOMA_SEVEN_GENE_REO_RIDGE_V3_2026_10_18"


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load repository module: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


PREFLIGHT = _load_module("reo_v3_dfci_preflight", PREFLIGHT_PATH)
VALIDATION = _load_module("reo_v3_gse91061_validation", VALIDATION_PATH)


def download(url: str) -> tuple[bytes, str]:
    request = urllib.request.Request(url, headers={"User-Agent": MODEL_VERSION})
    with urllib.request.urlopen(request, timeout=120) as response:
        data = response.read()
    if not data:
        raise RuntimeError(f"empty download: {url}")
    return data, hashlib.sha256(data).hexdigest()


def _liu_data():
    raw = {}
    for key, filename in LIU_FILES.items():
        raw[key], _ = download(LIU_BASE + filename)

    _, patient_rows = PREFLIGHT.parse_cbio_tsv(raw["patient"], "patient clinical")
    _, sample_rows = PREFLIGHT.parse_cbio_tsv(raw["sample"], "sample clinical")
    patient_by_id = {
        row.get("PATIENT_ID", "").strip(): row
        for row in patient_rows
        if row.get("PATIENT_ID", "").strip()
    }
    sample_by_id = {
        row.get("SAMPLE_ID", "").strip(): row
        for row in sample_rows
        if row.get("SAMPLE_ID", "").strip()
    }

    text = raw["expression"].decode("utf-8-sig")
    reader = csv.reader(io.StringIO(text), delimiter="\t")
    header = next(reader)
    if len(header) < 3:
        raise ValueError("Liu expression matrix lacks gene identifiers or sample columns")
    sample_ids = [item.strip() for item in header[2:]]
    if not sample_ids or len(set(sample_ids)) != len(sample_ids):
        raise ValueError("Liu expression sample IDs are empty or duplicated")
    wanted = set(GENES)
    matrix = {}
    for line_number, row in enumerate(reader, start=2):
        if not row:
            continue
        if len(row) != len(header):
            raise ValueError(f"Liu expression row {line_number} has incorrect width")
        gene = row[0].strip()
        if gene not in wanted:
            continue
        if gene in matrix:
            raise ValueError(f"duplicate Liu expression row for {gene}")
        values = []
        for sample, token in zip(sample_ids, row[2:]):
            try:
                value = float(token)
            except ValueError as exc:
                raise ValueError(f"non-numeric Liu TPM for {gene}/{sample}") from exc
            if not math.isfinite(value) or value < 0:
                raise ValueError(f"invalid Liu TPM for {gene}/{sample}")
            values.append(value)
        matrix[gene] = dict(zip(sample_ids, values))
    missing = sorted(wanted - set(matrix))
    if missing:
        raise ValueError(f"Liu matrix is missing required genes: {missing}")

    observations = []
    for sample_id in sample_ids:
        sample = sample_by_id.get(sample_id)
        if sample is None:
            raise ValueError(f"Liu expression sample lacks clinical sample row: {sample_id}")
        patient_id = sample.get("PATIENT_ID", "").strip()
        patient = patient_by_id.get(patient_id)
        if patient is None:
            raise ValueError(f"Liu sample lacks patient clinical row: {sample_id}")
        response = patient.get("BR", "").strip()
        endpoint = PREFLIGHT.classify_response(response)
        if endpoint == "RESPONDER_CR_PR":
            y = 1
        elif endpoint == "NONRESPONDER_PD":
            y = 0
        else:
            continue
        observations.append({
            "sample_id": sample_id,
            "patient_id": patient_id,
            "response_source": response,
            "y": y,
            "expression": {gene: matrix[gene][sample_id] for gene in GENES},
        })

    patient_ids = [row["patient_id"] for row in observations]
    if len(set(patient_ids)) != len(patient_ids):
        raise ValueError("Liu endpoint contains multiple expression samples per patient")
    class_counts = {str(y): sum(row["y"] == y for row in observations) for y in (0, 1)}
    if len(observations) != 103 or class_counts != {"0": 56, "1": 47}:
        raise ValueError(
            "Liu frozen endpoint changed: "
            f"n={len(observations)}, class_counts={class_counts}; expected n=103, 47 CR/PR, 56 PD"
        )
    return observations, {key: hashlib.sha256(value).hexdigest() for key, value in raw.items()}


def _gse91061_data():
    series_gz, series_sha = download(GSE91061_SERIES_URL)
    series_raw = gzip.decompress(series_gz) if series_gz[:2] == b"\x1f\x8b" else series_gz
    metadata = VALIDATION.parse_series_matrix(series_raw.decode("utf-8"))
    selected, dedup_exclusions = VALIDATION.freeze_pretreatment(metadata)

    fpkm_gz, fpkm_sha = download(GSE91061_FPKM_URL)
    with tempfile.TemporaryDirectory() as directory:
        route_path = Path(directory) / "gse91061_route.tsv"
        matrix_info = VALIDATION.build_route_tsv(fpkm_gz, set(metadata), route_path)
        with route_path.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.reader(handle, delimiter="\t")
            header = next(reader)
            samples = header[1:]
            by_gene = {}
            for row in reader:
                by_gene[row[0]] = {sample: float(value) for sample, value in zip(samples, row[1:])}

    observations = []
    exclusions = list(dedup_exclusions)
    for record in selected:
        y, endpoint_name = VALIDATION.endpoint(record["response"])
        if y is None:
            exclusions.append({
                "sample_id": record["sample_id"],
                "patient_id": record["patient_id"],
                "response": record["response"],
                "reason": endpoint_name,
            })
            continue
        sample_id = record["sample_id"]
        if sample_id not in samples:
            raise ValueError(f"GSE91061 sample missing from expression matrix: {sample_id}")
        observations.append({
            "sample_id": sample_id,
            "patient_id": record["patient_id"],
            "response_source": record["response"],
            "y": y,
            "expression": {gene: by_gene[gene][sample_id] for gene in GENES},
        })

    class_counts = {str(y): sum(row["y"] == y for row in observations) for y in (0, 1)}
    if len(observations) != 33 or class_counts != {"0": 23, "1": 10}:
        raise ValueError(
            "GSE91061 locked endpoint changed: "
            f"n={len(observations)}, class_counts={class_counts}; expected n=33, 10 CR/PR, 23 PD"
        )
    return observations, {
        "series_matrix_compressed_sha256": series_sha,
        "fpkm_compressed_sha256": fpkm_sha,
        **matrix_info,
    }, exclusions


def pair_features(expression: dict[str, float]) -> list[float]:
    if set(expression) != set(GENES):
        raise ValueError("expression record must contain exactly the frozen seven genes")
    if not all(math.isfinite(float(expression[g])) for g in GENES):
        raise ValueError("expression record contains non-finite values")
    return [1.0 if expression[a] > expression[b] else 0.0 for a, b in PAIRS]


def sigmoid(value: float) -> float:
    if value >= 0:
        return 1.0 / (1.0 + math.exp(-value))
    exp_value = math.exp(value)
    return exp_value / (1.0 + exp_value)


def _solve_linear(matrix: list[list[float]], vector: list[float]) -> list[float]:
    n = len(vector)
    augmented = [list(matrix[i]) + [float(vector[i])] for i in range(n)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda row: abs(augmented[row][col]))
        if abs(augmented[pivot][col]) < 1e-12:
            raise ValueError("singular Newton system in ridge logistic fit")
        augmented[col], augmented[pivot] = augmented[pivot], augmented[col]
        scale = augmented[col][col]
        augmented[col] = [value / scale for value in augmented[col]]
        for row in range(n):
            if row == col:
                continue
            factor = augmented[row][col]
            if factor != 0.0:
                augmented[row] = [
                    augmented[row][j] - factor * augmented[col][j]
                    for j in range(n + 1)
                ]
    return [augmented[i][-1] for i in range(n)]


def _objective(x: list[list[float]], y: list[int], beta: list[float], penalty: float) -> float:
    total = 0.5 * penalty * sum(value * value for value in beta[1:])
    for row, label in zip(x, y):
        eta = sum(a * b for a, b in zip(row, beta))
        softplus = eta + math.log1p(math.exp(-eta)) if eta >= 0 else math.log1p(math.exp(eta))
        total += softplus - label * eta
    return total


def fit_ridge_logistic(features: list[list[float]], labels: list[int], penalty: float = RIDGE_LAMBDA):
    if len(features) != len(labels) or len(labels) < 5:
        raise ValueError("features and labels must align and contain at least five samples")
    if any(label not in (0, 1) for label in labels) or len(set(labels)) != 2:
        raise ValueError("ridge logistic fit requires both binary endpoint classes")
    width = len(PAIRS)
    if any(len(row) != width for row in features):
        raise ValueError(f"every feature row must have {width} pair features")

    means = [sum(row[j] for row in features) / len(features) for j in range(width)]
    scales = []
    for j, mean in enumerate(means):
        variance = sum((row[j] - mean) ** 2 for row in features) / len(features)
        scales.append(math.sqrt(variance) if variance > 1e-12 else 1.0)
    standardized = [
        [1.0] + [(row[j] - means[j]) / scales[j] for j in range(width)]
        for row in features
    ]
    beta = [math.log(sum(labels) / (len(labels) - sum(labels)))] + [0.0] * width

    converged = False
    iteration = 0
    for iteration in range(1, 101):
        probabilities = [sigmoid(sum(a * b for a, b in zip(row, beta))) for row in standardized]
        dimension = width + 1
        gradient = [0.0] * dimension
        hessian = [[0.0] * dimension for _ in range(dimension)]
        for row, label, probability in zip(standardized, labels, probabilities):
            residual = probability - label
            weight = probability * (1.0 - probability)
            for i in range(dimension):
                gradient[i] += residual * row[i]
                for j in range(dimension):
                    hessian[i][j] += weight * row[i] * row[j]
        for j in range(1, dimension):
            gradient[j] += penalty * beta[j]
            hessian[j][j] += penalty
        if max(abs(value) for value in gradient) < 1e-7:
            converged = True
            break
        step = _solve_linear(hessian, gradient)
        old_objective = _objective(standardized, labels, beta, penalty)
        step_size = 1.0
        accepted = False
        while step_size >= 1e-8:
            candidate = [beta[i] - step_size * step[i] for i in range(dimension)]
            if _objective(standardized, labels, candidate, penalty) <= old_objective + 1e-12:
                beta = candidate
                accepted = True
                break
            step_size *= 0.5
        if not accepted:
            if max(abs(value) for value in gradient) < 1e-5:
                converged = True
                break
            raise ValueError("ridge logistic line search failed to decrease objective")
    if not converged:
        probabilities = [sigmoid(sum(a * b for a, b in zip(row, beta))) for row in standardized]
        gradient_norm = max(
            abs(sum((p - y_i) * row[j] for p, y_i, row in zip(probabilities, labels, standardized))
                + (penalty * beta[j] if j > 0 else 0.0))
            for j in range(width + 1)
        )
        if gradient_norm >= 1e-5:
            raise ValueError(f"ridge logistic fit did not converge: gradient={gradient_norm}")

    return {
        "intercept": beta[0],
        "coefficients": beta[1:],
        "feature_means": means,
        "feature_scales": scales,
        "ridge_lambda": penalty,
        "iterations": iteration,
        "converged": True,
        "standardization": "training mean and population SD; constant feature SD set to 1",
    }


def predict_probability(features: list[list[float]], model: dict) -> list[float]:
    output = []
    for row in features:
        if len(row) != len(model["coefficients"]):
            raise ValueError("prediction feature width differs from model")
        standardized = [
            (row[j] - model["feature_means"][j]) / model["feature_scales"][j]
            for j in range(len(row))
        ]
        eta = model["intercept"] + sum(
            value * coefficient for value, coefficient in zip(standardized, model["coefficients"])
        )
        output.append(sigmoid(eta))
    return output


def auc(labels: list[int], scores: list[float]) -> float:
    positive = [score for label, score in zip(labels, scores) if label == 1]
    negative = [score for label, score in zip(labels, scores) if label == 0]
    if not positive or not negative:
        raise ValueError("AUROC requires both endpoint classes")
    wins = sum(1.0 if p > n else 0.5 if p == n else 0.0 for p in positive for n in negative)
    return wins / (len(positive) * len(negative))


def stratified_auc_ci(labels: list[int], scores: list[float]) -> dict:
    positive = [score for label, score in zip(labels, scores) if label == 1]
    negative = [score for label, score in zip(labels, scores) if label == 0]
    rng = random.Random(BOOTSTRAP_SEED)
    values = []
    for _ in range(BOOTSTRAP_ITERATIONS):
        bp = [rng.choice(positive) for _ in positive]
        bn = [rng.choice(negative) for _ in negative]
        values.append(auc([1] * len(bp) + [0] * len(bn), bp + bn))
    values.sort()
    def quantile(p):
        position = p * (len(values) - 1)
        lo, hi = math.floor(position), math.ceil(position)
        if lo == hi:
            return values[lo]
        return values[lo] * (hi - position) + values[hi] * (position - lo)
    return {
        "method": "stratified patient bootstrap",
        "iterations": BOOTSTRAP_ITERATIONS,
        "seed": BOOTSTRAP_SEED,
        "lower_95": quantile(0.025),
        "upper_95": quantile(0.975),
    }


def metrics(labels: list[int], probabilities: list[float]) -> dict:
    if len(labels) != len(probabilities) or not labels or len(set(labels)) != 2:
        raise ValueError("metrics require aligned samples and both classes")
    predictions = [int(probability >= 0.5) for probability in probabilities]
    tp = sum(y == 1 and p == 1 for y, p in zip(labels, predictions))
    fn = sum(y == 1 and p == 0 for y, p in zip(labels, predictions))
    tn = sum(y == 0 and p == 0 for y, p in zip(labels, predictions))
    fp = sum(y == 0 and p == 1 for y, p in zip(labels, predictions))
    sensitivity = tp / (tp + fn)
    specificity = tn / (tn + fp)
    prevalence = sum(labels) / len(labels)
    brier = sum((p - y) ** 2 for p, y in zip(probabilities, labels)) / len(labels)
    prevalence_brier = prevalence * (1.0 - prevalence)
    interval = stratified_auc_ci(labels, probabilities)
    return {
        "n": len(labels),
        "responders": sum(labels),
        "nonresponders": len(labels) - sum(labels),
        "prevalence": prevalence,
        "auroc": auc(labels, probabilities),
        "auroc_95_ci": interval,
        "balanced_accuracy_at_0_5": 0.5 * (sensitivity + specificity),
        "sensitivity_at_0_5": sensitivity,
        "specificity_at_0_5": specificity,
        "brier": brier,
        "prevalence_only_brier": prevalence_brier,
        "brier_beats_prevalence_baseline": brier < prevalence_brier,
    }


def run_development() -> dict:
    training, training_hashes = _liu_data()
    validation, validation_sources, exclusions = _gse91061_data()
    train_features = [pair_features(row["expression"]) for row in training]
    train_labels = [row["y"] for row in training]
    test_features = [pair_features(row["expression"]) for row in validation]
    test_labels = [row["y"] for row in validation]

    model = fit_ridge_logistic(train_features, train_labels)
    train_probabilities = predict_probability(train_features, model)
    test_probabilities = predict_probability(test_features, model)
    train_metrics = metrics(train_labels, train_probabilities)
    test_metrics = metrics(test_labels, test_probabilities)
    external_overlap = sorted(set(row["patient_id"] for row in training) & set(row["patient_id"] for row in validation))
    if external_overlap:
        raise ValueError(f"patient IDs overlap across development and validation: {external_overlap}")

    return {
        "status": "REO_V3_DEVELOPMENT_AND_LOCKED_EXTERNAL_TEST_COMPLETE",
        "model_version": MODEL_VERSION,
        "model_type": "ridge logistic regression over all 21 within-sample orderings among the frozen seven genes",
        "genes": list(GENES),
        "pairs": [{"gene_a": a, "gene_b": b, "feature": f"{a}>{b}"} for a, b in PAIRS],
        "training_cohort": {
            "name": "Liu/DFCI mel_dfci_2019",
            "source_commit": "7a4b4ec142f76ac04db22834232b23142d25bd2a",
            "expression_unit": "TPM",
            "source_sha256": training_hashes,
            "endpoint": "CR/PR versus PD; SD/mixed/unknown excluded",
            "metrics": train_metrics,
            "sample_count": len(training),
            "patient_ids": sorted(row["patient_id"] for row in training),
        },
        "external_validation_cohort": {
            "name": "GSE91061 pretreatment",
            "expression_unit": "GEO FPKM",
            "source": validation_sources,
            "endpoint": "CR/PR versus PD; SD/unknown/mixed excluded",
            "metrics": test_metrics,
            "sample_count": len(validation),
            "patient_ids": sorted(row["patient_id"] for row in validation),
            "exclusions": exclusions,
            "patient_overlap_with_training": external_overlap,
        },
        "model_parameters": model,
        "external_promotion_screen": {
            "auroc_point_estimate_gt_0_5": test_metrics["auroc"] > 0.5,
            "auroc_ci_lower_gt_0_5": test_metrics["auroc_95_ci"]["lower_95"] > 0.5,
            "brier_better_than_prevalence_baseline": test_metrics["brier_beats_prevalence_baseline"],
            "balanced_accuracy_gt_0_5": test_metrics["balanced_accuracy_at_0_5"] > 0.5,
            "passed_single_cohort_screen": (
                test_metrics["auroc"] > 0.5
                and test_metrics["auroc_95_ci"]["lower_95"] > 0.5
                and test_metrics["brier_beats_prevalence_baseline"]
                and test_metrics["balanced_accuracy_at_0_5"] > 0.5
            ),
            "second_independent_replication": False,
        },
        "patients": {
            "training": [
                {"sample_id": row["sample_id"], "patient_id": row["patient_id"], "y": row["y"],
                 "probability": probability}
                for row, probability in zip(training, train_probabilities)
            ],
            "external_validation": [
                {"sample_id": row["sample_id"], "patient_id": row["patient_id"], "y": row["y"],
                 "probability": probability}
                for row, probability in zip(validation, test_probabilities)
            ],
        },
        "scale_robustness_note": (
            "Pairwise features are invariant to a common positive multiplicative scale factor within a "
            "sample, which is why TPM and FPKM can be considered for an REO model. This does not prove "
            "cross-pipeline equivalence: annotation, transcript-to-gene aggregation, and quantification "
            "can alter within-sample gene orderings."
        ),
        "claim_boundary": (
            "Research-stage candidate only. GSE91061 is one small locked external cohort. No clinical "
            "utility, treatment-selection benefit, prospective validity, or patient outcome improvement "
            "is established. Do not use this output to select or withhold therapy. Even a passed screen "
            "requires independent replication and clinical-utility evaluation."
        ),
    }


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Develop and test the seven-gene melanoma REO v3 candidate.")
    parser.add_argument("--output", type=Path, default=Path("melanoma_reo_v3_receipt.json"))
    args = parser.parse_args()
    result = run_development()
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "model_version": result["model_version"],
        "training_metrics": result["training_cohort"]["metrics"],
        "external_validation_metrics": result["external_validation_cohort"]["metrics"],
        "external_promotion_screen": result["external_promotion_screen"],
        "receipt": str(args.output),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
