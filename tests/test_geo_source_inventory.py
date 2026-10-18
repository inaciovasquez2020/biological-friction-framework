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
