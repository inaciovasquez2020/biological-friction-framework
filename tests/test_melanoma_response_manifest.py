import importlib.util
from pathlib import Path

import pytest

MODULE_PATH = Path(__file__).resolve().parents[1] / "infra" / "ci" / "parse_melanoma_response_manifest.py"
SPEC = importlib.util.spec_from_file_location("parse_melanoma_response_manifest", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


def _write_manifest(path, rows):
    with open(path, "w", encoding="utf-8") as handle:
        handle.write("sample_id\tpatient_id\ttimepoint\tresponse\n")
        for row in rows:
            handle.write("\t".join(row) + "\n")


def test_primary_endpoint_is_cr_pr_vs_pd_and_sd_is_excluded(tmp_path):
    manifest = tmp_path / "clinical.tsv"
    _write_manifest(
        manifest,
        [
            ("s1", "p1", "pretreatment", "CR"),
            ("s2", "p2", "baseline", "partial response"),
            ("s3", "p3", "pre", "PD"),
            ("s4", "p4", "pre-treatment", "SD"),
            ("s5", "p5", "on-treatment", "CR"),
        ],
    )

    result = MODULE.parse_manifest(manifest)
    assert [(item["patient_id"], item["y"]) for item in result["included"]] == [
        ("p1", 1),
        ("p2", 1),
        ("p3", 0),
    ]
    reasons = {item["patient_id"]: item["reason"] for item in result["excluded"]}
    assert reasons["p4"] == "excluded_nonprimary_endpoint"
    assert reasons["p5"] == "nonpretreatment"
    assert result["n_responder"] == 2
    assert result["n_nonresponder"] == 1


def test_duplicate_pretreatment_patient_fails_closed_before_endpoint_selection(tmp_path):
    manifest = tmp_path / "duplicate.tsv"
    _write_manifest(
        manifest,
        [
            ("s1", "p1", "pretreatment", "CR"),
            ("s2", "p1", "pretreatment", "PD"),
        ],
    )

    with pytest.raises(ValueError, match="duplicate pretreatment patient_id"):
        MODULE.parse_manifest(manifest)


def test_duplicate_sample_id_fails_closed(tmp_path):
    manifest = tmp_path / "duplicate_sample.tsv"
    _write_manifest(
        manifest,
        [
            ("s1", "p1", "pretreatment", "CR"),
            ("s1", "p2", "on-treatment", "PD"),
        ],
    )

    with pytest.raises(ValueError, match="duplicate sample_id"):
        MODULE.parse_manifest(manifest)


def test_unrecognised_response_or_timepoint_is_not_silently_reclassified(tmp_path):
    bad_response = tmp_path / "bad_response.tsv"
    _write_manifest(bad_response, [("s1", "p1", "pretreatment", "almost response")])
    with pytest.raises(ValueError, match="unrecognised response"):
        MODULE.parse_manifest(bad_response)

    bad_timepoint = tmp_path / "bad_timepoint.tsv"
    _write_manifest(bad_timepoint, [("s1", "p1", "cycle 2", "CR")])
    with pytest.raises(ValueError, match="unrecognised timepoint"):
        MODULE.parse_manifest(bad_timepoint)


def test_required_columns_are_strict(tmp_path):
    manifest = tmp_path / "missing.tsv"
    manifest.write_text("sample_id\tpatient_id\tresponse\ns1\tp1\tCR\n", encoding="utf-8")
    with pytest.raises(ValueError, match="missing required columns"):
        MODULE.parse_manifest(manifest)
