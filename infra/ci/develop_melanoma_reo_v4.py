#!/usr/bin/env python3
"""Train a broad REO candidate on Liu/DFCI + Gide; test once on GSE93157 melanoma.

All gene-pair selection and model fitting use the two RNA-seq development cohorts.
GSE93157 is an untouched NanoString baseline cohort. This is research-only.
"""
from __future__ import annotations

import csv
import gzip
import hashlib
import io
import json
import math
import random
import urllib.request
from pathlib import Path

import numpy as np
from scipy.stats import fisher_exact

ROOT = Path(__file__).resolve().parent
PREFLIGHT_PATH = ROOT / "preflight_mel_dfci_v2_cohort.py"

LIU_BASE = (
    "https://media.githubusercontent.com/media/cBioPortal/datahub/"
    "7a4b4ec142f76ac04db22834232b23142d25bd2a/public/mel_dfci_2019/"
)
LIU_FILES = {
    "patient": "data_clinical_patient.txt",
    "sample": "data_clinical_sample.txt",
    "expression": "data_mrna_seq_tpm.txt",
}
GIDE_EXPRESSION_URL = (
    "https://raw.githubusercontent.com/xmuyulab/ims_gene_signature/"
    "275be3c340e4cba698d085bc1a875b92dd45602c/data/mel_gide19_exp_data.csv"
)
GIDE_PHENOTYPE_URL = (
    "https://raw.githubusercontent.com/Yun-Ching-Chen/NSCLC_ICB_CombBiomarker/"
    "1e9d8b62b7226425985a4f10e3ae1830cc176937/"
    "Data/Melanoma_Metastatic_PRJEB23709_Gide2019_pheno.csv"
)
GSE93157_MATRIX_URL = (
    "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE93nnn/GSE93157/"
    "matrix/GSE93157_series_matrix.txt.gz"
)
MODEL_VERSION = "MELANOMA_PANEL_REO_RIDGE_V4_2026_10_18"
RIDGE_LAMBDA = 1.0
MAX_SELECTED_PAIRS = 15
POOL_DELTA_MIN = 0.25
COHORT_DELTA_MIN = 0.10
MIN_CLASS_STABILITY = 0.75
FDR_MAX = 0.05
BOOTSTRAP_ITERATIONS = 10000
BOOTSTRAP_SEED = 20261018


