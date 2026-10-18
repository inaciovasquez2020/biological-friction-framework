import argparse
import csv
import gzip
import hashlib
import importlib.util
import io
import json
import math
import random
import re
import tempfile
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BASE_AUDIT_PATH = ROOT / "audit_gse78220_development.py"
V2_PATH = ROOT / "score_melanoma_route_burden_v2.py"
CALIBRATION_PATH = ROOT / "fit_melanoma_v2_calibration.py"

SERIES_URL = "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE91nnn/GSE91061/matrix/GSE91061_series_matrix.txt.gz"
FPKM_URL = "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE91nnn/GSE91061/suppl/GSE91061_BMS038109Sample.hg19KnownGene.fpkm.csv.gz"

# NCBI Entrez Gene identifiers, not inferred from expression values.
ENTREZ_TO_SYMBOL = {
    "10765": "KDM5B",
    "948": "CD36",
    "4286": "MITF",
    "10797": "MTHFD2",
    "4804": "NGFR",
    "4907": "NT5E",
    "6663": "SOX10",
}
FROZEN_INTERCEPT = -2.7753294906668593
FROZEN_SLOPE = 5.91276103727729
FROZEN_THRESHOLD = 0.5
BOOTSTRAP_ITERATIONS = 10000
BOOTSTRAP_SEED = 20261018


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load repository module: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


BASE = load_module("gse78220_base_for_gse91061", BASE_AUDIT_PATH)
V2 = load_module("melanoma_v2_for_gse91061", V2_PATH)
CAL = load_module("melanoma_v2_calibration_for_gse91061", CALIBRATION_PATH)


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def download(url):
    req = urllib.request.Request(
        url, headers={"User-Agent": "biological-friction-framework-gse91061-validation/1.0"}
    )
    with urllib.request.urlopen(req, timeout=120) as response:
        data = response.read()
    return data, sha256(data)


def parse_series_matrix(text):
    titles = None
    descriptions = None
    characteristics = []
    for line in text.splitlines():
        if line.startswith("!Sample_title\t"):
            titles = next(csv.reader([line], delimiter="\t"))[1:]
        elif line.startswith("!Sample_description\t"):
            descriptions = next(csv.reader([line], delimiter="\t"))[1:]
        elif line.startswith("!Sample_characteristics_ch1\t"):
            characteristics.append(next(csv.reader([line], delimiter="\t"))[1:])
    if not titles or len(set(titles)) != len(titles):
        raise ValueError("GSE91061 series matrix has missing or duplicate sample titles")
    if descriptions is not None and len(descriptions) != len(titles):
        raise ValueError("GSE91061 sample descriptions are misaligned")
    if any(len(row) != len(titles) for row in characteristics):
        raise ValueError("GSE91061 sample characteristics are misaligned")

    records = {}
    for i, title in enumerate(titles):
        fields = {}
        for row in characteristics:
            token = row[i].strip()
            if ":" not in token:
                continue
            key, value = token.split(":", 1)
            key = re.sub(r"\s+", " ", key.strip().lower())
            value = value.strip()
            if key in fields and fields[key] != value:
                raise ValueError(f"{title}: conflicting characteristic {key}")
            fields[key] = value

        desc = descriptions[i] if descriptions is not None else ""
        patient = None
        for key, value in fields.items():
            if "patient id" in key or key == "patient" or key == "patient identifier":
                patient = value.strip()
                break
        if not patient:
            match = re.search(r"\bPt\s*([A-Za-z0-9.-]+)", title, re.IGNORECASE)
            if match:
                patient = "Pt" + match.group(1)
        if not patient:
            raise ValueError(f"{title}: cannot identify patient from source metadata/title")

        title_match = re.search(r"_(Pre|On)(?:_|$)", title, re.IGNORECASE)
        timepoint = None
        if title_match:
            timepoint = "pretreatment" if title_match.group(1).lower() == "pre" else "on-treatment"
        for key, value in fields.items():
            if "visit" in key or "biopsy time" in key or "treatment" in key and "response" not in key:
                norm = value.lower().replace("_", " ").replace("-", " ")
                if "pre" in norm or "baseline" in norm:
                    found = "pretreatment"
                elif "on" in norm or "post" in norm:
                    found = "on-treatment"
                else:
                    continue
                if timepoint is not None and timepoint != found:
                    raise ValueError(f"{title}: conflicting timepoint metadata")
                timepoint = found
        if timepoint is None:
            desc_lower = desc.lower()
            if "pre anti-pd-1 treatment" in desc_lower:
                timepoint = "pretreatment"
            elif "on anti-pd-1 treatment" in desc_lower:
                timepoint = "on-treatment"
        if timepoint is None:
            raise ValueError(f"{title}: cannot establish pretreatment/on-treatment status")

        response = None
        for key, value in fields.items():
            if "response" in key:
                if response is not None and response != value:
                    raise ValueError(f"{title}: conflicting response annotations")
                response = value.strip()
        if response is None:
            response = ""

        ordinal = None
        ordinal_match = re.search(r"\b(\d+)(?:st|nd|rd|th)\s+biopsy\b", desc, re.IGNORECASE)
        if ordinal_match:
            ordinal = int(ordinal_match.group(1))

        records[title] = {
            "sample_id": title,
            "patient_id": patient,
            "timepoint": timepoint,
            "response": response,
            "biopsy_ordinal": ordinal,
            "characteristics": fields,
            "description": desc,
        }
    return records


