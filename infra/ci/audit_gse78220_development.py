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

EXPECTED_WORKBOOK_SHA256 = "ae3b044f23a0a4cd2859da36726a220856c35216a169c17f93dfc3bd20b04de6"
EXPECTED_GENE_ROWS = 25268
EXPECTED_SAMPLE_COLUMNS = 28

NCBI_WORKBOOK_URL = (
    "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE78nnn/GSE78220/"
    "suppl/GSE78220_PatientFPKM.xlsx"
)
PINNED_MIRROR_WORKBOOK_URL = (
    "https://raw.githubusercontent.com/VietHuynh3001/MELANOMA/"
    "78770ee3527fff857e5ee34c508979a6ee0ff697/"
    "melanoma/GSE78220/GSE78220_PatientFPKM.xlsx"
)
NCBI_SERIES_URL = (
    "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE78nnn/GSE78220/"
    "matrix/GSE78220_series_matrix.txt.gz"
)
PINNED_MIRROR_SERIES_URL = (
    "https://raw.githubusercontent.com/VietHuynh3001/MELANOMA/"
    "78770ee3527fff857e5ee34c508979a6ee0ff697/"
    "melanoma/GSE78220/GSE78220_series_matrix.txt"
)

SCORER_PATH = Path(__file__).resolve().with_name("score_melanoma_route_burden.py")
MANIFEST_PATH = Path(__file__).resolve().with_name("parse_melanoma_response_manifest.py")


def _load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to load module {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SCORER = _load_module("score_melanoma_route_burden", SCORER_PATH)
MANIFEST = _load_module("parse_melanoma_response_manifest", MANIFEST_PATH)


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def _download(url, timeout=90):
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "biological-friction-framework-gse78220-audit/1.0"},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read()


def download_checksum_locked(urls, expected_sha256):
    errors = []
    for url in urls:
        try:
            data = _download(url)
        except Exception as exc:
            errors.append(f"{url}: download failed: {exc}")
            continue
        digest = sha256_bytes(data)
        if digest != expected_sha256:
            errors.append(
                f"{url}: sha256 mismatch: expected {expected_sha256}, observed {digest}"
            )
            continue
        return data, url, digest
    raise RuntimeError("no checksum-valid workbook source: " + " | ".join(errors))


def download_series_text(urls):
    errors = []
    for url in urls:
        try:
            data = _download(url)
            if data[:2] == b"\x1f\x8b":
                data = gzip.decompress(data)
            text = data.decode("utf-8")
        except Exception as exc:
            errors.append(f"{url}: download/decode failed: {exc}")
            continue
        if "!Sample_title" not in text or "!Sample_characteristics_ch1" not in text:
            errors.append(f"{url}: does not look like a GEO series matrix")
            continue
        return text, url, sha256_bytes(data)
    raise RuntimeError("no usable series-matrix source: " + " | ".join(errors))


def _parse_geo_row(line):
    return next(csv.reader([line], delimiter="\t"))


def _normalise_key(value):
    return re.sub(r"\s+", " ", value.strip().lower())


