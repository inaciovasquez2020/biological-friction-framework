import importlib.util
from pathlib import Path

import pytest

MODULE_PATH = Path(__file__).resolve().parents[1] / "infra" / "ci" / "audit_gse78220_v2_development.py"
SPEC = importlib.util.spec_from_file_location("audit_gse78220_v2_development", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


def test_v2_continuation_requires_all_three_frozen_conditions():
    labels = [1, 1, 0, 0]
    scores = [0.9, 0.8, 0.2, 0.1]
    result = MODULE.development_continue(labels, scores, 0.75, 0.80)
    assert result["passed"] is True
    assert result["expected_direction_observed"] is True

    assert MODULE.development_continue(labels, scores, 0.60, 0.80)["passed"] is False
    assert MODULE.development_continue(labels, scores, 0.75, 0.50)["passed"] is False

    reversed_scores = [0.1, 0.2, 0.8, 0.9]
    result = MODULE.development_continue(labels, reversed_scores, 0.75, 0.80)
    assert result["expected_direction_observed"] is False
    assert result["passed"] is False


def test_v2_continuation_uses_strict_auroc_and_auprc_thresholds():
    labels = [1, 1, 0, 0]
    scores = [0.8, 0.7, 0.3, 0.2]
    prevalence = 0.5

    assert MODULE.development_continue(labels, scores, 0.6000001, prevalence + 1e-7)["passed"]
    assert not MODULE.development_continue(labels, scores, 0.6, prevalence + 0.1)["passed"]
    assert not MODULE.development_continue(labels, scores, 0.7, prevalence)["passed"]


def test_v2_continuation_fails_closed_on_bad_endpoint_surface():
    with pytest.raises(ValueError, match="non-empty and aligned"):
        MODULE.development_continue([1], [], 0.7, 0.7)
    with pytest.raises(ValueError, match="both endpoint classes"):
        MODULE.development_continue([1, 1], [0.8, 0.7], 0.7, 0.7)
