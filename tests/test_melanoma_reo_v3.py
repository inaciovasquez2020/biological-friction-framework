import importlib.util
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "infra" / "ci" / "develop_melanoma_reo_v3.py"
SPEC = importlib.util.spec_from_file_location("melanoma_reo_v3_test_module", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_pair_feature_count_order_and_ties():
    expression = {
        "KDM5B": 8.0,
        "CD36": 4.0,
        "MITF": 4.0,
        "MTHFD2": 2.0,
        "NGFR": 1.0,
        "NT5E": 3.0,
        "SOX10": 0.0,
    }
    features = MODULE.pair_features(expression)
    assert len(features) == 21
    assert features[0] == 1.0
    assert features[1] == 1.0
    assert features[2] == 1.0
    assert features[3] == 1.0
    assert features[4] == 1.0
    assert features[5] == 1.0
    assert features[6] == 1.0
    assert features[7] == 1.0
    assert features[8] == 1.0
    assert features[9] == 1.0
    assert features[10] == 1.0
    assert features[11] == 1.0
    assert features[12] == 1.0
    assert features[13] == 1.0
    assert features[14] == 1.0
    assert features[15] == 1.0
    assert features[16] == 1.0
    assert features[17] == 1.0
    assert features[18] == 1.0
    assert features[19] == 1.0
    assert features[20] == 1.0


def test_pair_feature_input_fails_closed():
    try:
        MODULE.pair_features({"KDM5B": 1.0})
    except ValueError as exc:
        assert "exactly the frozen seven genes" in str(exc)
    else:
        raise AssertionError("partial gene set must fail")


def test_ridge_logistic_fit_and_prediction_are_finite():
    features = []
    labels = []
    for i in range(60):
        label = int(i >= 30)
        row = [float(label)]
        row.extend(float((i + j) % 2) for j in range(1, len(MODULE.PAIRS)))
        features.append(row)
        labels.append(label)
    model = MODULE.fit_ridge_logistic(features, labels)
    probabilities = MODULE.predict_probability(features, model)
    assert model["converged"] is True
    assert len(probabilities) == 60
    assert all(0.0 < value < 1.0 for value in probabilities)
    assert MODULE.auc(labels, probabilities) > 0.95


def test_metrics_report_baseline_and_ci():
    labels = [1, 1, 1, 0, 0, 0]
    probabilities = [0.8, 0.7, 0.6, 0.4, 0.3, 0.2]
    result = MODULE.metrics(labels, probabilities)
    assert result["auroc"] == 1.0
    assert result["balanced_accuracy_at_0_5"] == 1.0
    assert result["brier"] < result["prevalence_only_brier"]
    assert result["auroc_95_ci"]["lower_95"] <= 1.0
    assert result["auroc_95_ci"]["upper_95"] == 1.0