def parse_geo_sample_metadata(text):
    titles = None
    descriptions = None
    characteristic_rows = []

    for line in text.splitlines():
        if line.startswith("!Sample_title\t"):
            titles = _parse_geo_row(line)[1:]
        elif line.startswith("!Sample_description\t"):
            descriptions = _parse_geo_row(line)[1:]
        elif line.startswith("!Sample_characteristics_ch1\t"):
            characteristic_rows.append(_parse_geo_row(line)[1:])

    if not titles or len(titles) != EXPECTED_SAMPLE_COLUMNS:
        raise ValueError(
            f"expected {EXPECTED_SAMPLE_COLUMNS} GEO sample titles, observed "
            f"{0 if not titles else len(titles)}"
        )
    if descriptions is None or len(descriptions) != len(titles):
        raise ValueError("GEO sample descriptions missing or misaligned")
    if len(set(titles)) != len(titles):
        raise ValueError("GEO sample titles are not unique")
    for row in characteristic_rows:
        if len(row) != len(titles):
            raise ValueError("GEO characteristic row width does not match sample titles")

    records = {
        title: {
            "sample_id": title,
            "description": descriptions[index],
            "characteristics": {},
        }
        for index, title in enumerate(titles)
    }

    for row in characteristic_rows:
        for index, token in enumerate(row):
            if ":" not in token:
                continue
            key, value = token.split(":", 1)
            key = _normalise_key(key)
            value = value.strip()
            if not key:
                continue
            record = records[titles[index]]
            previous = record["characteristics"].get(key)
            if previous is not None and previous != value:
                raise ValueError(
                    f"conflicting GEO characteristic {key!r} for {titles[index]}: "
                    f"{previous!r} versus {value!r}"
                )
            record["characteristics"][key] = value

    for title, record in records.items():
        chars = record["characteristics"]
        if "patient id" not in chars:
            raise ValueError(f"{title}: missing patient id")
        if "anti-pd-1 response" not in chars:
            raise ValueError(f"{title}: missing anti-pd-1 response")

        description = record["description"]
        biopsy_match = re.search(
            r"\b(\d+)(?:st|nd|rd|th)\s+biopsy\b", description, flags=re.IGNORECASE
        )
        if not biopsy_match:
            raise ValueError(f"{title}: missing biopsy ordinal in description")
        record["patient_id"] = chars["patient id"].strip()
        record["response"] = chars["anti-pd-1 response"].strip()
        record["biopsy_ordinal"] = int(biopsy_match.group(1))

        characteristic_time = chars.get("biopsy time")
        desc_lower = description.lower()
        if "pre anti-pd-1 treatment" in desc_lower:
            description_time = "pretreatment"
        elif "on anti-pd-1 treatment" in desc_lower:
            description_time = "nonpretreatment"
        else:
            description_time = None

        characteristic_class = None
        if characteristic_time is not None:
            norm = characteristic_time.strip().lower().replace("_", "-")
            if "pre" in norm:
                characteristic_class = "pretreatment"
            elif "on" in norm or "post" in norm:
                characteristic_class = "nonpretreatment"
            else:
                raise ValueError(
                    f"{title}: unrecognised biopsy time characteristic {characteristic_time!r}"
                )

        if description_time is None and characteristic_class is None:
            raise ValueError(f"{title}: no interpretable treatment timepoint")
        if (
            description_time is not None
            and characteristic_class is not None
            and description_time != characteristic_class
        ):
            raise ValueError(f"{title}: conflicting description/characteristic timepoint")

        record["timepoint"] = description_time or characteristic_class

    return records


def freeze_first_pretreatment_biopsy(records):
    by_patient = {}
    for record in records.values():
        if record["timepoint"] != "pretreatment":
            continue
        by_patient.setdefault(record["patient_id"], []).append(record)

    selected_pretreatment = set()
    later_exclusions = []
    for patient_id, patient_records in sorted(by_patient.items()):
        ordered = sorted(
            patient_records,
            key=lambda item: (item["biopsy_ordinal"], item["sample_id"]),
        )
        if len(ordered) > 1 and ordered[0]["biopsy_ordinal"] == ordered[1]["biopsy_ordinal"]:
            raise ValueError(
                f"{patient_id}: pretreatment biopsy ordinal tie prevents frozen deduplication"
            )
        selected_pretreatment.add(ordered[0]["sample_id"])
        for later in ordered[1:]:
            later_exclusions.append(
                {
                    "sample_id": later["sample_id"],
                    "patient_id": patient_id,
                    "reason": "later_pretreatment_biopsy",
                    "biopsy_ordinal": later["biopsy_ordinal"],
                }
            )

    retained = []
    for sample_id, record in records.items():
        if record["timepoint"] == "pretreatment" and sample_id not in selected_pretreatment:
            continue
        retained.append(record)
    return retained, later_exclusions


def canonical_expression_sample(raw_header):
    value = str(raw_header).strip()
    if not value:
        raise ValueError("empty expression sample header")
    return value.split(".", 1)[0]


