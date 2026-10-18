import importlib.util
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "infra" / "ci" / "develop_melanoma_wnt_v1.py"
SPEC = importlib.util.spec_from_file_location("melanoma_wnt_v1", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_fixed_score_uses_only_frozen_panel_genes():
    expression = {gene: 10.0 for gene in MODULE.RESISTANCE_GENES}
    expression["RNF43"] = 2.0
    expression["UNRELATED_GENE"] = 1e12
    score, receipt = MODULE.fixed_wnt_score(expression)
    assert score > 0
    assert receipt["direction"] == "higher score predicts nonresponse"
    assert "UNRELATED_GENE" not in receipt["resistance_genes_present"]


def test_fixed_score_fails_closed_when_panel_coverage_missing():
    try:
        MODULE.fixed_wnt_score({"RNF43": 1.0, "WNT2B": 1.0})
    except ValueError as exc:
        assert "panel coverage inadequate" in str(exc)
    else:
        raise AssertionError("insufficient panel coverage must fail closed")


def test_auc_ties_are_averaged():
    assert MODULE.auc([0, 1, 0, 1], [1.0, 1.0, 0.0, 0.0]) == 0.5


def test_series_matrix_parser_and_response_labels():
    raw = b'''!Sample_title\t"Responder_001"\t"Nonresponder_001"
!series_matrix_table_begin
ID_REF\t"GSM1"\t"GSM2"
"WNT2B"\t10\t2
"RNF43"\t3\t9
"WNT5A"\t8\t1
"FZD4"\t7\t2
"LRP6"\t6\t3
"DKK2"\t5\t2
!series_matrix_table_end
'''
    rows, metadata = MODULE.parse_series_matrix(raw)
    assert [row["y"] for row in rows] == [1, 0]
    assert metadata["sample_count"] == 2
    assert rows[0]["expression"]["WNT2B"] == 10.0