def freeze_pretreatment(records):
    by_patient = {}
    for record in records.values():
        if record["timepoint"] == "pretreatment":
            by_patient.setdefault(record["patient_id"], []).append(record)
    selected = []
    excluded = []
    for patient, samples in sorted(by_patient.items()):
        if len(samples) == 1:
            selected.append(samples[0])
            continue
        if any(sample["biopsy_ordinal"] is None for sample in samples):
            raise ValueError(
                f"{patient}: multiple pretreatment samples without source biopsy ordinals; "
                "patient-level deduplication cannot be resolved without guessing"
            )
        samples = sorted(samples, key=lambda r: (r["biopsy_ordinal"], r["sample_id"]))
        ordinals = [r["biopsy_ordinal"] for r in samples]
        if len(ordinals) != len(set(ordinals)):
            raise ValueError(f"{patient}: tied pretreatment biopsy ordinals")
        selected.append(samples[0])
        excluded.extend({
            "sample_id": r["sample_id"], "patient_id": patient,
            "reason": "later_pretreatment_biopsy", "biopsy_ordinal": r["biopsy_ordinal"]
        } for r in samples[1:])
    if not selected:
        raise ValueError("GSE91061 contains no eligible pretreatment patients")
    return selected, excluded


def endpoint(raw):
    token = re.sub(r"[_\-/]+", " ", str(raw).strip().upper())
    token = re.sub(r"\s+", " ", token)
    if token in {"CR", "COMPLETE RESPONSE", "COMPLETE RESPONDER", "PR", "PARTIAL RESPONSE", "PARTIAL RESPONDER"}:
        return 1, "CR_PR"
    if token in {"PD", "PROGRESSIVE DISEASE", "PROGRESSION", "PROGRESSIVE"}:
        return 0, "PD"
    if token in {"SD", "STABLE DISEASE", "MIXED", "MIXED RESPONSE", "MR", "UNEVALUABLE", "NOT EVALUABLE", "NE", "UNKNOWN", "NA", "N A", "MISSING", ""}:
        return None, "excluded_nonprimary_endpoint"
    raise ValueError(f"unrecognised response annotation {raw!r}; fail closed")


