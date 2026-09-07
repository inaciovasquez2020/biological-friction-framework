import importlib.util
import inspect
from pathlib import Path

import pytest

MODULE_PATH = Path(__file__).resolve().parents[1] / "infra" / "ci" / "score_melanoma_route_burden_v2.py"
SPEC = importlib.util.spec_from_file_location("score_melanoma_route_burden_v2", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


def _write_matrix(path):
    rows = [
        ("KDM5B", 1, 2, 3, 4, -1),
        ("CD36", 1, 2, 3, 4, -1),
        ("MITF", 1, 2, 3, 4, -1),
        ("MTHFD2", 1, 2, 3, 4, -1),
        ("NGFR", 1, 2, 3, 4, -1),
        ("NT5E", 1, 2, 3, 4, -1),
        ("SOX10", 3, 2, 1, 0, 4),
    ]
    with open(path, "w", encoding="utf-8") as handle:
        handle.write("gene\td1\td2\td3\te_high\te_low\n")
        for gene, *values in rows:
            handle.write(gene + "\t" + "\t".join(str(value) for value in values) + "\n")


def test_fit_reference_is_outcome_blind_and_exact(tmp_path):
    matrix = tmp_path / "expression.tsv"
    _write_matrix(matrix)
    reference = MODULE.fit_reference(matrix, ["d1", "d2", "d3"])

    assert reference["reference_samples"] == ["d1", "d2", "d3"]
    assert reference["route_reference"]["KDM5B"] == [1.0, 2.0, 3.0]
    assert reference["route_reference"]["SOX10"] == [1.0, 2.0, 3.0]
    assert list(inspect.signature(MODULE.fit_reference).parameters) == ["path", "reference_samples"]
    assert "outcome" not in inspect.signature(MODULE.score_matrix).parameters


def test_ecdf_midrank_and_signed_sox10(tmp_path):
    matrix = tmp_path / "expression.tsv"
    _write_matrix(matrix)
    reference = MODULE.fit_reference(matrix, ["d1", "d2", "d3"])
    scored = MODULE.score_matrix(matrix, reference, ["d1", "d2", "d3"])["samples"]

    assert scored["d1"]["route_ecdf"]["KDM5B"] == pytest.approx(1 / 6)
    assert scored["d2"]["route_ecdf"]["KDM5B"] == pytest.approx(1 / 2)
    assert scored["d3"]["route_ecdf"]["KDM5B"] == pytest.approx(5 / 6)

    assert scored["d1"]["route_ecdf"]["SOX10"] == pytest.approx(5 / 6)
    assert scored["d1"]["signed_spokes"]["SOX10"] == pytest.approx(1 / 6)
    assert scored["d3"]["signed_spokes"]["SOX10"] == pytest.approx(5 / 6)


def test_external_samples_reuse_frozen_reference(tmp_path):
    matrix = tmp_path / "expression.tsv"
    _write_matrix(matrix)
    reference = MODULE.fit_reference(matrix, ["d1", "d2", "d3"])

    high = MODULE.score_matrix(matrix, reference, ["e_high"])["samples"]["e_high"]
    low = MODULE.score_matrix(matrix, reference, ["e_low"])["samples"]["e_low"]

    assert high["route_ecdf"]["KDM5B"] == pytest.approx(1.0)
    assert high["signed_spokes"]["SOX10"] == pytest.approx(1.0)
    assert high["route_burden_v2"] == pytest.approx(1.0)
    assert high["s_pd1_v2"] == pytest.approx(0.0)

    assert low["route_ecdf"]["KDM5B"] == pytest.approx(0.0)
    assert low["signed_spokes"]["SOX10"] == pytest.approx(0.0)
    assert low["route_burden_v2"] == pytest.approx(0.0)
    assert low["s_pd1_v2"] == pytest.approx(1.0)

    # Scoring external samples cannot alter the frozen development reference.
    assert reference["route_reference"]["KDM5B"] == [1.0, 2.0, 3.0]


def test_missing_route_gene_fails_closed(tmp_path):
    matrix = tmp_path / "missing.tsv"
    matrix.write_text(
        "gene\td1\nKDM5B\t1\nCD36\t1\nMITF\t1\nMTHFD2\t1\nNGFR\t1\nNT5E\t1\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="missing frozen route genes"):
        MODULE.fit_reference(matrix, ["d1"])


def test_reference_version_or_direction_drift_fails_closed(tmp_path):
    matrix = tmp_path / "expression.tsv"
    _write_matrix(matrix)
    reference = MODULE.fit_reference(matrix, ["d1", "d2", "d3"])

    bad_version = dict(reference)
    bad_version["feature_version"] = "other"
    with pytest.raises(ValueError, match="feature version mismatch"):
        MODULE.score_matrix(matrix, bad_version, ["e_high"])

    bad_direction = dict(reference)
    bad_direction["route_directions"] = dict(reference["route_directions"])
    bad_direction["route_directions"]["SOX10"] = "high"
    with pytest.raises(ValueError, match="route directions mismatch"):
        MODULE.score_matrix(matrix, bad_direction, ["e_high"])
