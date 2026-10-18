import importlib.util
import csv
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "infra" / "ci" / "audit_itm_pc4_route_overlap.py"
SPEC = importlib.util.spec_from_file_location("itm_pc4_audit", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


def write_csv(path, header, rows):
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(header)
        writer.writerows(rows)


def fixture_inputs(tmp_path):
    matrix = tmp_path / "matrix.csv"
    signature = tmp_path / "signature.csv"
    manifest = tmp_path / "manifest.csv"
    genes = ["KDM5B", "CD36", "MITF", "MTHFD2", "NGFR", "NT5E", "SOX10", "PMEL"]
    write_csv(matrix, ["gene", "AOI_1", "AOI_2"], [[gene, 1, 2] for gene in genes])
    write_csv(
        signature,
        ["gene_symbol", "pc4_direction"],
        [["MITF", "positive"], ["SOX10", "negative"], ["KDM5B", "negative"], ["PMEL", "positive"]],
    )
    write_csv(manifest, ["sample_id", "patient_id"], [["AOI_1", "P1"], ["AOI_2", "P1"]])
    return matrix, signature, manifest


def test_overlap_audit_is_descriptive_and_does_not_score(tmp_path):
    matrix, signature, manifest = fixture_inputs(tmp_path)
    result = MODULE.audit(
        matrix, signature, manifest, expected_positive_genes=2, expected_negative_genes=2
    )
    assert result["cohort_accounting"]["matrix_sample_columns"] == 2
    assert result["cohort_accounting"]["unique_patients_in_manifest"] == 1
    assert result["cohort_accounting"]["patients_with_multiple_aois"] == {"P1": 2}
    assert result["frozen_route_overlap"]["exact_route_pc4_overlap"] == [
        "KDM5B", "MITF", "SOX10"
    ]
    assert result["frozen_route_overlap"]["direction_consistent_overlap"] == ["MITF", "SOX10"]
    assert result["frozen_route_overlap"]["direction_conflict_overlap"] == ["KDM5B"]
    assert result["decision"]["frozen_v2_scoring_performed"] is False
    assert result["decision"]["survival_analysis_performed"] is False


def test_matrix_manifest_sample_mismatch_is_reported(tmp_path):
    matrix, signature, manifest = fixture_inputs(tmp_path)
    write_csv(manifest, ["sample_id", "patient_id"], [["AOI_1", "P1"], ["OTHER", "P2"]])
    result = MODULE.audit(
        matrix, signature, manifest, expected_positive_genes=2, expected_negative_genes=2
    )
    assert result["decision"]["input_identity_gate_pass"] is False
    assert result["cohort_accounting"]["matrix_samples_missing_manifest"] == ["AOI_2"]
    assert result["cohort_accounting"]["manifest_samples_missing_matrix"] == ["OTHER"]
    assert result["decision"]["ready_for_signature_overlap_interpretation"] is False


def test_duplicate_signature_gene_is_rejected(tmp_path):
    matrix, signature, manifest = fixture_inputs(tmp_path)
    write_csv(
        signature,
        ["gene_symbol", "pc4_direction"],
        [["MITF", "positive"], ["MITF", "negative"]],
    )
    try:
        MODULE.audit(matrix, signature, manifest)
    except ValueError as exc:
        assert "duplicate signature gene" in str(exc)
    else:
        raise AssertionError("duplicate signature gene was accepted")


def test_nonfinite_expression_values_are_not_read_or_required(tmp_path):
    matrix, signature, manifest = fixture_inputs(tmp_path)
    write_csv(
        matrix,
        ["gene", "AOI_1", "AOI_2"],
        [["MITF", "not_downloaded", ""], ["SOX10", "NA", "NA"]],
    )
    result = MODULE.audit(
        matrix, signature, manifest, expected_positive_genes=2, expected_negative_genes=2
    )
    assert result["decision"]["input_identity_gate_pass"] is True
    assert result["decision"]["frozen_v2_scoring_performed"] is False



def test_treatment_context_is_inventoried_without_modeling_or_imputation(tmp_path):
    matrix, signature, manifest = fixture_inputs(tmp_path)
    write_csv(
        manifest,
        [
            "sample_id", "patient_id", "treatment_class", "exposure_status",
            "biopsy_timing", "response_endpoint", "response_status",
        ],
        [
            ["AOI_1", "P1", "anti-PD-1", "previously treated", "post-treatment", "RECIST", "PD"],
            ["AOI_2", "P1", "anti-PD-1", "unknown", "unknown", "RECIST", ""],
        ],
    )
    result = MODULE.audit(
        matrix, signature, manifest, expected_positive_genes=2, expected_negative_genes=2
    )
    context = result["treatment_context_inventory"]
    assert context["all_context_columns_present"] is True
    assert context["field_summary"]["treatment_class"]["categories"] == {"anti-PD-1": 2}
    assert context["field_summary"]["exposure_status"]["reported_rows"] == 1
    assert context["field_summary"]["biopsy_timing"]["unresolved_rows"] == 1
    assert result["decision"]["treatment_response_analysis_performed"] is False
    assert result["decision"]["treatment_interaction_test_performed"] is False


def test_treatment_context_absence_is_reported_not_inferred(tmp_path):
    matrix, signature, manifest = fixture_inputs(tmp_path)
    result = MODULE.audit(
        matrix, signature, manifest, expected_positive_genes=2, expected_negative_genes=2
    )
    context = result["treatment_context_inventory"]
    assert context["all_context_columns_present"] is False
    assert context["field_summary"]["treatment_class"]["column_present"] is False
    assert result["decision"]["treatment_context_columns_complete"] is False



def test_published_source_ici_alias_is_counted_without_relabeling_it():
    context = MODULE.summarize_treatment_context(
        [
            {"ICI": "0"},
            {"ICI": "1"},
            {"ICI": ""},
        ]
    )
    assert context["field_summary"]["exposure_status"]["source_column"] == "ICI"
    assert context["field_summary"]["exposure_status"]["categories"] == {"0": 1, "1": 1}
    assert context["field_summary"]["exposure_status"]["unresolved_rows"] == 1
    assert context["field_summary"]["treatment_class"]["column_present"] is False
    assert context["analysis_performed"] is False