def build_route_tsv(fpkm_gzip_bytes, expected_samples, output_path):
    raw = gzip.decompress(fpkm_gzip_bytes)
    text = raw.decode("utf-8-sig")
    reader = csv.reader(io.StringIO(text))
    try:
        header = next(reader)
    except StopIteration as exc:
        raise ValueError("GSE91061 FPKM matrix is empty") from exc
    if len(header) < 2:
        raise ValueError("GSE91061 FPKM matrix has no sample columns")
    samples = [str(x).strip().strip('"') for x in header[1:]]
    if len(samples) != len(set(samples)):
        raise ValueError("duplicate sample names in GSE91061 FPKM matrix")
    if set(samples) != set(expected_samples):
        raise ValueError(
            "expression/metadata sample mismatch: "
            f"expression_only={sorted(set(samples)-set(expected_samples))[:8]}, "
            f"metadata_only={sorted(set(expected_samples)-set(samples))[:8]}"
        )
    found = {}
    for line_no, row in enumerate(reader, start=2):
        if not row or all(not cell.strip() for cell in row):
            continue
        if len(row) != len(header):
            raise ValueError(f"FPKM row {line_no} width mismatch")
        gene_id = row[0].strip().strip('"')
        symbol = ENTREZ_TO_SYMBOL.get(gene_id)
        if symbol is None:
            continue
        if symbol in found:
            raise ValueError(f"duplicate Entrez rows mapped to {symbol}")
        values = {}
        for sample, raw_value in zip(samples, row[1:]):
            try:
                value = float(raw_value)
            except ValueError as exc:
                raise ValueError(f"non-numeric FPKM {symbol}/{sample}: {raw_value!r}") from exc
            if not math.isfinite(value):
                raise ValueError(f"non-finite FPKM {symbol}/{sample}")
            values[sample] = value
        found[symbol] = values
    missing = sorted(set(ENTREZ_TO_SYMBOL.values()) - set(found))
    if missing:
        raise ValueError(f"frozen route markers missing from FPKM matrix: {missing}")
    with open(output_path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(["gene", *samples])
        for symbol in ENTREZ_TO_SYMBOL.values():
            writer.writerow([symbol, *[found[symbol][sample] for sample in samples]])
    return {"sample_count": len(samples), "route_genes": sorted(found), "matrix_sha256_uncompressed": sha256(raw)}


def auc(labels, scores):
    positives = [s for y, s in zip(labels, scores) if y == 1]
    negatives = [s for y, s in zip(labels, scores) if y == 0]
    if not positives or not negatives:
        raise ValueError("AUROC requires both responders and nonresponders")
    wins = sum(1.0 if p > n else 0.5 if p == n else 0.0 for p in positives for n in negatives)
    return wins / (len(positives) * len(negatives))


def auc_ci(labels, scores):
    pos = [s for y, s in zip(labels, scores) if y == 1]
    neg = [s for y, s in zip(labels, scores) if y == 0]
    rng = random.Random(BOOTSTRAP_SEED)
    values = []
    for _ in range(BOOTSTRAP_ITERATIONS):
        bp = [rng.choice(pos) for _ in pos]
        bn = [rng.choice(neg) for _ in neg]
        values.append(auc([1] * len(bp) + [0] * len(bn), bp + bn))
    values.sort()
    def q(p):
        x = p * (len(values) - 1)
        lo, hi = math.floor(x), math.ceil(x)
        return values[lo] if lo == hi else values[lo] * (hi-x) + values[hi] * (x-lo)
    return {"method": "stratified_patient_bootstrap", "iterations": BOOTSTRAP_ITERATIONS,
            "seed": BOOTSTRAP_SEED, "lower_95": q(0.025), "upper_95": q(0.975)}


def run_validation(output_path=None):
    series_gz, series_gz_sha = download(SERIES_URL)
    series_bytes = gzip.decompress(series_gz) if series_gz[:2] == b"\x1f\x8b" else series_gz
    series_text = series_bytes.decode("utf-8")
    if "!Sample_title" not in series_text:
        raise ValueError("downloaded series file is not a GEO series matrix")
    metadata = parse_series_matrix(series_text)
    selected, dedup_exclusions = freeze_pretreatment(metadata)

    fpkm_gz, fpkm_gz_sha = download(FPKM_URL)
    with tempfile.TemporaryDirectory() as tmp:
        route_tsv = Path(tmp) / "gse91061_route.tsv"
        matrix_info = build_route_tsv(fpkm_gz, set(metadata), route_tsv)

        # Reproduce the frozen development reference and calibration from GSE78220 only.
        dev_audit = BASE.run_audit()
        if dev_audit.get("decision") != "CONTINUE_TO_CALIBRATION_FREEZE_BEFORE_GSE91061":
            raise ValueError("GSE78220 v2 continuation gate no longer passes")
        fit = CAL.run_fit()["calibration"]
        if not math.isclose(fit["intercept"], FROZEN_INTERCEPT, rel_tol=0.0, abs_tol=1e-12):
            raise ValueError("recomputed development intercept differs from frozen coefficient")
        if not math.isclose(fit["slope"], FROZEN_SLOPE, rel_tol=0.0, abs_tol=1e-12):
            raise ValueError("recomputed development slope differs from frozen coefficient")
        reference = dev_audit["feature"]["reference"]
        selected_ids = [r["sample_id"] for r in selected]
        scored = V2.score_matrix(route_tsv, reference, selected_ids)

        patient_rows = []
        exclusions = list(dedup_exclusions)
        for record in selected:
            y, endpoint_name = endpoint(record["response"])
            score = scored["samples"][record["sample_id"]]
            probability = 1.0 / (1.0 + math.exp(-(FROZEN_INTERCEPT + FROZEN_SLOPE * score["s_pd1_v2"])))
            row = {
                "sample_id": record["sample_id"],
                "patient_id": record["patient_id"],
                "timepoint": record["timepoint"],
                "raw_response": record["response"],
                "endpoint": endpoint_name,
                "y": y,
                "s_pd1_v2": score["s_pd1_v2"],
                "route_burden_v2": score["route_burden_v2"],
                "predicted_probability": probability,
                "predicted_class": 1 if probability >= FROZEN_THRESHOLD else 0,
            }
            if y is None:
                exclusions.append({**row, "reason": endpoint_name})
            else:
                patient_rows.append(row)

    labels = [r["y"] for r in patient_rows]
    scores = [r["predicted_probability"] for r in patient_rows]
    predictions = [r["predicted_class"] for r in patient_rows]
    if not labels or len(set(labels)) != 2:
        raise ValueError(f"eligible validation endpoint lacks both classes; class_counts={ {str(y): labels.count(y) for y in set(labels)} }")
    tp = sum(y == 1 and p == 1 for y, p in zip(labels, predictions))
    fn = sum(y == 1 and p == 0 for y, p in zip(labels, predictions))
    tn = sum(y == 0 and p == 0 for y, p in zip(labels, predictions))
    fp = sum(y == 0 and p == 1 for y, p in zip(labels, predictions))
    sensitivity = tp / (tp + fn)
    specificity = tn / (tn + fp)
    prevalence = sum(labels) / len(labels)
    brier = sum((p-y) ** 2 for p, y in zip(scores, labels)) / len(labels)
    prevalence_brier = prevalence * (1.0 - prevalence)
    metrics = {
        "n_included": len(labels),
        "n_responder": sum(labels),
        "n_nonresponder": len(labels) - sum(labels),
        "responder_prevalence": prevalence,
        "auroc": auc(labels, scores),
        "auroc_95_ci": auc_ci(labels, scores),
        "balanced_accuracy": 0.5 * (sensitivity + specificity),
        "sensitivity": sensitivity,
        "specificity": specificity,
        "brier_score": brier,
        "prevalence_only_brier": prevalence_brier,
        "brier_beats_prevalence_only": brier < prevalence_brier,
        "auroc_ci_lower_exceeds_0_5": auc_ci(labels, scores)["lower_95"] > 0.5,
    }
    promotion_conditions = {
        "auroc_point_estimate_gt_0_5": metrics["auroc"] > 0.5,
        "auroc_95_ci_lower_gt_0_5": metrics["auroc_ci_lower_exceeds_0_5"],
        "brier_better_than_prevalence_only": metrics["brier_beats_prevalence_only"],
        "reproducible_source_data_and_code": True,
        "second_independent_cohort_replication": False,
        "no_patient_or_biopsy_leakage": True,
    }
    result = {
        "status": "GSE91061_LOCKED_PRETREATMENT_VALIDATION_ATTEMPT",
        "feature_version": V2.FEATURE_VERSION,
        "calibration_version": CAL.CALIBRATION_VERSION,
        "cohort": "GSE91061_PRETREATMENT",
        "source": {
            "series_matrix_url": SERIES_URL,
            "series_matrix_compressed_sha256": series_gz_sha,
            "series_matrix_uncompressed_sha256": sha256(series_bytes),
            "fpkm_url": FPKM_URL,
            "fpkm_compressed_sha256": fpkm_gz_sha,
            **matrix_info,
            "entrez_to_symbol": ENTREZ_TO_SYMBOL,
        },
        "freeze": {
            "development_cohort": "GSE78220",
            "development_reference_recomputed_from_development_only": True,
            "frozen_intercept": FROZEN_INTERCEPT,
            "frozen_slope": FROZEN_SLOPE,
            "decision_threshold": FROZEN_THRESHOLD,
            "threshold_refit": False,
            "validation_expression_used_to_refit_reference": False,
            "validation_labels_used_to_refit_any_parameter": False,
            "on_treatment_samples_scored": False,
            "patient_level_deduplication": "one pretreatment sample per patient; if repeats, earliest source biopsy ordinal; fail closed if unresolved",
        },
        "selected_pretreatment_sample_count": len(selected),
        "dedup_exclusions": dedup_exclusions,
        "endpoint_exclusions": exclusions,
        "patients": patient_rows,
        "metrics": metrics,
        "promotion_conditions": promotion_conditions,
        "retrospectively_validated_predictive_model": False,
        "boundary": (
            "One locked external cohort analysis only. Even if all single-cohort statistical "
            "conditions pass, the repository's promotion gate also requires a second independent "
            "cohort replication without refitting. This report does not establish treatment selection, "
            "clinical utility, efficacy, or cure."
        ),
    }
    serialized = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if output_path:
        Path(output_path).write_text(serialized, encoding="utf-8")
    return result


def main():
    parser = argparse.ArgumentParser(description="Run locked GSE91061 pretreatment validation of melanoma v2.")
    parser.add_argument("--output", type=Path, default=Path("gse91061-v2-validation.json"))
    args = parser.parse_args()
    result = run_validation(args.output)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
