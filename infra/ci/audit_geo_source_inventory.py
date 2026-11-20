#!/usr/bin/env python3
"""Download and inventory public GEO source files; no model fitting or preprocessing."""
from __future__ import annotations
import argparse, gzip, hashlib, io, json, re, tarfile, tempfile, urllib.request
from collections import Counter
from pathlib import Path
import xml.etree.ElementTree as ET

GSE = {
    "GSE165745": {
        "matrix": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE165nnn/GSE165745/matrix/GSE165745_series_matrix.txt.gz",
        "raw": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE165nnn/GSE165745/suppl/GSE165745_RAW.tar",
        "expected_samples": 24,
    },
    "GSE280470": {
        "matrix": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE280nnn/GSE280470/matrix/GSE280470_series_matrix.txt.gz",
        "raw": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE280nnn/GSE280470/suppl/GSE280470_RAW.tar",
        "expected_samples": 39,
    },
}
VERSION = "GEO_SOURCE_INVENTORY_V1_2026_10_18"
RECONCILIATION_GENES = (
    "WNT2B", "WNT5A", "WNT7B", "WNT8B", "FZD1", "FZD2", "FZD4",
    "FZD5", "FZD7", "FZD8", "FZD10", "LRP5", "LRP6", "DKK2",
    "SFRP2", "SFRP4", "PYGO1", "DVL1", "RNF43",
)
RECONCILIATION_TOLERANCE = 1e-5

def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

def download(url: str, path: Path) -> dict:
    request = urllib.request.Request(url, headers={"User-Agent": VERSION})
    with urllib.request.urlopen(request, timeout=120) as response, path.open("wb") as out:
        while True:
            chunk = response.read(1024 * 1024)
            if not chunk:
                break
            out.write(chunk)
    if path.stat().st_size == 0:
        raise RuntimeError(f"Empty download: {url}")
    return {"url": url, "bytes": path.stat().st_size, "sha256": sha256(path)}

def matrix_inventory(path: Path, expected: int) -> dict:
    raw = path.read_bytes()
    if raw[:2] == b"\x1f\x8b":
        raw = gzip.decompress(raw)
    text = raw.decode("utf-8-sig")
    titles = []
    for line in text.splitlines():
        if line.startswith("!Sample_title"):
            import csv
            titles = next(csv.reader([line], delimiter="\t"))[1:]
            break
    gsm = []
    for line in text.splitlines():
        if line.startswith("!Sample_geo_accession"):
            import csv
            gsm = next(csv.reader([line], delimiter="\t"))[1:]
            break
    labels = Counter("nonresponder" if "nonresponder" in t.lower() or t.lower().startswith("nr") else "responder" if "responder" in t.lower() or t.lower().startswith("r") else "unclassified" for t in titles)
    return {"uncompressed_sha256": hashlib.sha256(raw).hexdigest(), "sample_count": len(titles),
            "titles": titles, "gsm_accessions": gsm, "title_label_counts": dict(labels),
            "expected_sample_count": expected, "sample_count_matches_expected": len(titles) == expected}

