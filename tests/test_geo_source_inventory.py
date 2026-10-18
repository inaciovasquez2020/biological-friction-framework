import gzip
import importlib.util
import io
import tarfile
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "infra" / "ci" / "audit_geo_source_inventory.py"
SPEC = importlib.util.spec_from_file_location("geo_source_inventory", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_matrix_inventory_preserves_sample_ids_and_labels(tmp_path):
    matrix = tmp_path / "matrix.txt.gz"
    payload = (
        '!Sample_title\t"Responder_001"\t"Nonresponder_001"\n'
        '!Sample_geo_accession\t"GSM1"\t"GSM2"\n'
    ).encode()
    matrix.write_bytes(gzip.compress(payload))
    result = MODULE.matrix_inventory(matrix, 2)
    assert result["sample_count"] == 2
    assert result["gsm_accessions"] == ["GSM1", "GSM2"]
    assert result["title_label_counts"] == {"responder": 1, "nonresponder": 1}
    assert result["sample_count_matches_expected"] is True


def test_rcc_inventory_parses_xml_without_interpreting_assay_values():
    result = MODULE.rcc_inventory("sample.RCC", b"<Code_Summary><Header/><Code_Summary/></Code_Summary>")
    assert result["xml_parse"] == "PASS"
    assert result["xml_root"] == "Code_Summary"
    assert "tag_counts" in result


def test_rcc_inventory_extracts_documented_code_summary_counts():
    raw = (
        b"<Header>\nFileVersion,1.7\n</Header>\n"
        b"<Sample_Attributes>\nID,SampleA\n</Sample_Attributes>\n"
        b"<Code_Summary>\nCodeClass,Name,Accession,Count\n"
        b"Endogenous,WNT5A,NM_003392.5,123\n"
        b"Endogenous,RNF43,NM_017763.5,7\n</Code_Summary>\n"
    )
    result = MODULE.rcc_inventory("sample.RCC", raw)
    assert result["code_summary_parse"] == "PASS"
    assert result["code_summary_row_count"] == 2
    assert result["code_summary"] == [
        {"code_class": "Endogenous", "name": "WNT5A", "accession": "NM_003392.5", "count": 123},
        {"code_class": "Endogenous", "name": "RNF43", "accession": "NM_017763.5", "count": 7},
    ]


def test_rcc_inventory_rejects_noninteger_counts():
    raw = (
        b"<Code_Summary>\nCodeClass,Name,Accession,Count\n"
        b"Endogenous,WNT5A,NM_003392.5,not-a-count\n</Code_Summary>"
    )
    try:
        MODULE.rcc_inventory("sample.RCC", raw)
    except ValueError as exc:
        assert "invalid RCC Count" in str(exc)
    else:
        raise AssertionError("invalid RCC Count must fail closed")


def test_full_feature_classifier_detects_log2_sample_scale():
    import math
    raw = {f"GENE{i}": i + 10 for i in range(204)}
    processed = {gene: math.log2(count) - 0.0243935046 for gene, count in raw.items()}
    result = MODULE.classify_full_feature_scale(raw, processed)
    assert result["scale_class"] == "LOG2_RAW_COUNT_PLUS_OFFSET"
    assert result["matched_feature_count"] == 204
    assert result["log2_max_relative_residual"] < 1e-6


def test_full_feature_classifier_detects_linear_sample_scale():
    raw = {f"GENE{i}": i + 10 for i in range(204)}
    processed = {gene: count * 0.570987 for gene, count in raw.items()}
    result = MODULE.classify_full_feature_scale(raw, processed)
    assert result["scale_class"] == "LINEAR_SCALAR_MULTIPLE"
    assert result["matched_feature_count"] == 204
    assert result["linear_max_relative_residual"] < 1e-6


def test_scale_classifier_detects_linear_scalar_multiple():
    raw = {gene: index + 10 for index, gene in enumerate(MODULE.RECONCILIATION_GENES)}
    processed = {gene: count * 2.75 for gene, count in raw.items()}
    result = MODULE.classify_sample_scale(raw, processed)
    assert result["scale_class"] == "LINEAR_SCALAR_MULTIPLE"
    assert result["matched_gene_count"] == 19
    assert result["linear_max_abs_residual"] < 1e-5


def test_scale_classifier_detects_log2_values_with_offset():
    import math
    raw = {gene: index + 10 for index, gene in enumerate(MODULE.RECONCILIATION_GENES)}
    processed = {gene: math.log2(count) - 0.024 for gene, count in raw.items()}
    result = MODULE.classify_sample_scale(raw, processed)
    assert result["scale_class"] == "LOG2_RAW_COUNT_PLUS_OFFSET"
    assert result["log2_max_abs_residual"] < 1e-5


def test_scale_classifier_rejects_mixed_transform():
    import math
    raw = {gene: index + 10 for index, gene in enumerate(MODULE.RECONCILIATION_GENES)}
    processed = {gene: count * 2.75 for gene, count in raw.items()}
    processed[MODULE.RECONCILIATION_GENES[0]] = math.log2(raw[MODULE.RECONCILIATION_GENES[0]])
    result = MODULE.classify_sample_scale(raw, processed)
    assert result["scale_class"] == "UNRESOLVED_OR_MIXED_SCALE"


def test_audit_one_preserves_matrix_when_raw_archive_download_fails(tmp_path, monkeypatch):
    matrix = tmp_path / "GSE_TEST_series_matrix.txt.gz"
    matrix.write_bytes(gzip.compress(
        b'!Sample_title\t"Responder_001"\n!Sample_geo_accession\t"GSM1"\n'
    ))

    def fake_download(url, path):
        if url.endswith("matrix"):
            path.write_bytes(matrix.read_bytes())
            return {"url": url, "bytes": path.stat().st_size, "sha256": MODULE.sha256(path)}
        raise OSError("simulated raw archive network failure")

    monkeypatch.setattr(MODULE, "download", fake_download)
    result = MODULE.audit_one(
        "GSE_TEST",
        {"matrix": "https://example.test/matrix", "raw": "https://example.test/raw", "expected_samples": 1},
        tmp_path,
    )
    assert result["matrix"]["sample_count"] == 1
    assert result["status"] == "SOURCE_DOWNLOAD_OR_PARSE_BLOCKED"
    assert result["raw_archive_error"]["type"] == "OSError"
