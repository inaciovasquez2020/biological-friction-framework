import importlib.util
import math
from pathlib import Path

import pytest

MODULE_PATH = Path(__file__).resolve().parents[1] / "infra" / "ci" / "fit_melanoma_v2_calibration.py"
SPEC = importlib.util.spec_from_file_location("fit_melanoma_v2_calibration", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


def test_sigmoid_is_stable_and_monotone():
    assert MODULE.sigmoid(-1000.0) == pytest.approx(0.0)
    assert MODULE.sigmoid(0.0) == pytest.approx(0.5)
    assert MODULE.sigmoid(1000.0) == pytest.approx(1.0)
    assert MODULE.sigmoid(-1.0) < MODULE.sigmoid(0.0) < MODULE.sigmoid(1.0)


def test_logistic_fit_recovers_finite_positive_direction_without_penalty():
    scores = [0.05, 0.15, 0.25, 0.40, 0.55, 0.65, 0.75, 0.90]
    labels = [0, 0, 0, 1, 0, 1, 1, 1]
    fit = MODULE.fit_logistic_calibration(scores, labels)

    assert fit["converged"] is True
    assert math.isfinite(fit["intercept"])
    assert math.isfinite(fit["slope"])
    assert fit["slope"] > 0.0
    assert fit["max_abs_score_equation"] <= MODULE.GRAD_TOL
    assert fit["decision_threshold"] == 0.5
    assert fit["solver"]["method"] == "unpenalized_two_parameter_logistic_newton_irls"


def test_fit_is_deterministic():
    scores = [0.10, 0.20, 0.35, 0.45, 0.60, 0.70, 0.80, 0.95]
    labels = [0, 0, 1, 0, 1, 1, 0, 1]
    first = MODULE.fit_logistic_calibration(scores, labels)
    second = MODULE.fit_logistic_calibration(scores, labels)
    assert first == second


def test_zero_variation_or_single_class_fails_closed():
    with pytest.raises(ValueError, match="zero variation"):
        MODULE.fit_logistic_calibration([0.5, 0.5, 0.5, 0.5], [0, 1, 0, 1])
    with pytest.raises(ValueError, match="both endpoint classes"):
        MODULE.fit_logistic_calibration([0.1, 0.2, 0.3], [1, 1, 1])


def test_nll_is_finite_for_large_linear_predictors():
    value = MODULE.logistic_nll([0.0, 1.0], [0, 1], -500.0, 1000.0)
    assert math.isfinite(value)
    assert value >= 0.0
