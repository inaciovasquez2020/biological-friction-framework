import importlib.util
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "infra" / "ci" / "develop_melanoma_rank_v5.py"
SPEC = importlib.util.spec_from_file_location("melanoma_rank_v5_test_module", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_rank_vector_is_monotone_scale_invariant_and_tie_aware():
    genes = ["A", "B", "C", "D"]
    expression = {"A": 8.0, "B": 4.0, "C": 4.0, "D": 1.0}
    scaled = {gene: value * 17.0 for gene, value in expression.items()}
    ranks = MODULE.rank_vector(expression, genes)
    assert ranks == MODULE.rank_vector(scaled, genes)
    assert ranks[0] > ranks[1] == ranks[2] > ranks[3]


def test_fixed_ridge_logistic_fit_and_prediction():
    features = []
    labels = []
    for i in range(80):
        y = int(i >= 40)
        row = [float(y) + ((i % 3) - 1) * 0.01]
        row.extend(float((i + j) % 5) / 5 for j in range(1, 12))
        features.append(row)
        labels.append(y)
    model, receipt = MODULE.fit_model(features, labels)
    probabilities = MODULE.predict(model, features)
    assert receipt["gene_count"] == 12
    assert len(probabilities) == 80
    assert MODULE.REO.auc(labels, probabilities) > 0.9
