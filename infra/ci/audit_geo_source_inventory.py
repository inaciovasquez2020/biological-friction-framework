#!/usr/bin/env python3
"""Download and inventory public GEO source files; no model fitting or preprocessing."""
from __future__ import annotations
import argparse, gzip, hashlib, json, re, tarfile, tempfile, urllib.request
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
    try:
        xml = gzip.decompress(content) if content[:2] == b"\x1f\x8b" else content
        root = ET.fromstring(xml)
        tags = Counter(el.tag.rsplit("}", 1)[-1] for el in root.iter())
        root_name = root.tag.rsplit("}", 1)[-1]
        # Report tag inventory only; do not infer assay semantics from undocumented fields.
        return {"member": member, "bytes": len(content), "sha256": hashlib.sha256(content).hexdigest(),
                "xml_root": root_name, "tag_counts": dict(tags.most_common(30)), "xml_parse": "PASS"}
    except Exception as exc:
        return {"member": member, "bytes": len(content), "sha256": hashlib.sha256(content).hexdigest(),
                "xml_parse": "FAIL", "error": str(exc)}

def audit_one(name: str, spec: dict, outdir: Path) -> dict:
    matrix_path = outdir / f"{name}_series_matrix.txt.gz"
    raw_path = outdir / f"{name}_RAW.tar"
    result = {"accession": name, "expected_samples": spec["expected_samples"]}
    result["matrix_download"] = download(spec["matrix"], matrix_path)
    result["matrix"] = matrix_inventory(matrix_path, spec["expected_samples"])
    result["raw_archive_download"] = download(spec["raw"], raw_path)
    members = []
    with tarfile.open(raw_path, "r:*") as archive:
        candidates = [m for m in archive.getmembers() if m.isfile()]
        result["archive_member_count"] = len(candidates)
        result["archive_member_names"] = [m.name for m in candidates]
        for member in candidates:
            if member.name.lower().endswith(".rcc.gz") or member.name.lower().endswith(".rcc"):
                stream = archive.extractfile(member)
                if stream is None:
                    continue
                members.append(rcc_inventory(member.name, stream.read()))
    result["rcc_file_count"] = len(members)
    result["rcc_files"] = members
    result["rcc_count_matches_expected"] = len(members) == spec["expected_samples"]
    result["status"] = "INVENTORY_COMPLETE" if result["matrix"]["sample_count_matches_expected"] and result["rcc_count_matches_expected"] else "INVENTORY_MISMATCH_REQUIRES_REVIEW"
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
        report["datasets"].append(audit_one(name, GSE[name], outdir))
    report["overall_status"] = "INVENTORY_COMPLETE" if all(d["status"] == "INVENTORY_COMPLETE" for d in report["datasets"]) else "REVIEW_REQUIRED"
    report_path = outdir / "source_inventory.json"
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"overall_status": report["overall_status"], "datasets": [
        {"accession": d["accession"], "sample_count": d["matrix"]["sample_count"],
         "rcc_file_count": d["rcc_file_count"], "status": d["status"]} for d in report["datasets"]
    ], "report": str(report_path)}, indent=2))
    if report["overall_status"] != "INVENTORY_COMPLETE":
        raise SystemExit(2)

if __name__ == "__main__":
    main()