def workbook_to_tsv(workbook_bytes, tsv_path):
    try:
        import openpyxl
    except ImportError as exc:
        raise RuntimeError("openpyxl is required for the GSE78220 audit") from exc

    with tempfile.NamedTemporaryFile(suffix=".xlsx") as handle:
        handle.write(workbook_bytes)
        handle.flush()
        workbook = openpyxl.load_workbook(handle.name, read_only=True, data_only=True)
        sheet = workbook.active
        iterator = sheet.iter_rows(values_only=True)
        try:
            header = next(iterator)
        except StopIteration as exc:
            raise ValueError("GSE78220 workbook is empty") from exc

        if not header or str(header[0]).strip().lower() != "gene":
            raise ValueError(f"first workbook column must be Gene, observed {header[0]!r}")
        samples = [canonical_expression_sample(cell) for cell in header[1:]]
        if len(samples) != EXPECTED_SAMPLE_COLUMNS:
            raise ValueError(
                f"expected {EXPECTED_SAMPLE_COLUMNS} expression samples, observed {len(samples)}"
            )
        if len(set(samples)) != len(samples):
            raise ValueError("canonical expression sample titles are not unique")

        row_count = 0
        seen_genes = set()
        with open(tsv_path, "w", encoding="utf-8", newline="") as out:
            writer = csv.writer(out, delimiter="\t", lineterminator="\n")
            writer.writerow(["gene", *samples])
            for row in iterator:
                if len(row) != len(header):
                    raise ValueError(
                        f"workbook row width {len(row)} differs from header width {len(header)}"
                    )
                gene = "" if row[0] is None else str(row[0]).strip()
                if not gene:
                    raise ValueError(f"workbook data row {row_count + 2} has empty gene")
                canonical_gene = gene.upper()
                if canonical_gene in seen_genes:
                    raise ValueError(f"duplicate gene symbol in workbook: {canonical_gene}")
                seen_genes.add(canonical_gene)
                writer.writerow([gene, *["" if value is None else value for value in row[1:]]])
                row_count += 1
        workbook.close()

    if row_count != EXPECTED_GENE_ROWS:
        raise ValueError(f"expected {EXPECTED_GENE_ROWS} gene rows, observed {row_count}")
    return {
        "gene_rows": row_count,
        "sample_columns": len(samples),
        "samples": samples,
    }


def write_frozen_manifest(records, path):
    fieldnames = ("sample_id", "patient_id", "timepoint", "response")
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames)
        writer.writeheader()
        for record in sorted(records, key=lambda item: item["sample_id"]):
            writer.writerow(
                {
                    "sample_id": record["sample_id"],
                    "patient_id": record["patient_id"],
                    "timepoint": (
                        "pretreatment" if record["timepoint"] == "pretreatment" else "on-treatment"
                    ),
                    "response": record["response"],
                }
            )


def auroc(labels, scores):
    positives = [score for label, score in zip(labels, scores) if label == 1]
    negatives = [score for label, score in zip(labels, scores) if label == 0]
    if not positives or not negatives:
        raise ValueError("AUROC requires both responder and nonresponder patients")
    concordance = 0.0
    for positive in positives:
        for negative in negatives:
            if positive > negative:
                concordance += 1.0
            elif positive == negative:
                concordance += 0.5
    return concordance / (len(positives) * len(negatives))


def average_precision(labels, scores):
    n_positive = sum(label == 1 for label in labels)
    if n_positive == 0:
        raise ValueError("average precision requires at least one responder")
    grouped = {}
    for label, score in zip(labels, scores):
        grouped.setdefault(float(score), []).append(int(label))

    tp = 0
    fp = 0
    previous_recall = 0.0
    ap = 0.0
    for score in sorted(grouped, reverse=True):
        group = grouped[score]
        tp += sum(label == 1 for label in group)
        fp += sum(label == 0 for label in group)
        recall = tp / n_positive
        precision = tp / (tp + fp)
        ap += (recall - previous_recall) * precision
        previous_recall = recall
    return ap


def stratified_auroc_bootstrap(labels, scores, iterations=5000, seed=20260906):
    positives = [score for label, score in zip(labels, scores) if label == 1]
    negatives = [score for label, score in zip(labels, scores) if label == 0]
    if not positives or not negatives:
        raise ValueError("bootstrap AUROC requires both endpoint classes")
    rng = random.Random(seed)
    boot = []
    for _ in range(iterations):
        sample_pos = [rng.choice(positives) for _ in positives]
        sample_neg = [rng.choice(negatives) for _ in negatives]
        sample_labels = [1] * len(sample_pos) + [0] * len(sample_neg)
        sample_scores = sample_pos + sample_neg
        boot.append(auroc(sample_labels, sample_scores))
    boot.sort()

    def quantile(probability):
        index = probability * (len(boot) - 1)
        low = int(math.floor(index))
        high = int(math.ceil(index))
        if low == high:
            return boot[low]
        weight = index - low
        return boot[low] * (1.0 - weight) + boot[high] * weight

    return {
        "method": "stratified_patient_bootstrap",
        "iterations": iterations,
        "seed": seed,
        "lower_95": quantile(0.025),
        "upper_95": quantile(0.975),
    }