def _load_preflight():
    import importlib.util
    spec = importlib.util.spec_from_file_location("reo_v4_dfci_preflight", PREFLIGHT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load Liu/DFCI clinical parser")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


PREFLIGHT = _load_preflight()


def download(url: str) -> tuple[bytes, str]:
    request = urllib.request.Request(url, headers={"User-Agent": MODEL_VERSION})
    with urllib.request.urlopen(request, timeout=120) as response:
        data = response.read()
    if not data:
        raise RuntimeError(f"empty download: {url}")
    return data, hashlib.sha256(data).hexdigest()


def _read_liu(wanted: set[str]):
    raw = {key: download(LIU_BASE + name) for key, name in LIU_FILES.items()}
    _, patient_rows = PREFLIGHT.parse_cbio_tsv(raw["patient"][0], "patient clinical")
    _, sample_rows = PREFLIGHT.parse_cbio_tsv(raw["sample"][0], "sample clinical")
    patient_by_id = {
        row.get("PATIENT_ID", "").strip(): row
        for row in patient_rows if row.get("PATIENT_ID", "").strip()
    }
    sample_by_id = {
        row.get("SAMPLE_ID", "").strip(): row
        for row in sample_rows if row.get("SAMPLE_ID", "").strip()
    }

    reader = csv.reader(io.StringIO(raw["expression"][0].decode("utf-8-sig")), delimiter="\t")
    header = next(reader)
    sample_ids = [token.strip() for token in header[2:]]
    if not sample_ids or len(set(sample_ids)) != len(sample_ids):
        raise ValueError("Liu sample columns are empty or duplicated")
    values_by_gene = {}
    for line_number, row in enumerate(reader, start=2):
        if not row:
            continue
        if len(row) != len(header):
            raise ValueError(f"Liu matrix row {line_number} width mismatch")
        gene = row[0].strip()
        if gene not in wanted:
            continue
        if gene in values_by_gene:
            raise ValueError(f"duplicate Liu gene row in target panel: {gene}")
        values = [float(token) for token in row[2:]]
        if not all(math.isfinite(value) and value >= 0 for value in values):
            raise ValueError(f"invalid Liu expression values for {gene}")
        values_by_gene[gene] = dict(zip(sample_ids, values))

    observations = []
    for sample_id in sample_ids:
        sample = sample_by_id.get(sample_id)
        if sample is None:
            raise ValueError(f"Liu expression sample lacks clinical sample row: {sample_id}")
        patient_id = sample.get("PATIENT_ID", "").strip()
        patient = patient_by_id.get(patient_id)
        if patient is None:
            raise ValueError(f"Liu sample lacks patient row: {sample_id}")
        response = patient.get("BR", "").strip()
        endpoint = PREFLIGHT.classify_response(response)
        if endpoint == "RESPONDER_CR_PR":
            y = 1
        elif endpoint == "NONRESPONDER_PD":
            y = 0
        else:
            continue
        observations.append({
            "cohort": "Liu_DFCI",
            "sample_id": sample_id,
            "patient_id": patient_id,
            "y": y,
            "expression": {gene: values_by_gene[gene][sample_id] for gene in values_by_gene},
        })

    if len(observations) != 103 or sum(row["y"] for row in observations) != 47:
        raise ValueError("Liu endpoint drifted from the frozen 103-patient CR/PR-versus-PD crosswalk")
    return observations, set(values_by_gene), {
        key: {"url": LIU_BASE + LIU_FILES[key], "sha256": value[1], "bytes": len(value[0])}
        for key, value in raw.items()
    }


def _read_gide(wanted: set[str]):
    exp_bytes, exp_sha = download(GIDE_EXPRESSION_URL)
    pheno_bytes, pheno_sha = download(GIDE_PHENOTYPE_URL)
    reader = csv.reader(io.StringIO(exp_bytes.decode("utf-8-sig")))
    header = next(reader)
    sample_ids = [token.strip() for token in header[1:]]
    if not sample_ids or len(set(sample_ids)) != len(sample_ids):
        raise ValueError("Gide expression sample IDs are empty or duplicated")
    values_by_gene = {}
    for line_number, row in enumerate(reader, start=2):
        if not row or all(not token.strip() for token in row):
            continue
        if len(row) != len(header):
            raise ValueError(f"Gide expression row {line_number} width mismatch")
        gene = row[0].strip()
        if gene not in wanted:
            continue
        if gene in values_by_gene:
            raise ValueError(f"duplicate Gide gene row in target panel: {gene}")
        values = [float(token) for token in row[1:]]
        if not all(math.isfinite(value) for value in values):
            raise ValueError(f"non-finite Gide expression values for {gene}")
        values_by_gene[gene] = dict(zip(sample_ids, values))

    phenotype_reader = csv.DictReader(io.StringIO(pheno_bytes.decode("utf-8-sig")))
    required = {"sid", "response", "Therapy", "biopsy_time", "pid"}
    if not phenotype_reader.fieldnames or not required.issubset(phenotype_reader.fieldnames):
        raise ValueError("Gide phenotype table lacks required accession/response/treatment fields")
    by_accession = {}
    for row in phenotype_reader:
        accession = row.get("sid", "").strip()
        if not accession or accession in by_accession:
            raise ValueError(f"empty or duplicate Gide accession: {accession!r}")
        by_accession[accession] = row

    observations = []
    pre_monotherapy = []
    for accession, row in by_accession.items():
        if row.get("Therapy", "").strip() != "anti-PD-1":
            continue
        if row.get("biopsy_time", "").strip() != "pre-treatment":
            continue
        pre_monotherapy.append(accession)
        response = row.get("response", "").strip().upper()
        if response in {"CR", "PR"}:
            y = 1
        elif response == "PD":
            y = 0
        else:
            continue
        if accession not in sample_ids:
            raise ValueError(f"Gide clinical accession lacks expression column: {accession}")
        observations.append({
            "cohort": "Gide_PRJEB23709",
            "sample_id": accession,
            "patient_id": row.get("pid", "").strip(),
            "y": y,
            "expression": {gene: values_by_gene[gene][accession] for gene in values_by_gene},
        })

    if len(pre_monotherapy) != 41 or len(observations) != 35:
        raise ValueError("Gide endpoint drifted from the frozen 41-row/35-included crosswalk")
    if sum(row["y"] for row in observations) != 19:
        raise ValueError("Gide responder count drifted from the frozen endpoint crosswalk")
    return observations, set(values_by_gene), {
        "expression_url": GIDE_EXPRESSION_URL,
        "expression_sha256": exp_sha,
        "expression_bytes": len(exp_bytes),
        "phenotype_url": GIDE_PHENOTYPE_URL,
        "phenotype_sha256": pheno_sha,
        "phenotype_bytes": len(pheno_bytes),
        "processing_note": "secondary processed expression matrix; within-sample gene ordering may be affected by quantile normalization",
    }


def _parse_geo_sample_fields(line: str) -> list[str]:
    return next(csv.reader([line], delimiter="\t"))[1:]


def _read_gse93157():
    compressed, source_sha = download(GSE93157_MATRIX_URL)
    raw = gzip.decompress(compressed) if compressed[:2] == b"\x1f\x8b" else compressed
    text = raw.decode("utf-8-sig")
    lines = text.splitlines()
    titles = source_names = None
    characteristics = []
    table_start = None
    for index, line in enumerate(lines):
        if line.startswith("!Sample_title\t"):
            titles = _parse_geo_sample_fields(line)
        elif line.startswith("!Sample_source_name_ch1\t"):
            source_names = _parse_geo_sample_fields(line)
        elif line.startswith("!Sample_characteristics_ch1\t"):
            characteristics.append(_parse_geo_sample_fields(line))
        elif line.strip() == "!series_matrix_table_begin":
            table_start = index + 1
            break
    if not titles or not source_names or table_start is None:
        raise ValueError("GSE93157 series matrix lacks sample metadata or expression table")
    if len(titles) != len(source_names) or any(len(row) != len(titles) for row in characteristics):
        raise ValueError("GSE93157 sample metadata dimensions do not align")

    metadata = []
    for i, title in enumerate(titles):
        fields = {}
        for row in characteristics:
            token = row[i].strip()
            if ":" in token:
                key, value = token.split(":", 1)
                key = " ".join(key.strip().lower().replace(".", " ").split())
                fields[key] = value.strip()
        metadata.append({
            "sample_id": title.strip(),
            "source_name": source_names[i].strip(),
            "fields": fields,
        })

    reader = csv.reader(io.StringIO("\n".join(lines[table_start:])), delimiter="\t")
    header = next(reader)
    if len(header) != len(titles) + 1:
        raise ValueError("GSE93157 expression table header does not match sample metadata")
    expression = {}
    for line_number, row in enumerate(reader, start=table_start + 2):
        if not row or row[0].strip() == "!series_matrix_table_end":
            break
        if len(row) != len(header):
            raise ValueError(f"GSE93157 expression row {line_number} width mismatch")
        gene = row[0].strip().strip('"')
        if not gene or gene in expression:
            raise ValueError(f"empty or duplicate GSE93157 gene identifier: {gene!r}")
        values = [float(token) for token in row[1:]]
        if not all(math.isfinite(value) for value in values):
            raise ValueError(f"non-finite GSE93157 expression values for {gene}")
        expression[gene] = dict(zip(titles, values))

    observations = []
    exclusions = []
    melanoma_baseline = []
    for sample in metadata:
        fields = sample["fields"]
        source = sample["source_name"].lower()
        cancer_type = fields.get("cancer type", fields.get("tumor type", "")).lower()
        if "melanoma" not in source and "melanoma" not in cancer_type:
            continue
        if fields.get("biopsy", "").strip().upper() != "BASELINE":
            continue
        if fields.get("drug", "").strip().upper() not in {"NIVOLUMAB", "ANTI-PD-1", "ANTI PD 1"}:
            continue
        melanoma_baseline.append(sample["sample_id"])
        response = fields.get("best resp", fields.get("best response", "")).strip().upper()
        if response in {"CR", "PR", "COMPLETE RESPONSE", "PARTIAL RESPONSE"}:
            y = 1
        elif response in {"PD", "PROGRESSIVE DISEASE"}:
            y = 0
        elif response in {"SD", "STABLE DISEASE"}:
            exclusions.append({"sample_id": sample["sample_id"], "response": response, "reason": "stable_disease_excluded"})
            continue
        else:
            exclusions.append({"sample_id": sample["sample_id"], "response": response, "reason": "unknown_or_unrecognized_response"})
            continue
        if sample["sample_id"] not in expression[next(iter(expression))]:
            raise ValueError(f"GSE93157 sample missing from expression matrix: {sample['sample_id']}")
        observations.append({
            "cohort": "GSE93157",
            "sample_id": sample["sample_id"],
            "patient_id": sample["sample_id"],
            "y": y,
            "expression": {gene: values[sample["sample_id"]] for gene, values in expression.items()},
            "response_source": response,
        })

    counts = {str(y): sum(row["y"] == y for row in observations) for y in (0, 1)}
    if len(observations) < 15 or counts["0"] < 5 or counts["1"] < 5:
        raise ValueError(
            "GSE93157 is too small for the prespecified external screen: "
            f"included={len(observations)}, class_counts={counts}, baseline_melanoma={len(melanoma_baseline)}"
        )
    return observations, set(expression), {
        "series_matrix_url": GSE93157_MATRIX_URL,
        "compressed_sha256": source_sha,
        "uncompressed_sha256": hashlib.sha256(raw).hexdigest(),
        "compressed_bytes": len(compressed),
        "uncompressed_bytes": len(raw),
        "baseline_melanoma_samples": melanoma_baseline,
        "excluded_endpoint_rows": exclusions,
        "class_counts": counts,
    }


def pair_features(expression: dict[str, float], selected_pairs: list[dict]) -> list[float]:
    result = []
    for pair in selected_pairs:
        a, b = pair["gene_a"], pair["gene_b"]
        if a not in expression or b not in expression:
            raise ValueError(f"sample missing selected pair gene: {a}, {b}")
        result.append(1.0 if expression[a] > expression[b] else 0.0)
    return result


def select_pairs(training, genes: list[str], cohort_deltas: dict, max_pairs: int = MAX_SELECTED_PAIRS):
    y = np.asarray([row["y"] for row in training], dtype=int)
    x = np.asarray([[row["expression"][gene] for gene in genes] for row in training], dtype=float)
    responders = y == 1
    nonresponders = y == 0
    liu = np.asarray([row["cohort"] == "Liu_DFCI" for row in training])
    gide = np.asarray([row["cohort"] == "Gide_PRJEB23709" for row in training])
    i_idx, j_idx = np.triu_indices(len(genes), k=1)
    total_pairs = len(i_idx)
    candidates = []

    for start in range(0, total_pairs, 5000):
        stop = min(start + 5000, total_pairs)
        ii, jj = i_idx[start:stop], j_idx[start:stop]
        ordered = x[:, ii] > x[:, jj]
        p_resp = ordered[responders].mean(axis=0)
        p_pd = ordered[nonresponders].mean(axis=0)
        delta = p_resp - p_pd
        p_resp_liu = ordered[liu & responders].mean(axis=0)
        p_pd_liu = ordered[liu & nonresponders].mean(axis=0)
        p_resp_gide = ordered[gide & responders].mean(axis=0)
        p_pd_gide = ordered[gide & nonresponders].mean(axis=0)
        delta_liu = p_resp_liu - p_pd_liu
        delta_gide = p_resp_gide - p_pd_gide
        stable = np.maximum.reduce([p_resp, 1 - p_resp, p_pd, 1 - p_pd])
        keep = (
            (np.abs(delta) >= POOL_DELTA_MIN)
            & (np.abs(delta_liu) >= COHORT_DELTA_MIN)
            & (np.abs(delta_gide) >= COHORT_DELTA_MIN)
            & (np.sign(delta_liu) == np.sign(delta_gide))
            & (np.sign(delta) == np.sign(delta_liu))
            & (stable >= MIN_CLASS_STABILITY)
        )
        for local in np.flatnonzero(keep):
            a, b = int(ii[local]), int(jj[local])
            a_resp = int(ordered[responders, local].sum())
            n_resp = int(responders.sum())
            a_pd = int(ordered[nonresponders, local].sum())
            n_pd = int(nonresponders.sum())
            p_value = float(fisher_exact([
                [a_resp, n_resp - a_resp],
                [a_pd, n_pd - a_pd],
            ], alternative="two-sided").pvalue)
            candidates.append({
                "gene_a": genes[a],
                "gene_b": genes[b],
                "delta_pooled": float(delta[local]),
                "delta_liu": float(delta_liu[local]),
                "delta_gide": float(delta_gide[local]),
                "p_resp_a_gt_b": float(p_resp[local]),
                "p_pd_a_gt_b": float(p_pd[local]),
                "p_value": p_value,
                "pair_index": start + local,
            })

    if not candidates:
        raise ValueError("NO_CROSS_COHORT_STABLE_GENE_PAIRS: no pair passed the prespecified effect/direction gate")
    ordered_p = np.argsort([item["p_value"] for item in candidates])
    adjusted = np.ones(len(candidates), dtype=float)
    running = 1.0
    for rank_index in range(len(ordered_p) - 1, -1, -1):
        original = int(ordered_p[rank_index])
        rank = rank_index + 1
        running = min(running, candidates[original]["p_value"] * total_pairs / rank)
        adjusted[original] = min(1.0, running)
    for item, fdr in zip(candidates, adjusted):
        item["fdr_bh_over_full_pair_family"] = float(fdr)
    qualifying = [item for item in candidates if item["fdr_bh_over_full_pair_family"] <= FDR_MAX]
    qualifying.sort(key=lambda item: (
        -abs(item["delta_pooled"]),
        item["fdr_bh_over_full_pair_family"],
        item["gene_a"],
        item["gene_b"],
    ))
    selected = qualifying[:max_pairs]
    if len(selected) < 3:
        raise ValueError(
            "TOO_FEW_CROSS_COHORT_STABLE_GENE_PAIRS: "
            f"only {len(selected)} pairs passed FDR/effect gates"
        )
    return selected, {
        "common_gene_count": len(genes),
        "tested_pair_count": total_pairs,
        "effect_prefilter_pair_count": len(candidates),
        "fdr_qualified_pair_count": len(qualifying),
        "selected_pair_count": len(selected),
        "selection_rules": {
            "pooled_abs_delta_min": POOL_DELTA_MIN,
            "per_cohort_abs_delta_min": COHORT_DELTA_MIN,
            "same_effect_direction_in_Liu_and_Gide": True,
            "minimum_class_ordering_stability": MIN_CLASS_STABILITY,
            "fdr_bh_max": FDR_MAX,
            "maximum_selected_pairs": max_pairs,
        },
    }


def sigmoid(value: float) -> float:
    if value >= 0:
        return 1.0 / (1.0 + math.exp(-value))
    exp_value = math.exp(value)
    return exp_value / (1.0 + exp_value)


def _solve_linear(matrix, vector):
    matrix = [list(row) + [float(vector[i])] for i, row in enumerate(matrix)]
    n = len(vector)
    for col in range(n):
        pivot = max(range(col, n), key=lambda row: abs(matrix[row][col]))
        if abs(matrix[pivot][col]) < 1e-12:
            raise ValueError("singular ridge logistic Newton system")
        matrix[col], matrix[pivot] = matrix[pivot], matrix[col]
        scale = matrix[col][col]
        matrix[col] = [value / scale for value in matrix[col]]
        for row in range(n):
            if row == col:
                continue
            factor = matrix[row][col]
            if factor:
                matrix[row] = [matrix[row][j] - factor * matrix[col][j] for j in range(n + 1)]
    return [matrix[i][-1] for i in range(n)]


def _objective(x, y, beta, penalty):
    total = 0.5 * penalty * sum(value * value for value in beta[1:])
    for row, label in zip(x, y):
        eta = sum(a * b for a, b in zip(row, beta))
        softplus = eta + math.log1p(math.exp(-eta)) if eta >= 0 else math.log1p(math.exp(eta))
        total += softplus - label * eta
    return total


def fit_ridge_logistic(features, labels, penalty=RIDGE_LAMBDA):
    x = np.asarray(features, dtype=float)
    y = np.asarray(labels, dtype=int)
    if x.ndim != 2 or len(x) != len(y) or len(y) < 10 or len(set(y.tolist())) != 2:
        raise ValueError("ridge logistic fit requires aligned features and both classes")
    means = x.mean(axis=0)
    scales = x.std(axis=0)
    scales[scales < 1e-12] = 1.0
    standardized = np.column_stack([np.ones(len(x)), (x - means) / scales]).tolist()
    beta = [math.log(float(y.sum()) / float(len(y) - y.sum()))] + [0.0] * x.shape[1]
    converged = False
    for iteration in range(1, 101):
        probabilities = [sigmoid(sum(a * b for a, b in zip(row, beta))) for row in standardized]
        dimension = len(beta)
        gradient = [0.0] * dimension
        hessian = [[0.0] * dimension for _ in range(dimension)]
        for row, label, probability in zip(standardized, y.tolist(), probabilities):
            residual = probability - label
            weight = probability * (1 - probability)
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
        old = _objective(standardized, y.tolist(), beta, penalty)
        size = 1.0
        while size >= 1e-8:
            candidate = [beta[i] - size * step[i] for i in range(dimension)]
            if _objective(standardized, y.tolist(), candidate, penalty) <= old + 1e-12:
                beta = candidate
                break
            size *= 0.5
        else:
            raise ValueError("ridge logistic line search failed")
    if not converged:
        raise ValueError("ridge logistic fit did not converge")
    return {
        "intercept": beta[0],
        "coefficients": beta[1:],
        "feature_means": means.tolist(),
        "feature_scales": scales.tolist(),
        "ridge_lambda": penalty,
        "iterations": iteration,
        "converged": True,
    }


def predict_probability(features, model):
    output = []
    for row in features:
        z = [(float(value) - mean) / scale for value, mean, scale in zip(row, model["feature_means"], model["feature_scales"])]
        output.append(sigmoid(model["intercept"] + sum(a * b for a, b in zip(z, model["coefficients"]))))
    return output


def auc(labels, scores):
    positive = [score for label, score in zip(labels, scores) if label == 1]
    negative = [score for label, score in zip(labels, scores) if label == 0]
    if not positive or not negative:
        raise ValueError("AUROC requires both classes")
    return sum(1.0 if p > n else 0.5 if p == n else 0.0 for p in positive for n in negative) / (len(positive) * len(negative))


def auc_ci(labels, scores):
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
        return values[lo] if lo == hi else values[lo] * (hi - position) + values[hi] * (position - lo)
    return {"method": "stratified patient bootstrap", "iterations": BOOTSTRAP_ITERATIONS,
            "seed": BOOTSTRAP_SEED, "lower_95": quantile(0.025), "upper_95": quantile(0.975)}


def calculate_metrics(labels, probabilities):
    predictions = [int(value >= 0.5) for value in probabilities]
    tp = sum(y == 1 and p == 1 for y, p in zip(labels, predictions))
    fn = sum(y == 1 and p == 0 for y, p in zip(labels, predictions))
    tn = sum(y == 0 and p == 0 for y, p in zip(labels, predictions))
    fp = sum(y == 0 and p == 1 for y, p in zip(labels, predictions))
    sensitivity, specificity = tp / (tp + fn), tn / (tn + fp)
    prevalence = sum(labels) / len(labels)
    brier = sum((p - y) ** 2 for p, y in zip(probabilities, labels)) / len(labels)
    baseline = prevalence * (1 - prevalence)
    interval = auc_ci(labels, probabilities)
    return {
        "n": len(labels), "responders": sum(labels), "nonresponders": len(labels) - sum(labels),
        "prevalence": prevalence, "auroc": auc(labels, probabilities), "auroc_95_ci": interval,
        "balanced_accuracy_at_0_5": 0.5 * (sensitivity + specificity),
        "sensitivity_at_0_5": sensitivity, "specificity_at_0_5": specificity,
        "brier": brier, "prevalence_only_brier": baseline,
        "brier_beats_prevalence_baseline": brier < baseline,
    }


def run_development():
    validation, panel_genes, validation_sources = _read_gse93157()
    liu, liu_genes, liu_sources = _read_liu(panel_genes)
    gide, gide_genes, gide_sources = _read_gide(panel_genes)
    genes = sorted(panel_genes & liu_genes & gide_genes)
    if len(genes) < 100:
        raise ValueError(f"only {len(genes)} common panel genes across cohorts; require at least 100")
    for row in liu + gide + validation:
        missing = set(genes) - set(row["expression"])
        if missing:
            raise ValueError(f"{row['cohort']}/{row['sample_id']} missing {len(missing)} common panel genes")
    training = liu + gide
    labels = [row["y"] for row in training]
    cohort_deltas = {"Liu_DFCI": len(liu), "Gide_PRJEB23709": len(gide)}
    selected_pairs, selection = select_pairs(training, genes, cohort_deltas)
    train_features = [pair_features(row["expression"], selected_pairs) for row in training]
    validation_features = [pair_features(row["expression"], selected_pairs) for row in validation]
    model = fit_ridge_logistic(train_features, labels)
    train_probabilities = predict_probability(train_features, model)
    validation_probabilities = predict_probability(validation_features, model)
    train_metrics = calculate_metrics(labels, train_probabilities)
    validation_labels = [row["y"] for row in validation]
    validation_metrics = calculate_metrics(validation_labels, validation_probabilities)
    overlap_ids = sorted(set(row["patient_id"] for row in training) & set(row["patient_id"] for row in validation))
    if overlap_ids:
        raise ValueError(f"source patient identifiers overlap training and validation: {overlap_ids}")

    screen = {
        "auroc_point_estimate_gt_0_5": validation_metrics["auroc"] > 0.5,
        "auroc_ci_lower_gt_0_5": validation_metrics["auroc_95_ci"]["lower_95"] > 0.5,
        "brier_better_than_prevalence_baseline": validation_metrics["brier_beats_prevalence_baseline"],
        "balanced_accuracy_gt_0_5": validation_metrics["balanced_accuracy_at_0_5"] > 0.5,
    }
    screen["passed_single_cohort_screen"] = all(screen.values())
    return {
        "status": "REO_V4_DEVELOPMENT_AND_GSE93157_TEST_COMPLETE",
        "model_version": MODEL_VERSION,
        "development_cohorts": {
            "Liu_DFCI": {"sample_count": len(liu), "metrics": calculate_metrics([row["y"] for row in liu], train_probabilities[:len(liu)]), "source": liu_sources},
            "Gide_PRJEB23709": {"sample_count": len(gide), "source": gide_sources,
                                "endpoint": "pretreatment anti-PD-1 monotherapy; CR/PR versus PD; SD excluded"},
            "combined_sample_count": len(training),
            "endpoint": "CR/PR versus PD; SD/mixed/unknown excluded",
        },
        "external_validation_cohort": {
            "name": "GSE93157 melanoma pretreatment anti-PD-1",
            "source": validation_sources,
            "sample_count": len(validation),
            "metrics": validation_metrics,
            "patient_overlap_with_training": overlap_ids,
        },
        "feature_space": {"common_gene_count": len(genes), "genes": genes, "pair_selection": selection},
        "selected_pairs": selected_pairs,
        "model_parameters": model,
        "development_apparent_metrics_not_for_claims": train_metrics,
        "external_promotion_screen": screen,
        "claim_boundary": (
            "Research-stage candidate only. GSE93157 is one small NanoString cohort and cross-platform "
            "gene-order comparability is not proven. No clinical utility, treatment-selection benefit, "
            "prospective validity, or patient outcome improvement is established. Do not use for treatment decisions."
        ),
    }


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Develop a broad melanoma REO candidate and test on GSE93157.")
    parser.add_argument("--output", type=Path, default=Path("melanoma-reo-v4-receipt.json"))
    args = parser.parse_args()
    result = run_development()
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "model_version": result["model_version"],
        "common_gene_count": result["feature_space"]["common_gene_count"],
        "selection": result["feature_space"]["pair_selection"],
        "selected_pairs": result["selected_pairs"],
        "external_validation_metrics": result["external_validation_cohort"]["metrics"],
        "external_promotion_screen": result["external_promotion_screen"],
        "receipt": str(args.output),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
