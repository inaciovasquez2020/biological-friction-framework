import importlib.util
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "infra" / "ci" / "develop_melanoma_reo_v4.py"
SPEC = importlib.util.spec_from_file_location("melanoma_reo_v4_test_module", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def _synthetic_training():
    rows = []
    for cohort, n_per_class in (("Liu_DFCI", 20), ("Gide_PRJEB23709", 10)):
        for y in (0, 1):
            for i in range(n_per_class):
                rows.append({
                    "cohort": cohort,
                    "sample_id": f"{cohort}_{y}_{i}",
                    "patient_id": f"{cohort}_{y}_{i}",
                    "y": y,
                    "expression": {
                        "A": 10.0 if y else 0.0,
                        "B": 1.0,
                        "C": 2.0,
                        "D": 3.0,
                        "E": 4.0,
                    },
                })
    return rows


def test_pair_selection_requires_same_direction_across_training_cohorts():
    rows = _synthetic_training()
    selected, receipt = MODULE.select_pairs(rows, ["A", "B", "C", "D", "E"], {})
    assert len(selected) >= 3
    assert receipt["tested_pair_count"] == 10
    assert all(pair["delta_liu"] * pair["delta_gide"] > 0 for pair in selected)


def test_ridge_logistic_predicts_synthetic_ordering_signal():
    rows = _synthetic_training()
    selected, _ = MODULE.select_pairs(rows, ["A", "B", "C", "D", "E"], {})
    features = [MODULE.pair_features(row["expression"], selected) for row in rows]
    labels = [row["y"] for row in rows]
    model = MODULE.fit_ridge_logistic(features, labels)
    probabilities = MODULE.predict_probability(features, model)
    assert model["converged"] is True
    assert MODULE.auc(labels, probabilities) > 0.95


def test_metric_baseline_is_reported():
    result = MODULE.calculate_metrics([1, 1, 0, 0], [0.8, 0.7, 0.2, 0.3])
    assert result["auroc"] == 1.0
    assert result["brier_beats_prevalence_baseline"] is True
    assert result["auroc_95_ci"]["upper_95"] == 1.0
