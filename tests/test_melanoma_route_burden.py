import importlib.util
import inspect
from pathlib import Path

import pytest

MODULE_PATH = Path(__file__).resolve().parents[1] / "infra" / "ci" / "score_melanoma_route_burden.py"
SPEC = importlib.util.spec_from_file_location("score_melanoma_route_burden", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


def _write_matrix(path, omit=None):
    rows = [
        ("A", 0, 0),
        ("KDM5B", 6, 1),
        ("CD36", 5, 2),
        ("MITF", 4, 3),
        ("MTHFD2", 3, 4),
        ("NGFR", 2, 5),
        ("NT5E", 1, 6),
        ("SOX10", 0, 7),
        ("Z", 7, 0),
    ]
    with open(path, "w", encoding="utf-8") as handle:
        handle.write("gene\tsample_a\tsample_b\n")
        for gene, a, b in rows:
            if gene == omit:
                continue
            handle.write(f"{gene}\t{a}\t{b}\n")


def test_frozen_score_matches_midrank_and_signed_sox10(tmp_path):
    matrix = tmp_path / "expression.tsv"
    _write_matrix(matrix)

    result = MODULE.score_matrix(matrix)
    sample_a = result["samples"]["sample_a"]
    sample_b = result["samples"]["sample_b"]

    # sample_a has two genes tied at expression 0, so SOX10 midrank is 1/9.
    assert sample_a["route_percentiles"]["SOX10"] == pytest.approx(1 / 9)
    assert sample_a["signed_spokes"]["SOX10"] == pytest.approx(8 / 9)
    assert sample_a["route_burden"] == pytest.approx(8 / 9)
    assert sample_a["s_pd1"] == pytest.approx(1 / 9)

    # sample_b's largest signed spoke is NT5E at expression 6: 7.5/9.
    assert sample_b["route_burden"] == pytest.approx(7.5 / 9)
    assert sample_b["s_pd1"] == pytest.approx(1.5 / 9)


def test_score_is_invariant_under_strictly_increasing_affine_transform(tmp_path):
    matrix = tmp_path / "expression.tsv"
    _write_matrix(matrix)
    baseline = MODULE.score_matrix(matrix)

    transformed = tmp_path / "transformed.tsv"
    with open(matrix, "r", encoding="utf-8") as src, open(transformed, "w", encoding="utf-8") as dst:
        header = src.readline()
        dst.write(header)
        for line in src:
            gene, a, b = line.rstrip("\n").split("\t")
            dst.write(f"{gene}\t{3 * float(a) + 11}\t{3 * float(b) + 11}\n")

    shifted = MODULE.score_matrix(transformed)
    assert shifted["samples"] == baseline["samples"]


def test_missing_frozen_route_gene_fails_closed(tmp_path):
    matrix = tmp_path / "missing.tsv"
    _write_matrix(matrix, omit="NT5E")

    with pytest.raises(ValueError, match="missing frozen route genes"):
        MODULE.score_matrix(matrix)


def test_public_interface_has_no_outcome_argument():
    assert list(inspect.signature(MODULE.score_matrix).parameters) == ["path"]
    assert "outcome" not in inspect.signature(MODULE.score_sample).parameters
