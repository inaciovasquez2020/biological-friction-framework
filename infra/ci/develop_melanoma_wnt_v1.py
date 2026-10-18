#!/usr/bin/env python3
"""Prespecified exploratory Wnt score for GSE165745; not a clinical tool.

The score is fixed from the published directional hypothesis before inspecting
sample-level outcomes: Wnt ligand/receptor/effector genes associated with
resistance contribute positively; RNF43, a negative regulator highlighted in
responders, contributes negatively. No feature selection or coefficient fitting
is performed. The 24-sample dataset is an exploratory cohort, not independent
validation.
"""
from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import io
import json
import math
import urllib.request
from pathlib import Path

URL = (
    "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE165nnn/GSE165745/"
    "matrix/GSE165745_series_matrix.txt.gz"
)
VERSION = "MELANOMA_WNT_FIXED_SCORE_V1_2026_10_18"
# Fixed before evaluation; symbols are restricted to the deposited NanoString panel.
RESISTANCE_GENES = (
    "WNT2B", "WNT5A", "WNT7B", "WNT8B", "FZD1", "FZD2", "FZD4",
    "FZD5", "FZD7", "FZD8", "FZD10", "LRP5", "LRP6", "DKK2",
    "SFRP2", "SFRP4", "PYGO1", "DVL1",
)
RESPONDER_GENES = ("RNF43",)
MIN_PANEL_GENES = 5


def fetch_matrix(url: str = URL) -> tuple[bytes, str]:
    request = urllib.request.Request(url, headers={"User-Agent": VERSION})
    with urllib.request.urlopen(request, timeout=90) as response:
        raw = response.read()
    if not raw:
        raise RuntimeError("GEO series matrix download was empty")
    if raw[:2] == b"\\x1f\\x8b":
        raw = gzip.decompress(raw)
    return raw, hashlib.sha256(raw).hexdigest()


def parse_series_matrix(raw: bytes) -> tuple[list[dict], dict]:
    text = raw.decode("utf-8-sig")
    lines = text.splitlines()
    titles = None
    for line in lines:
        if line.startswith("!Sample_title"):
            titles = next(csv.reader([line], delimiter="\t"))[1:]
            break
    if not titles:
        raise ValueError("GEO matrix lacks !Sample_title metadata")
    try:
        start = next(i for i, line in enumerate(lines) if line == "!series_matrix_table_begin")
        end = next(i for i, line in enumerate(lines[start + 1:], start + 1)
                   if line == "!series_matrix_table_end")
    except StopIteration as exc:
        raise ValueError("GEO matrix expression table delimiters missing") from exc

    table = list(csv.reader(io.StringIO("\n".join(lines[start + 1:end])), delimiter="\t"))
    if not table or len(table[0]) != len(titles) + 1:
        raise ValueError("sample-title count does not match expression matrix width")
    header = table[0]
    sample_expr = [dict() for _ in titles]
    for row in table[1:]:
        if len(row) != len(header):
            continue
        gene = row[0].strip().strip('"')
        try:
            values = [float(v) for v in row[1:]]
        except ValueError:
            continue
        if not gene or not all(math.isfinite(v) for v in values):
            continue
        for i, value in enumerate(values):
            sample_expr[i][gene.upper()] = value

    rows = []
    for title, expression in zip(titles, sample_expr):
        normalized = title.lower()
        if "nonresponder" in normalized or normalized.startswith("nr"):
            y = 0
            label = "NONRESPONDER"
        elif "responder" in normalized or normalized.startswith("r"):
            y = 1
            label = "RESPONDER"
        else:
            raise ValueError(f"unrecognized response label in GEO title: {title}")
        rows.append({"sample_title": title, "label": label, "y": y, "expression": expression})
    metadata = {
        "dataset": "GSE165745",
        "source_url": URL,
        "raw_sha256": hashlib.sha256(raw).hexdigest(),
        "sample_count": len(rows),
        "response_counts": {
            "responders": sum(r["y"] for r in rows),
            "nonresponders": sum(1 - r["y"] for r in rows),
        },
        "sample_titles": titles,
    }
    return rows, metadata