def rcc_inventory(member: str, content: bytes) -> dict:
    """Parse documented RCC Code_Summary counts; never equate them to processed GEO values."""
    raw = gzip.decompress(content) if content[:2] == b"\x1f\x8b" else content
    text = raw.decode("utf-8-sig")
    tags = Counter(re.findall(r"</?([A-Za-z_][A-Za-z0-9_]*)", text))
    root_match = re.search(r"<([A-Za-z_][A-Za-z0-9_]*)", text)
    result = {"member": member, "bytes": len(content),
              "sha256": hashlib.sha256(content).hexdigest(),
              "xml_root": root_match.group(1) if root_match else None,
              "tag_counts": dict(tags.most_common(30))}
    section = re.search(r"<Code_Summary>\s*(.*?)\s*</Code_Summary>", text, re.S)
    if section:
        import csv
        rows = list(csv.DictReader(section.group(1).splitlines()))
        required = {"CodeClass", "Name", "Accession", "Count"}
        if rows and required.issubset(set(rows[0])):
            parsed = []
            for line_number, row in enumerate(rows, start=2):
                try:
                    count = int(row["Count"])
                except (TypeError, ValueError) as exc:
                    raise ValueError(f"invalid RCC Count at Code_Summary row {line_number}") from exc
                if count < 0 or not row["Name"] or not row["Accession"]:
                    raise ValueError(f"invalid RCC gene record at Code_Summary row {line_number}")
                parsed.append({"code_class": row["CodeClass"], "name": row["Name"],
                               "accession": row["Accession"], "count": count})
            result.update({"code_summary_parse": "PASS", "code_summary_row_count": len(parsed),
                           "code_summary": parsed})
            result["xml_parse"] = "PASS"
            return result
    # Compatibility path for existing parser fixtures; a real RCC must have a valid
    # Code_Summary table to count as parsed by audit_one.
    try:
        root = ET.fromstring(raw)
        result.update({"xml_root": root.tag.rsplit("}", 1)[-1],
                       "xml_parse": "PASS", "code_summary_parse": "MISSING_OR_INVALID"})
    except Exception as exc:
        result.update({"xml_parse": "FAIL", "code_summary_parse": "MISSING_OR_INVALID",
                       "error": str(exc)})
    return result