def run_audit():
    workbook_bytes, workbook_source, workbook_sha = download_checksum_locked(
        [NCBI_WORKBOOK_URL, PINNED_MIRROR_WORKBOOK_URL],
        EXPECTED_WORKBOOK_SHA256,
    )
    series_text, series_source, series_sha = download_series_text(
        [NCBI_SERIES_URL, PINNED_MIRROR_SERIES_URL]
    )
    metadata = parse_geo_sample_metadata(series_text)
    retained_records, later_exclusions = freeze_first_pretreatment_biopsy(metadata)

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        expression_tsv = tmp_path / "expression.tsv"
        workbook_shape = workbook_to_tsv(workbook_bytes, expression_tsv)
        if set(workbook_shape["samples"]) != set(metadata):
            missing_in_expression = sorted(set(metadata) - set(workbook_shape["samples"]))
            missing_in_metadata = sorted(set(workbook_shape["samples"]) - set(metadata))
            raise ValueError(
                "expression/GEO title mismatch: "
                f"missing_in_expression={missing_in_expression}, "
                f"missing_in_metadata={missing_in_metadata}"
            )

        scored = SCORER.score_matrix(expression_tsv)

        manifest_path = tmp_path / "manifest.tsv"
        write_frozen_manifest(retained_records, manifest_path)
        manifest = MANIFEST.parse_manifest(manifest_path)

    joined = []
    for endpoint in manifest["included"]:
        sample_id = endpoint["sample_id"]
        if sample_id not in scored["samples"]:
            raise ValueError(f"included endpoint sample {sample_id} has no expression score")
        score = scored["samples"][sample_id]["s_pd1"]
        joined.append(
            {
                "sample_id": sample_id,
                "patient_id": endpoint["patient_id"],
                "y": endpoint["y"],
                "endpoint": endpoint["endpoint"],
                "s_pd1": score,
                "route_burden": scored["samples"][sample_id]["route_burden"],
            }
        )

    labels = [item["y"] for item in joined]
    scores = [item["s_pd1"] for item in joined]
    roc = auroc(labels, scores)
    ap = average_precision(labels, scores)
    roc_ci = stratified_auroc_bootstrap(labels, scores)

    expected_dedup = [
        item
        for item in later_exclusions
        if item["patient_id"] == "Pt27" and item["sample_id"] == "Pt27B"
    ]
    if len(expected_dedup) != 1:
        raise ValueError("frozen Pt27 first-biopsy rule did not exclude exactly Pt27B")
    if "Pt27A" not in {item["sample_id"] for item in joined}:
        raise ValueError("frozen Pt27 first-biopsy rule did not retain Pt27A")

    nonpretreatment_exclusions = [
        item for item in manifest["excluded"] if item["reason"] == "nonpretreatment"
    ]
    if not any(item["sample_id"] == "Pt16" for item in nonpretreatment_exclusions):
        raise ValueError("expected on-treatment sample Pt16 was not excluded")

    return {
        "status": "development_cohort_audit_only",
        "cohort": "GSE78220",
        "locked_validation_cohort_touched": False,
        "workbook": {
            "sha256": workbook_sha,
            "expected_sha256": EXPECTED_WORKBOOK_SHA256,
            "source_used": workbook_source,
            **workbook_shape,
        },
        "series_matrix": {
            "sha256": series_sha,
            "source_used": series_source,
            "sample_count": len(metadata),
        },
        "frozen_selection": {
            "rule": "earliest pretreatment biopsy ordinal per patient; selection ignores response",
            "later_pretreatment_exclusions": later_exclusions,
            "nonpretreatment_exclusions": nonpretreatment_exclusions,
        },
        "endpoint": {
            "definition": "CR_or_PR_vs_PD",
            "n_included": manifest["n_included"],
            "n_responder": manifest["n_responder"],
            "n_nonresponder": manifest["n_nonresponder"],
            "excluded": manifest["excluded"],
        },
        "feature": {
            "version": scored["feature_version"],
            "direction": "higher_s_pd1_predicts_CR_PR",
            "weights_learned_from_outcomes": False,
        },
        "development_metrics": {
            "auroc": roc,
            "auroc_95_ci": roc_ci,
            "average_precision": ap,
            "responder_prevalence": (
                manifest["n_responder"] / manifest["n_included"]
                if manifest["n_included"]
                else None
            ),
        },
        "patients": joined,
        "claim_boundary": (
            "This is a development-cohort falsification/compatibility audit only. "
            "It cannot establish a validated predictive melanoma model, treatment-selection "
            "system, clinical efficacy, or cancer cure. GSE91061 outcomes remain locked."
        ),
        "next_gate": (
            "If the frozen development score is numerically coherent, freeze any probability "
            "calibration using development data only before one-time independent GSE91061 validation."
        ),
    }


def main():
    parser = argparse.ArgumentParser(
        description="Run the frozen GSE78220 melanoma route-burden development audit."
    )
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run_audit()
    text = json.dumps(result, indent=2, sort_keys=True)
    if args.output:
        args.output.write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