def fixed_wnt_score(expression: dict[str, float]) -> tuple[float, dict]:
    resistance = [g for g in RESISTANCE_GENES if g in expression]
    responder = [g for g in RESPONDER_GENES if g in expression]
    if len(resistance) < MIN_PANEL_GENES or not responder:
        raise ValueError(
            f"panel coverage inadequate: resistance genes={len(resistance)}, "
            f"responder genes={len(responder)}"
        )
    # log1p is applied to nonnegative NanoString processed counts; fail closed otherwise.
    used = resistance + responder
    if any(expression[g] < 0 for g in used):
        raise ValueError("negative expression value is incompatible with fixed log1p score")
    resistance_mean = sum(math.log1p(expression[g]) for g in resistance) / len(resistance)
    responder_mean = sum(math.log1p(expression[g]) for g in responder) / len(responder)
    return resistance_mean - responder_mean, {
        "resistance_genes_present": resistance,
        "responder_genes_present": responder,
        "resistance_gene_count": len(resistance),
        "responder_gene_count": len(responder),
        "formula": "mean(log1p(resistance-associated Wnt panel genes)) - mean(log1p(RNF43))",
        "direction": "higher score predicts nonresponse",
    }


def auc(labels: list[int], scores: list[float]) -> float:
    positives = sum(labels)
    negatives = len(labels) - positives
    if positives == 0 or negatives == 0:
        raise ValueError("AUROC requires both outcome classes")
    order = sorted(range(len(scores)), key=lambda i: scores[i])
    ranks = [0.0] * len(scores)
    i = 0
    while i < len(order):
        j = i + 1
        while j < len(order) and scores[order[j]] == scores[order[i]]:
            j += 1
        average_rank = ((i + 1) + j) / 2
        for k in range(i, j):
            ranks[order[k]] = average_rank
        i = j
    positive_rank_sum = sum(ranks[i] for i, y in enumerate(labels) if y == 1)
    return (positive_rank_sum - positives * (positives + 1) / 2) / (positives * negatives)


def evaluate(rows: list[dict], metadata: dict) -> dict:
    if len(rows) < 4 or len({r["y"] for r in rows}) != 2:
        raise ValueError("exploratory evaluation requires at least four samples and both classes")
    scored = []
    gene_receipt = None
    for row in rows:
        score, gene_receipt = fixed_wnt_score(row["expression"])
        scored.append({**row, "score": score})
    # Larger score means predicted nonresponse. AUC is oriented to nonresponse as positive.
    labels = [1 - r["y"] for r in scored]
    scores = [r["score"] for r in scored]
    threshold = (min(scores) + max(scores)) / 2
    predicted_nonresponse = [int(s >= threshold) for s in scores]
    truth_nonresponse = labels
    sensitivity = sum(p == 1 and y == 1 for p, y in zip(predicted_nonresponse, truth_nonresponse)) / max(1, sum(truth_nonresponse))
    specificity = sum(p == 0 and y == 0 for p, y in zip(predicted_nonresponse, truth_nonresponse)) / max(1, sum(1 - y for y in truth_nonresponse))
    # This is a score, not a calibrated probability; no Brier score is reported.
    return {
        "status": "EXPLORATORY_FIXED_SCORE_EVALUATED",
        "model_version": VERSION,
        "dataset": metadata,
        "feature_definition": gene_receipt,
        "evaluation": {
            "sample_count": len(scored),
            "responders": sum(r["y"] for r in scored),
            "nonresponders": sum(1 - r["y"] for r in scored),
            "auroc_for_nonresponse": auc(labels, scores),
            "balanced_accuracy_at_midrange_score_threshold": (sensitivity + specificity) / 2,
            "threshold_rule": "midpoint of observed minimum and maximum score; descriptive only",
            "sample_scores": [
                {"sample_title": r["sample_title"], "observed_label": r["label"], "score": r["score"]}
                for r in scored
            ],
        },
        "limitations": [
            "n=24; exploratory only, with no independent validation cohort in this analysis",
            "response labels are those deposited with GEO; clinical endpoint details require source-paper audit",
            "processed NanoString values are used as deposited; normalization provenance must be verified",
            "the score is not a calibrated probability and must not guide treatment",
            "no feature selection, coefficient fitting, threshold tuning, or outcome-based model tuning was performed",
        ],
        "claim_boundary": "No clinical utility, external validity, treatment-selection benefit, or patient-outcome improvement is established.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("melanoma-wnt-v1-receipt.json"))
    args = parser.parse_args()
    raw, raw_sha = fetch_matrix()
    rows, metadata = parse_series_matrix(raw)
    metadata["download_payload_sha256"] = raw_sha
    result = evaluate(rows, metadata)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "model_version": VERSION,
        "sample_count": result["evaluation"]["sample_count"],
        "auroc_for_nonresponse": result["evaluation"]["auroc_for_nonresponse"],
        "receipt": str(args.output),
        "claim_boundary": result["claim_boundary"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
