import importlib.util
from pathlib import Path

import pytest

MODULE_PATH = (
    Path(__file__).resolve().parents[1]
    / "infra"
    / "ci"
    / "audit_gse78220_development.py"
)
SPEC = importlib.util.spec_from_file_location("audit_gse78220_development", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


def _synthetic_series_matrix():
    return "\n".join(
        [
            '!Sample_title\t"S1"\t"S2"\t"S3"\t"S4"',
            '!Sample_description\t'
            '"Patient 1 melanoma, pre anti-PD-1 treatment, 1st biopsy"\t'
            '"Patient 2 melanoma, on anti-PD-1 treatment, 1st biopsy"\t'
            '"Patient 3 melanoma, pre anti-PD-1 treatment, 2nd biopsy"\t'
            '"Patient 3 melanoma, pre anti-PD-1 treatment, 1st biopsy"',
            '!Sample_characteristics_ch1\t'
            '"patient id: Pt1"\t"patient id: Pt2"\t"patient id: Pt3"\t"patient id: Pt3"',
            '!Sample_characteristics_ch1\t'
            '"anti-pd-1 response: Complete Response"\t'
            '"anti-pd-1 response: Partial Response"\t'
            '"anti-pd-1 response: Progressive Disease"\t'
            '"anti-pd-1 response: Progressive Disease"',
            '!Sample_characteristics_ch1\t'
            '"biopsy time: pre-treatment"\t'
            '"biopsy time: on-treatment"\t'
            '"biopsy time: pre-treatment"\t'
            '"biopsy time: pre-treatment"',
        ]
    )


def test_metadata_freezes_first_pretreatment_biopsy_without_response_selection(monkeypatch):
    monkeypatch.setattr(MODULE, "EXPECTED_SAMPLE_COLUMNS", 4)
    records = MODULE.parse_geo_sample_metadata(_synthetic_series_matrix())
    retained, excluded = MODULE.freeze_first_pretreatment_biopsy(records)

    assert {item["sample_id"] for item in retained} == {"S1", "S2", "S4"}
    assert excluded == [
        {
            "sample_id": "S3",
            "patient_id": "Pt3",
            "reason": "later_pretreatment_biopsy",
            "biopsy_ordinal": 2,
        }
    ]


def test_expression_header_canonicalisation_is_frozen():
    assert MODULE.canonical_expression_sample("Pt27A.baseline") == "Pt27A"
    assert MODULE.canonical_expression_sample("Pt16.on-treatment") == "Pt16"


def test_auroc_uses_responder_higher_score_direction():
    labels = [1, 1, 0, 0]
    assert MODULE.auroc(labels, [0.9, 0.8, 0.2, 0.1]) == pytest.approx(1.0)
    assert MODULE.auroc(labels, [0.1, 0.2, 0.8, 0.9]) == pytest.approx(0.0)


def test_average_precision_groups_tied_scores_without_row_order_dependence():
    labels_a = [1, 0, 1, 0]
    scores_a = [0.8, 0.8, 0.4, 0.1]
    labels_b = [0, 1, 1, 0]
    scores_b = [0.8, 0.8, 0.4, 0.1]
    assert MODULE.average_precision(labels_a, scores_a) == pytest.approx(
        MODULE.average_precision(labels_b, scores_b)
    )


def test_checksum_locked_download_rejects_wrong_bytes(monkeypatch):
    monkeypatch.setattr(MODULE, "_download", lambda url: b"wrong")
    with pytest.raises(RuntimeError, match="sha256 mismatch"):
        MODULE.download_checksum_locked(["https://example.invalid/file"], "0" * 64)
