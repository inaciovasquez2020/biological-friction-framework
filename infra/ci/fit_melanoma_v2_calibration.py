import argparse
import importlib.util
import json
import math
from pathlib import Path

AUDIT_PATH = Path(__file__).resolve().with_name("audit_gse78220_v2_development.py")
FEATURE_VERSION = "MELANOMA_ROUTE_BURDEN_V2_DEFINITION_2026_09_06"
CALIBRATION_VERSION = "MELANOMA_V2_LOGISTIC_CALIBRATION_2026_09_06"
MAX_ITER = 100
STEP_TOL = 1e-12
GRAD_TOL = 1e-10
MIN_INFO_DET = 1e-14
DECISION_THRESHOLD = 0.5


def _load_audit_module():
    spec = importlib.util.spec_from_file_location("audit_gse78220_v2_for_calibration", AUDIT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load frozen v2 development audit")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sigmoid(value):
    value = float(value)
    if not math.isfinite(value):
        raise ValueError("logistic linear predictor must be finite")
    if value >= 0.0:
        return 1.0 / (1.0 + math.exp(-value))
    exp_value = math.exp(value)
    return exp_value / (1.0 + exp_value)


def _validate_xy(scores, labels):
    if len(scores) != len(labels) or len(scores) < 3:
        raise ValueError("scores and labels must be aligned with >=3 observations")
    xs = [float(value) for value in scores]
    ys = [int(value) for value in labels]
    if not all(math.isfinite(value) for value in xs):
        raise ValueError("scores must be finite")
    if any(value not in (0, 1) for value in ys):
        raise ValueError("labels must be binary")
    positives = sum(ys)
    negatives = len(ys) - positives
    if positives == 0 or negatives == 0:
        raise ValueError("calibration requires both endpoint classes")
    if max(xs) == min(xs):
        raise ValueError("calibration score has zero variation")
    return xs, ys


def logistic_nll(scores, labels, intercept, slope):
    xs, ys = _validate_xy(scores, labels)
    total = 0.0
    for x, y in zip(xs, ys):
        eta = intercept + slope * x
        # Stable Bernoulli negative log-likelihood: log(1+exp(eta)) - y*eta.
        if eta >= 0.0:
            softplus = eta + math.log1p(math.exp(-eta))
        else:
            softplus = math.log1p(math.exp(eta))
        total += softplus - y * eta
    return total


def fit_logistic_calibration(scores, labels):
    """Deterministic unpenalized 2-parameter logistic MLE by Newton/IRLS."""
    xs, ys = _validate_xy(scores, labels)
    prevalence = sum(ys) / len(ys)
    intercept = math.log(prevalence / (1.0 - prevalence))
    slope = 0.0
    converged = False
    final_grad = None
    final_det = None

    for iteration in range(1, MAX_ITER + 1):
        probabilities = [sigmoid(intercept + slope * x) for x in xs]
        weights = [p * (1.0 - p) for p in probabilities]

        g0 = sum(y - p for y, p in zip(ys, probabilities))
        g1 = sum((y - p) * x for x, y, p in zip(xs, ys, probabilities))

        h00 = sum(weights)
        h01 = sum(w * x for w, x in zip(weights, xs))
        h11 = sum(w * x * x for w, x in zip(weights, xs))
        det = h00 * h11 - h01 * h01
        if not math.isfinite(det) or det <= MIN_INFO_DET:
            raise ValueError("calibration information matrix is singular or non-finite")

        delta_intercept = (h11 * g0 - h01 * g1) / det
        delta_slope = (-h01 * g0 + h00 * g1) / det
        if not math.isfinite(delta_intercept) or not math.isfinite(delta_slope):
            raise ValueError("calibration Newton step is non-finite")

        intercept += delta_intercept
        slope += delta_slope
        if not math.isfinite(intercept) or not math.isfinite(slope):
            raise ValueError("calibration coefficients became non-finite")

        final_grad = max(abs(g0), abs(g1))
        final_det = det
        if max(abs(delta_intercept), abs(delta_slope)) <= STEP_TOL:
            # Recompute score equations at the updated coefficients before certifying convergence.
            updated = [sigmoid(intercept + slope * x) for x in xs]
            ug0 = sum(y - p for y, p in zip(ys, updated))
            ug1 = sum((y - p) * x for x, y, p in zip(xs, ys, updated))
            final_grad = max(abs(ug0), abs(ug1))
            if final_grad <= GRAD_TOL:
                converged = True
                break

    if not converged:
        raise ValueError("calibration logistic MLE did not converge under frozen tolerances")

    probabilities = [sigmoid(intercept + slope * x) for x in xs]
    nll = logistic_nll(xs, ys, intercept, slope)
    brier = sum((p - y) ** 2 for p, y in zip(probabilities, ys)) / len(ys)
    predictions = [1 if p >= DECISION_THRESHOLD else 0 for p in probabilities]
    tp = sum(y == 1 and pred == 1 for y, pred in zip(ys, predictions))
    fn = sum(y == 1 and pred == 0 for y, pred in zip(ys, predictions))
    tn = sum(y == 0 and pred == 0 for y, pred in zip(ys, predictions))
    fp = sum(y == 0 and pred == 1 for y, pred in zip(ys, predictions))
    sensitivity = tp / (tp + fn)
    specificity = tn / (tn + fp)
    balanced_accuracy = 0.5 * (sensitivity + specificity)

    return {
        "intercept": intercept,
        "slope": slope,
        "iterations": iteration,
        "converged": True,
        "max_abs_score_equation": final_grad,
        "information_determinant_last_iteration": final_det,
        "negative_log_likelihood": nll,
        "development_brier": brier,
        "development_balanced_accuracy_at_0_5": balanced_accuracy,
        "development_sensitivity_at_0_5": sensitivity,
        "development_specificity_at_0_5": specificity,
        "decision_threshold": DECISION_THRESHOLD,
        "solver": {
            "method": "unpenalized_two_parameter_logistic_newton_irls",
            "max_iter": MAX_ITER,
            "step_tol": STEP_TOL,
            "gradient_tol": GRAD_TOL,
            "min_information_determinant": MIN_INFO_DET,
            "initial_intercept": "logit(development_responder_prevalence)",
            "initial_slope": 0.0,
        },
    }


def run_fit():
    audit_module = _load_audit_module()
    audit = audit_module.run_audit()
    if audit.get("decision") != "CONTINUE_TO_CALIBRATION_FREEZE_BEFORE_GSE91061":
        raise ValueError("frozen v2 development continuation screen did not pass")
    if audit.get("locked_validation_cohort_touched") is not False:
        raise ValueError("locked validation cohort was touched before calibration freeze")
    if audit["feature"]["version"] != FEATURE_VERSION:
        raise ValueError("v2 feature version drifted before calibration")

    patients = audit["patients"]
    scores = [item["s_pd1_v2"] for item in patients]
    labels = [item["y"] for item in patients]
    fit = fit_logistic_calibration(scores, labels)
    if fit["slope"] <= 0.0:
        raise ValueError("calibration slope is not positive despite frozen higher-score response direction")

    return {
        "status": "development_only_calibration_frozen",
        "calibration_version": CALIBRATION_VERSION,
        "feature_version": FEATURE_VERSION,
        "development_cohort": "GSE78220",
        "locked_validation_cohort": "GSE91061_PRETREATMENT",
        "locked_validation_cohort_touched": False,
        "endpoint": "CR_or_PR_vs_PD",
        "source_provenance": {
            "workbook_sha256": audit["workbook"]["sha256"],
            "workbook_expected_sha256": audit["workbook"]["expected_sha256"],
            "series_matrix_sha256": audit["series_matrix"]["sha256"],
            "reference_samples": audit["frozen_selection"]["reference_samples"],
            "route_reference": audit["feature"]["reference"],
        },
        "development_screen": {
            "auroc": audit["development_metrics"]["auroc"],
            "auroc_95_ci": audit["development_metrics"]["auroc_95_ci"],
            "average_precision": audit["development_metrics"]["average_precision"],
            "responder_prevalence": audit["development_metrics"]["responder_prevalence"],
            "continuation_screen": audit["continuation_screen"],
        },
        "calibration": fit,
        "patient_count": len(patients),
        "responder_count": sum(labels),
        "nonresponder_count": len(labels) - sum(labels),
        "validation_rule": {
            "probability": "sigmoid(intercept + slope * S_PD1_v2)",
            "classify_responder_if_probability_gte": DECISION_THRESHOLD,
            "no_validation_refit": True,
        },
        "claim_boundary": (
            "Development-only calibration coefficients and the 0.5 decision threshold are frozen. "
            "No GSE91061 outcome has been accessed, and no retrospective predictive validation, "
            "treatment selection, clinical efficacy, or cancer cure is established."
        ),
    }


def main():
    parser = argparse.ArgumentParser(description="Fit and freeze melanoma v2 development-only logistic calibration.")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run_fit()
    text = json.dumps(result, indent=2, sort_keys=True)
    if args.output:
        args.output.write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