def classify_sample_scale(raw_counts: dict[str, int], processed_values: dict[str, float]) -> dict:
    """Classify panel values as a common linear scaling or log2(raw count)+offset."""
    common = [g for g in RECONCILIATION_GENES
              if g in raw_counts and g in processed_values and raw_counts[g] > 0]
    missing = [g for g in RECONCILIATION_GENES if g not in raw_counts or g not in processed_values]
    if len(common) != len(RECONCILIATION_GENES):
        return {"scale_class": "PANEL_MAPPING_INCOMPLETE", "matched_gene_count": len(common),
                "missing_genes": missing}
    ratios = [processed_values[g] / raw_counts[g] for g in common]
    linear_factor = sorted(ratios)[len(ratios) // 2] if len(ratios) % 2 else (
        sorted(ratios)[len(ratios) // 2 - 1] + sorted(ratios)[len(ratios) // 2]
    ) / 2
    linear_residual = max(abs(processed_values[g] - raw_counts[g] * linear_factor) for g in common)
    offsets = [processed_values[g] - __import__("math").log2(raw_counts[g]) for g in common]
    log2_offset = sorted(offsets)[len(offsets) // 2] if len(offsets) % 2 else (
        sorted(offsets)[len(offsets) // 2 - 1] + sorted(offsets)[len(offsets) // 2]
    ) / 2
    log2_residual = max(abs(processed_values[g] - (__import__("math").log2(raw_counts[g]) + log2_offset))
                        for g in common)
    if linear_residual <= RECONCILIATION_TOLERANCE:
        scale_class = "LINEAR_SCALAR_MULTIPLE"
    elif log2_residual <= RECONCILIATION_TOLERANCE:
        scale_class = "LOG2_RAW_COUNT_PLUS_OFFSET"
    else:
        scale_class = "UNRESOLVED_OR_MIXED_SCALE"
    return {"scale_class": scale_class, "matched_gene_count": len(common), "missing_genes": missing,
            "linear_factor": linear_factor, "linear_max_abs_residual": linear_residual,
            "log2_offset": log2_offset, "log2_max_abs_residual": log2_residual,
            "tolerance": RECONCILIATION_TOLERANCE}


def classify_full_feature_scale(raw_counts: dict[str, int], processed_values: dict[str, float]) -> dict:
    """Classify the full shared assay using relative residuals to tolerate matrix rounding."""
    common = [g for g in raw_counts if g in processed_values and raw_counts[g] > 0]
    if len(common) < 100:
        return {"scale_class": "FEATURE_MAPPING_INCOMPLETE", "matched_feature_count": len(common)}
    ratios = [processed_values[g] / raw_counts[g] for g in common]
    factor = __import__("statistics").median(ratios)
    linear_residual = max(abs(processed_values[g] - factor * raw_counts[g]) /
                          max(1.0, abs(processed_values[g])) for g in common)
    offsets = [processed_values[g] - __import__("math").log2(raw_counts[g]) for g in common]
    offset = __import__("statistics").median(offsets)
    log_residual = max(abs(processed_values[g] - (__import__("math").log2(raw_counts[g]) + offset)) /
                       max(1.0, abs(processed_values[g])) for g in common)
    tolerance = 1e-6
    if linear_residual <= tolerance:
        scale_class = "LINEAR_SCALAR_MULTIPLE"
    elif log_residual <= tolerance:
        scale_class = "LOG2_RAW_COUNT_PLUS_OFFSET"
    else:
        scale_class = "UNRESOLVED_OR_MIXED_SCALE"
    return {"scale_class": scale_class, "matched_feature_count": len(common),
            "linear_factor": factor, "linear_max_relative_residual": linear_residual,
            "log2_offset": offset, "log2_max_relative_residual": log_residual,
            "relative_tolerance": tolerance}


def reconcile_rcc_to_matrix(matrix_path: Path, rcc_files: list[dict]) -> dict:
    """Match RCC raw counts to processed GEO values by GSM and classify per-sample scale."""
    raw = matrix_path.read_bytes()
    if raw[:2] == b"\x1f\x8b":
        raw = gzip.decompress(raw)
    lines = raw.decode("utf-8-sig").splitlines()
    import csv
    gsm = []
    for line in lines:
        if line.startswith("!Sample_geo_accession"):
            gsm = next(csv.reader([line], delimiter="\t"))[1:]
            break
    try:
        start = lines.index("!series_matrix_table_begin")
        end = lines.index("!series_matrix_table_end", start)
    except ValueError:
        return {"status": "MATRIX_TABLE_MISSING", "sample_count": len(gsm)}
    table = list(csv.reader(io.StringIO("\n".join(lines[start + 1:end])), delimiter="\t"))
    if not table or len(table[0]) != len(gsm) + 1:
        return {"status": "MATRIX_WIDTH_MISMATCH", "sample_count": len(gsm)}
    processed = {}
    for row in table[1:]:
        if len(row) != len(table[0]):
            continue
        gene = row[0].strip().strip('"').upper()
        try:
            values = [float(value) for value in row[1:]]
        except ValueError:
            continue
        processed[gene] = dict(zip(gsm, values))
    samples = []
    missing_samples = []
    for item in rcc_files:
        match = re.match(r"^(GSM\d+)_", item.get("member", ""))
        if not match:
            missing_samples.append(item.get("member"))
            continue
        accession = match.group(1)
        counts = {row["name"].upper(): row["count"] for row in item.get("code_summary", [])}
        values = {gene: processed[gene][accession] for gene in RECONCILIATION_GENES
                  if gene in processed and accession in processed[gene]}
        classified = classify_sample_scale(counts, values)
        full_values = {gene: samples[accession] for gene, samples in processed.items()
                       if accession in samples}
        full_classified = classify_full_feature_scale(counts, full_values)
        samples.append({"gsm_accession": accession, **classified,
                        "full_feature_scale": full_classified})
    classes = Counter(item["scale_class"] for item in samples)
    complete = len(gsm) == len(rcc_files) and len(samples) == len(gsm) and not missing_samples and all(
        item["matched_gene_count"] == len(RECONCILIATION_GENES) for item in samples
    )
    consistent = complete and len(classes) == 1 and next(iter(classes), None) == "LINEAR_SCALAR_MULTIPLE"
    status = "CONSISTENT_LINEAR_SCALE" if consistent else (
        "MIXED_SCALE_DETECTED" if complete and len(classes) > 1 or complete and "LOG2_RAW_COUNT_PLUS_OFFSET" in classes
        else "RECONCILIATION_INCOMPLETE"
    )
    return {"status": status, "sample_count_matrix": len(gsm), "rcc_file_count": len(rcc_files),
            "matched_sample_count": len(samples), "expected_panel_gene_count": len(RECONCILIATION_GENES),
            "matched_panel_measurements": sum(item["matched_gene_count"] for item in samples),
            "expected_panel_measurements": len(gsm) * len(RECONCILIATION_GENES),
            "scale_class_counts": dict(classes),
            "full_feature_scale_class_counts": dict(Counter(
                item["full_feature_scale"]["scale_class"] for item in samples)),
            "full_feature_sample_results": [
                {"gsm_accession": item["gsm_accession"], **item["full_feature_scale"]}
                for item in samples
            ],
            "sample_results": samples,
            "missing_rcc_sample_identifiers": missing_samples,
            "claim_boundary": "Scale classification is empirical; it does not identify the undocumented normalization procedure."}


def audit_one(name: str, spec: dict, outdir: Path) -> dict:
    matrix_path = outdir / f"{name}_series_matrix.txt.gz"
    raw_path = outdir / f"{name}_RAW.tar"
    result = {"accession": name, "expected_samples": spec["expected_samples"]}
    try:
        result["matrix_download"] = download(spec["matrix"], matrix_path)
        result["matrix"] = matrix_inventory(matrix_path, spec["expected_samples"])
    except Exception as exc:
        result["matrix_error"] = {"type": type(exc).__name__, "message": str(exc)}
    try:
        result["raw_archive_download"] = download(spec["raw"], raw_path)
        members = []
        with tarfile.open(raw_path, "r:*") as archive:
            candidates = [m for m in archive.getmembers() if m.isfile()]
            result["archive_member_count"] = len(candidates)
            result["archive_member_names"] = [m.name for m in candidates]
            for member in candidates:
                if member.name.lower().endswith(".rcc.gz") or member.name.lower().endswith(".rcc"):
                    stream = archive.extractfile(member)
                    if stream is not None:
                        members.append(rcc_inventory(member.name, stream.read()))
        result["rcc_file_count"] = len(members)
        result["rcc_files"] = members
        result["rcc_count_matches_expected"] = len(members) == spec["expected_samples"]
        if "matrix_error" not in result and "matrix" in result and all(
            item.get("code_summary_parse") == "PASS" for item in members
        ):
            result["rcc_to_matrix_reconciliation"] = reconcile_rcc_to_matrix(matrix_path, members)
    except Exception as exc:
        result["raw_archive_error"] = {"type": type(exc).__name__, "message": str(exc)}
    matrix_ok = result.get("matrix", {}).get("sample_count_matches_expected", False)
    rcc_ok = result.get("rcc_count_matches_expected", False) and all(
        item.get("code_summary_parse") == "PASS" for item in result.get("rcc_files", [])
    )
    if matrix_ok and rcc_ok:
        result["status"] = "INVENTORY_COMPLETE"
    elif "matrix_error" in result or "raw_archive_error" in result:
        result["status"] = "SOURCE_DOWNLOAD_OR_PARSE_BLOCKED"
    else:
        result["status"] = "INVENTORY_MISMATCH_REQUIRES_REVIEW"
    return result

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--outdir", default="geo-source-audit")
    parser.add_argument("--datasets", nargs="+", choices=sorted(GSE), default=["GSE165745", "GSE280470"])
    args = parser.parse_args()
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    report = {"schema_version": VERSION, "datasets": []}
    for name in args.datasets:
        try:
            report["datasets"].append(audit_one(name, GSE[name], outdir))
        except Exception as exc:
            report["datasets"].append({"accession": name, "status": "SOURCE_DOWNLOAD_OR_PARSE_BLOCKED",
                                       "error_type": type(exc).__name__, "error": str(exc)})
    report["overall_status"] = "INVENTORY_COMPLETE" if all(
        d["status"] == "INVENTORY_COMPLETE"
        and d.get("rcc_to_matrix_reconciliation", {}).get("status") == "CONSISTENT_LINEAR_SCALE"
        for d in report["datasets"]
    ) else "REVIEW_REQUIRED"
    report_path = outdir / "source_inventory.json"
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"overall_status": report["overall_status"], "datasets": [
        {"accession": d["accession"],
         "sample_count": d.get("matrix", {}).get("sample_count"),
         "rcc_file_count": d.get("rcc_file_count"),
         "status": d["status"],
         "reconciliation_status": d.get("rcc_to_matrix_reconciliation", {}).get("status"),
         "error": d.get("error")} for d in report["datasets"]
    ], "report": str(report_path)}, indent=2))
    if report["overall_status"] != "INVENTORY_COMPLETE":
        raise SystemExit(2)

if __name__ == "__main__":
    main()
