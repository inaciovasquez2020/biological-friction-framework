#!/usr/bin/env python3
"""Locked feasibility audit for Liu/DFCI melanoma cohort; deliberately does not score v2."""
from __future__ import annotations
import csv
import hashlib
import io
import json
import os
import sys
import urllib.request
from collections import Counter
from datetime import datetime, timezone

BASE = "https://media.githubusercontent.com/media/cBioPortal/datahub/7a4b4ec142f76ac04db22834232b23142d25bd2a/public/mel_dfci_2019/"
FILES = {
    "patient": "data_clinical_patient.txt",
    "sample": "data_clinical_sample.txt",
    "expression": "data_mrna_seq_tpm.txt",
}
GENES = ["KDM5B", "CD36", "MITF", "MTHFD2", "NGFR", "NT5E", "SOX10"]


def get_bytes(name: str) -> bytes:
    req = urllib.request.Request(BASE + FILES[name], headers={"User-Agent": "melanoma-v2-cohort-preflight/1.0"})
    with urllib.request.urlopen(req, timeout=90) as response:
        data = response.read()
        if not data or data.startswith(b"version https://git-lfs.github.com/spec/v1"):
            raise RuntimeError(f"{name}: response was empty or a Git LFS pointer, not the actual data")
        return data


def parse_cbio_tsv(data: bytes, name: str):
    text = data.decode("utf-8-sig")
    rows = list(csv.reader(io.StringIO(text), delimiter="\t"))
    if len(rows) < 6 or not rows[0][0].startswith("#"):
        raise RuntimeError(f"{name}: unexpected cBioPortal clinical file format")
    headers = rows[4]
    records = []
    for row in rows[5:]:
        if not row or all(v == "" for v in row):
            continue
        row = row + [""] * (len(headers) - len(row))
        records.append(dict(zip(headers, row)))
    return headers, records


def classify_response(label: str):
    """Map source clinical response labels to the frozen CR/PR-vs-PD endpoint."""
    norm = "".join(ch for ch in label.upper() if ch.isalnum())
    if norm in {"CR", "PR", "CRPR", "PRCR", "COMPLETERESPONSE", "PARTIALRESPONSE"}:
        return "RESPONDER_CR_PR"
    if norm in {"PD", "PROGRESSIVEDISEASE"}:
        return "NONRESPONDER_PD"
    return "EXCLUDED_NONMATCHING_OR_UNKNOWN"


