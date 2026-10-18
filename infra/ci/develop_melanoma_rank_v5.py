#!/usr/bin/env python3
"""Rank-vector ridge-logistic candidate trained on Liu + Gide and tested on GSE93157.

The GSE93157 outcomes are never used for feature selection, tuning, or calibration.
This is research-only and must not be used for treatment decisions.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import numpy as np
from scipy.stats import rankdata
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parent
REO_V4_PATH = ROOT / "develop_melanoma_reo_v4.py"
MODEL_VERSION = "MELANOMA_PANEL_RANK_RIDGE_V5_2026_10_18"
LOGISTIC_C = 0.1
MIN_COMMON_GENES = 100


def _load_reo_v4():
    spec = importlib.util.spec_from_file_location("melanoma_reo_v5_data_sources", REO_V4_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load the pinned cohort parsers")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


REO = _load_reo_v4()


def rank_vector(expression: dict[str, float], genes: list[str]) -> list[float]:
    if not genes or any(gene not in expression for gene in genes):
        raise ValueError("rank vector requires every frozen panel gene")
    values = np.asarray([float(expression[gene]) for gene in genes], dtype=float)
    if not np.isfinite(values).all():
        raise ValueError("rank vector input contains non-finite expression values")
    return (rankdata(values, method="average") / len(genes)).tolist()


def rank_matrix(rows, genes):
    return np.asarray([rank_vector(row["expression"], genes) for row in rows], dtype=float)


def fit_model(features, labels):
    features = np.asarray(features, dtype=float)
    labels = np.asarray(labels, dtype=int)
    if features.ndim != 2 or len(features) != len(labels) or len(set(labels.tolist())) != 2:
        raise ValueError("rank ridge model requires aligned features and both endpoint classes")
    model = make_pipeline(
        StandardScaler(),
        LogisticRegression(
            penalty="l2",
            C=LOGISTIC_C,
            solver="liblinear",
            max_iter=10000,
            random_state=20261018,
        ),
    )
    model.fit(features, labels)
    classifier = model.named_steps["logisticregression"]
    scaler = model.named_steps["standardscaler"]
    return model, {
        "model_type": "per-sample gene ranks + training-standardized L2 logistic regression",
        "gene_count": int(features.shape[1]),
        "logistic_C_fixed_before_validation": LOGISTIC_C,
        "standardization": "training cohort mean and standard deviation",
        "intercept": float(classifier.intercept_[0]),
        "coefficients": classifier.coef_[0].tolist(),
        "feature_means": scaler.mean_.tolist(),
        "feature_scales": scaler.scale_.tolist(),
        "converged_iterations": classifier.n_iter_.tolist(),
    }


def predict(model, features):
    return model.predict_proba(np.asarray(features, dtype=float))[:, 1].tolist()


def _screen(metrics):
    return {
        "auroc_point_estimate_gt_0_5": metrics["auroc"] > 0.5,
        "auroc_ci_lower_gt_0_5": metrics["auroc_95_ci"]["lower_95"] > 0.5,
        "brier_better_than_prevalence_baseline": metrics["brier_beats_prevalence_baseline"],
        "balanced_accuracy_gt_0_5": metrics["balanced_accuracy_at_0_5"] > 0.5,
        "passed_single_cohort_screen": (
            metrics["auroc"] > 0.5
            and metrics["auroc_95_ci"]["lower_95"] > 0.5
            and metrics["brier_beats_prevalence_baseline"]
            and metrics["balanced_accuracy_at_0_5"] > 0.5
        ),
    }


def run_development():
    validation, panel_genes, validation_sources = REO._read_gse93157()
    if not validation_sources["eligibility"]["eligible_for_prespecified_external_screen"]:
        return {
            "status": "STOPPED_NO_ELIGIBLE_EXTERNAL_COHORT",
            "model_version": MODEL_VERSION,
            "external_validation_cohort": {
                "name": "GSE93157 melanoma pre-anti-PD-1 (baseline and archival)",
                "source": validation_sources,
                "sample_count": len(validation),
            },
            "claim_boundary": "No model fitted because the external cohort is ineligible.",
        }

    liu, liu_genes, liu_sources = REO._read_liu(panel_genes)
    gide, gide_genes, gide_sources = REO._read_gide(panel_genes)
    genes = sorted(panel_genes & liu_genes & gide_genes)
    if len(genes) < MIN_COMMON_GENES:
        raise ValueError(f"only {len(genes)} common genes; require at least {MIN_COMMON_GENES}")
    training = liu + gide
    train_x = rank_matrix(training, genes)
    train_y = [row["y"] for row in training]
    validation_x = rank_matrix(validation, genes)
    validation_y = [row["y"] for row in validation]

    model, model_receipt = fit_model(train_x, train_y)
    train_probabilities = predict(model, train_x)
    validation_probabilities = predict(model, validation_x)
    train_metrics = REO.calculate_metrics(train_y, train_probabilities)
    validation_metrics = REO.calculate_metrics(validation_y, validation_probabilities)

    # Prespecified cross-cohort transport checks use no GSE93157 outcomes.
    liu_x = rank_matrix(liu, genes)
    gide_x = rank_matrix(gide, genes)
    liu_y = [row["y"] for row in liu]
    gide_y = [row["y"] for row in gide]
    liu_only_model, liu_only_receipt = fit_model(liu_x, liu_y)
    gide_on_liu_model = predict(liu_only_model, gide_x)
    gide_on_liu_metrics = REO.calculate_metrics(gide_y, gide_on_liu_model)
    gide_only_model, gide_only_receipt = fit_model(gide_x, gide_y)
    liu_on_gide_model = predict(gide_only_model, liu_x)
    liu_on_gide_metrics = REO.calculate_metrics(liu_y, liu_on_gide_model)

    identifier_collisions = sorted(set(row["patient_id"] for row in training) & set(row["patient_id"] for row in validation))
    identifier_overlap_note = (
        "Patient identifiers are cohort-local; strings such as Patient42 recur across source studies "
        "and cannot establish person-level overlap. The source studies are distinct, but no global "
        "person-level crosswalk is available to prove absence of overlap."
    )

    return {
        "status": "RANK_V5_DEVELOPMENT_AND_GSE93157_TEST_COMPLETE",
        "model_version": MODEL_VERSION,
        "development_cohorts": {
            "Liu_DFCI": {"sample_count": len(liu), "responders": sum(liu_y), "source": liu_sources},
            "Gide_PRJEB23709": {"sample_count": len(gide), "responders": sum(gide_y), "source": gide_sources},
            "combined_sample_count": len(training),
            "endpoint": "CR/PR versus PD; SD/mixed/unknown excluded",
        },
        "external_validation_cohort": {
            "name": "GSE93157 melanoma pre-anti-PD-1 (baseline and archival)",
            "source": validation_sources,
            "sample_count": len(validation),
            "metrics": validation_metrics,
            "promotion_screen": _screen(validation_metrics),
            "patient_overlap_with_training": "NOT_PROVEN_BY_GLOBAL_IDENTIFIER",
            "cohort_local_identifier_collisions": identifier_collisions,
            "overlap_audit_note": identifier_overlap_note,
            "timing_note": "Both baseline and archival tissue are pre-treatment; archival tissue was collected >3 months before therapy.",
        },
        "cross_cohort_transport_checks": {
            "fit_Liu_test_Gide": {
                "training_n": len(liu),
                "test_n": len(gide),
                "metrics": gide_on_liu_metrics,
                "model_parameters": liu_only_receipt,
            },
            "fit_Gide_test_Liu": {
                "training_n": len(gide),
                "test_n": len(liu),
                "metrics": liu_on_gide_metrics,
                "model_parameters": gide_only_receipt,
            },
            "note": "These are internal transport checks; they are not additional independent clinical validations.",
        },
        "feature_space": {
            "common_gene_count": len(genes),
            "genes": genes,
            "representation": "within-sample average ranks scaled to (0,1)",
        },
        "model_parameters": model_receipt,
        "development_apparent_metrics_not_for_claims": train_metrics,
        "claim_boundary": (
            "Research-stage candidate only. This is one small external cohort with a cross-platform assay. "
            "No clinical utility, treatment-selection benefit, prospective validity, or patient outcome "
            "improvement is established. Do not use to select or withhold therapy."
        ),
    }


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Fit a rank-vector ridge model and test on GSE93157.")
    parser.add_argument("--output", type=Path, default=Path("melanoma-rank-v5-receipt.json"))
    args = parser.parse_args()
    result = run_development()
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    summary = {
        "status": result["status"],
        "model_version": result["model_version"],
        "receipt": str(args.output),
    }
    if result["status"] == "RANK_V5_DEVELOPMENT_AND_GSE93157_TEST_COMPLETE":
        summary["common_gene_count"] = result["feature_space"]["common_gene_count"]
        summary["external_validation_metrics"] = result["external_validation_cohort"]["metrics"]
        summary["external_promotion_screen"] = result["external_validation_cohort"]["promotion_screen"]
        summary["cross_cohort_transport_metrics"] = {
            name: item["metrics"] for name, item in result["cross_cohort_transport_checks"].items()
            if isinstance(item, dict) and "metrics" in item
        }
    else:
        summary["external_validation_cohort"] = result["external_validation_cohort"]
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
