import argparse
import importlib.util
import json
import tempfile
from pathlib import Path

BASE_AUDIT_PATH = Path(__file__).resolve().with_name("audit_gse78220_development.py")
V2_SCORER_PATH = Path(__file__).resolve().with_name("score_melanoma_route_burden_v2.py")


def _load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to load module {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


BASE = _load_module("audit_gse78220_development_base", BASE_AUDIT_PATH)
V2 = _load_module("score_melanoma_route_burden_v2_for_audit", V2_SCORER_PATH)


def development_continue(labels, scores, auroc_value, average_precision_value):
    if len(labels) != len(scores) or not labels:
        raise ValueError("labels and scores must be non-empty and aligned")
    responders = [score for label, score in zip(labels, scores) if label == 1]
    nonresponders = [score for label, score in zip(labels, scores) if label == 0]
    if not responders or not nonresponders:
        raise ValueError("development screen requires both endpoint classes")
    prevalence = len(responders) / len(labels)
    mean_responder = sum(responders) / len(responders)
    mean_nonresponder = sum(nonresponders) / len(nonresponders)
    expected_direction = mean_responder > mean_nonresponder
    passed = (
        auroc_value > 0.60
        and average_precision_value > prevalence
        and expected_direction
    )
    return {
        "thresholds": {
            "auroc_strictly_greater_than": 0.60,
            "average_precision_strictly_greater_than_responder_prevalence": True,
            "direction": "mean_S_PD1_v2_CR_PR_strictly_greater_than_mean_S_PD1_v2_PD",
        },
        "mean_responder_score": mean_responder,
        "mean_nonresponder_score": mean_nonresponder,
        "expected_direction_observed": expected_direction,
        "passed": passed,
    }


def run_audit():
    workbook_bytes, workbook_source, workbook_sha = BASE.download_checksum_locked(
        [BASE.NCBI_WORKBOOK_URL, BASE.PINNED_MIRROR_WORKBOOK_URL],
        BASE.EXPECTED_WORKBOOK_SHA256,
    )
    series_text, series_source, series_sha = BASE.download_series_text(
        [BASE.NCBI_SERIES_URL, BASE.PINNED_MIRROR_SERIES_URL]
    )
    metadata = BASE.parse_geo_sample_metadata(series_text)

    # This selection is frozen before response parsing and uses only patient/sample/time metadata.
    retained_records, later_exclusions = BASE.freeze_first_pretreatment_biopsy(metadata)
    reference_samples = sorted(
        record["sample_id"]
        for record in retained_records
        if record["timepoint"] == "pretreatment"
    )
    if not reference_samples:
        raise ValueError("frozen GSE78220 pretreatment reference is empty")

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        expression_tsv = tmp_path / "expression.tsv"
        workbook_shape = BASE.workbook_to_tsv(workbook_bytes, expression_tsv)
        if set(workbook_shape["samples"]) != set(metadata):
            raise ValueError("expression/GEO sample-title mismatch")

        # Outcome-blind fit and scoring happen before the response manifest is parsed.
        reference = V2.fit_reference(expression_tsv, reference_samples)
        scored = V2.score_matrix(expression_tsv, reference, reference_samples)

        manifest_path = tmp_path / "manifest.tsv"
        BASE.write_frozen_manifest(retained_records, manifest_path)
        manifest = BASE.MANIFEST.parse_manifest(manifest_path)

    joined = []
    for endpoint in manifest["included"]:
        sample_id = endpoint["sample_id"]
        if sample_id not in scored["samples"]:
            raise ValueError(f"included endpoint sample {sample_id} lacks a frozen v2 score")
        sample_score = scored["samples"][sample_id]
        joined.append(
            {
                "sample_id": sample_id,
                "patient_id": endpoint["patient_id"],
                "y": endpoint["y"],
                "endpoint": endpoint["endpoint"],
                "s_pd1_v2": sample_score["s_pd1_v2"],
                "route_burden_v2": sample_score["route_burden_v2"],
            }
        )

    labels = [item["y"] for item in joined]
    scores = [item["s_pd1_v2"] for item in joined]
    roc = BASE.auroc(labels, scores)
    ap = BASE.average_precision(labels, scores)
    roc_ci = BASE.stratified_auroc_bootstrap(labels, scores)
    prevalence = manifest["n_responder"] / manifest["n_included"]
    continuation = development_continue(labels, scores, roc, ap)

    expected_dedup = [
        item
        for item in later_exclusions
        if item["patient_id"] == "Pt27" and item["sample_id"] == "Pt27B"
    ]
    if len(expected_dedup) != 1 or "Pt27A" not in reference_samples:
        raise ValueError("frozen Pt27 first-biopsy rule was not preserved")
    if "Pt27B" in reference_samples:
        raise ValueError("Pt27B entered the frozen v2 development reference")

    nonpretreatment_exclusions = [
        item for item in manifest["excluded"] if item["reason"] == "nonpretreatment"
    ]
    if not any(item["sample_id"] == "Pt16" for item in nonpretreatment_exclusions):
        raise ValueError("expected on-treatment sample Pt16 was not excluded")
    if "Pt16" in reference_samples:
        raise ValueError("on-treatment Pt16 entered the v2 development reference")

    if manifest["n_included"] != 26 or manifest["n_responder"] != 14 or manifest["n_nonresponder"] != 12:
        raise ValueError("frozen primary endpoint membership drifted from the verified v1 audit")

    return {
        "status": "v2_development_continuation_screen",
        "cohort": "GSE78220",
        "locked_validation_cohort": "GSE91061_PRETREATMENT",
        "locked_validation_cohort_touched": False,
        "workbook": {
            "sha256": workbook_sha,
            "expected_sha256": BASE.EXPECTED_WORKBOOK_SHA256,
            "source_used": workbook_source,
            **workbook_shape,
        },
        "series_matrix": {
            "sha256": series_sha,
            "source_used": series_source,
            "sample_count": len(metadata),
        },
        "frozen_selection": {
            "rule": "earliest pretreatment biopsy ordinal per patient; selection ignores response",
            "reference_samples": reference_samples,
            "later_pretreatment_exclusions": later_exclusions,
            "nonpretreatment_exclusions": nonpretreatment_exclusions,
        },
        "feature": {
            "version": V2.FEATURE_VERSION,
            "direction": "higher_S_PD1_v2_predicts_CR_PR",
            "aggregation": "unweighted_mean_of_seven_signed_development_ECDF_spokes",
            "reference_fit_uses_outcomes": False,
            "reference": reference,
        },
        "endpoint": {
            "definition": "CR_or_PR_vs_PD",
            "n_included": manifest["n_included"],
            "n_responder": manifest["n_responder"],
            "n_nonresponder": manifest["n_nonresponder"],
            "excluded": manifest["excluded"],
        },
        "development_metrics": {
            "auroc": roc,
            "auroc_95_ci": roc_ci,
            "average_precision": ap,
            "responder_prevalence": prevalence,
        },
        "continuation_screen": continuation,
        "patients": joined,
        "decision": (
            "CONTINUE_TO_CALIBRATION_FREEZE_BEFORE_GSE91061"
            if continuation["passed"]
            else "RETIRE_V2_KEEP_GSE91061_LOCKED"
        ),
        "claim_boundary": (
            "This is a development-cohort continuation screen only. Passing it would only permit "
            "the next frozen development-only calibration/validation preparation step; it would not "
            "establish predictive validity, treatment selection, clinical efficacy, or cancer cure."
        ),
    }


def main():
    parser = argparse.ArgumentParser(description="Run the frozen GSE78220 melanoma v2 development screen.")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run_audit()
    text = json.dumps(result, indent=2, sort_keys=True)
    if args.output:
        args.output.write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