def main():
    raw = {k: get_bytes(k) for k in FILES}
    patient_headers, patients = parse_cbio_tsv(raw["patient"], "patient clinical")
    sample_headers, samples = parse_cbio_tsv(raw["sample"], "sample clinical")

    required_patient = {"PATIENT_ID", "BR"}
    required_sample = {"PATIENT_ID", "SAMPLE_ID"}
    if not required_patient.issubset(patient_headers):
        raise RuntimeError(f"patient clinical missing required columns: {sorted(required_patient - set(patient_headers))}")
    if not required_sample.issubset(sample_headers):
        raise RuntimeError(f"sample clinical missing required columns: {sorted(required_sample - set(sample_headers))}")

    # Expression is a gene-by-sample matrix; parse the header and gene symbols only.
    exp_text = raw["expression"].decode("utf-8-sig")
    exp_reader = csv.reader(io.StringIO(exp_text), delimiter="\t")
    exp_header = next(exp_reader)
    if len(exp_header) < 3:
        raise RuntimeError("TPM expression matrix has fewer than three columns")
    gene_col = 0
    sample_ids = set(exp_header[2:])
    gene_symbols = set()
    duplicate_gene_rows = Counter()
    for row in exp_reader:
        if not row:
            continue
        symbol = row[gene_col].strip()
        if symbol:
            gene_symbols.add(symbol)
            duplicate_gene_rows[symbol] += 1

    patient_by_id = {p.get("PATIENT_ID", "").strip(): p for p in patients if p.get("PATIENT_ID", "").strip()}
    mapped_samples = [s for s in samples if s.get("SAMPLE_ID", "").strip() in sample_ids]
    sample_to_patient = Counter(s.get("PATIENT_ID", "").strip() for s in mapped_samples)
    patients_with_expression = sorted({s.get("PATIENT_ID", "").strip() for s in mapped_samples if s.get("PATIENT_ID", "").strip()})
    response_counts = Counter()
    endpoint_counts = Counter()
    endpoint_patients = []
    missing_patient_labels = []
    for pid in patients_with_expression:
        p = patient_by_id.get(pid)
        if not p:
            missing_patient_labels.append(pid)
            response_counts["MISSING_PATIENT_ROW"] += 1
            continue
        label = p.get("BR", "").strip()
        response_counts[label or "MISSING_RESPONSE"] += 1
        endpoint_class = classify_response(label)
        endpoint_counts[endpoint_class] += 1
        if endpoint_class == "RESPONDER_CR_PR":
            endpoint_patients.append({"patient_id": pid, "source_response": label, "frozen_class": "CR_PR"})
        elif endpoint_class == "NONRESPONDER_PD":
            endpoint_patients.append({"patient_id": pid, "source_response": label, "frozen_class": "PD"})

    genes_missing = [g for g in GENES if g not in gene_symbols]
    duplicate_sample_ids = len(sample_ids) != len(exp_header[2:])
    patient_multi_sample = sorted(pid for pid, count in sample_to_patient.items() if count > 1)
    receipt = {
        "schema": "mel_dfci_v2_cohort_preflight_v1",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "study": "mel_dfci_2019",
        "source_commit": "7a4b4ec142f76ac04db22834232b23142d25bd2a",
        "source_urls": {k: BASE + v for k, v in FILES.items()},
        "sha256": {k: hashlib.sha256(v).hexdigest() for k, v in raw.items()},
        "source_sizes_bytes": {k: len(v) for k, v in raw.items()},
        "expression_unit": "RNA-seq TPM (cBioPortal datahub; not FPKM)",
        "expression_sample_columns": len(sample_ids),
        "expression_gene_symbols": len(gene_symbols),
        "required_seven_gene_coverage": {g: g in gene_symbols for g in GENES},
        "missing_required_genes": genes_missing,
        "duplicate_expression_sample_columns": duplicate_sample_ids,
        "clinical_patient_rows": len(patients),
        "clinical_sample_rows": len(samples),
        "expression_columns_matching_clinical_samples": len(mapped_samples),
        "patients_with_expression": len(patients_with_expression),
        "patients_with_multiple_expression_samples": patient_multi_sample,
        "response_field": "BR",
        "source_response_counts_among_expression_patients": dict(response_counts),
        "frozen_endpoint_counts_before_patient-level deduplication": dict(endpoint_counts),
        "missing_patient_rows": missing_patient_labels,
        "endpoint_patient_rows": endpoint_patients,
        "score_computed": False,
        "v2_eligible": False,
        "decision": "BLOCKED_NOT_SCORED",
        "blockers": [
            "Candidate matrix is TPM, while the frozen GSE78220 ECDF reference is FPKM; no justified per-sample conversion or same-pipeline FPKM reconstruction has been established.",
            "Clinical sample-to-patient mapping, duplicate specimen policy, and exact CR/PR-versus-PD endpoint require human-readable verification before scoring.",
            "This preflight does not establish expression-scale compatibility and must not be treated as model validation."
        ],
    }
    out = os.environ.get("OUTPUT_JSON", "mel_dfci_v2_cohort_preflight.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(receipt, f, indent=2, sort_keys=True)
        f.write("\n")
    print(json.dumps({k: receipt[k] for k in [
        "study", "expression_unit", "expression_sample_columns", "expression_gene_symbols",
        "required_seven_gene_coverage", "expression_columns_matching_clinical_samples",
        "patients_with_expression", "source_response_counts_among_expression_patients",
        "frozen_endpoint_counts_before_patient-level deduplication", "score_computed", "v2_eligible", "decision"
    ]}, indent=2))
    print(f"receipt={out}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"FAIL_CLOSED: {type(exc).__name__}: {exc}", file=sys.stderr)
        sys.exit(2)
