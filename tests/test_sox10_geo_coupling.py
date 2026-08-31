import gzip
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from infra.ci.analyze_sox10_geo_coupling import (
    analyze_gse259388,
    analyze_gse259389,
    read_target_values,
)


GENES = {
    "BIRC3": "ENSG00000023445.17",
    "JUND": "ENSG00000130522.8",
    "JUN": "ENSG00000177606.7",
    "FOSL2": "ENSG00000075426.12",
}


def _write_sample(path, values):
    with gzip.open(path, "wt", encoding="utf-8") as f:
        f.write("gene_id\tgene_symbol\tnormalized_count\n")
        for symbol, ensembl in GENES.items():
            f.write(f"{ensembl}\t{symbol}\t{values[symbol]}\n")


def test_reads_symbols_or_versioned_ensembl_ids(tmp_path):
    path = tmp_path / "sample.txt.gz"
    _write_sample(path, {"BIRC3": 10, "JUND": 20, "JUN": 30, "FOSL2": 40})
    assert read_target_values(path) == {"BIRC3": 10, "JUND": 20, "JUN": 30, "FOSL2": 40}


def test_gse259388_matched_clone_ratios(tmp_path):
    base = {"BIRC3": 100, "JUND": 80, "JUN": 60, "FOSL2": 40}
    for clone in ("218", "421"):
        for treatment, scale in {
            "siCTRL": 1.0,
            "siTAZ1": 0.5,
            "siTAZ2": 0.6,
            "siYAP1": 0.9,
            "siYAP2": 0.8,
        }.items():
            for rep in (1, 2, 3):
                values = {gene: value * scale for gene, value in base.items()}
                _write_sample(tmp_path / f"{clone}_{treatment}_{rep}.txt.gz", values)

    result = analyze_gse259388(tmp_path)
    assert result["dataset"] == "GSE259388"
    assert result["status"] == "descriptive_only"
    assert result["contrasts"]["218"]["siTAZ1"]["BIRC3"]["ratio"] < 1
    assert result["contrasts"]["421"]["siTAZ2"]["JUND"]["ratio"] < 1


def test_gse259388_fails_when_target_gene_is_missing(tmp_path):
    path = tmp_path / "218_siCTRL_1.txt.gz"
    with gzip.open(path, "wt", encoding="utf-8") as f:
        f.write("gene\tvalue\nBIRC3\t10\nJUND\t20\nJUN\t30\n")
    with pytest.raises(AssertionError, match="missing target genes"):
        read_target_values(path)


def test_gse259389_wide_matrix_ratios(tmp_path):
    path = tmp_path / "GSE259389_allSamples.txt"
    columns = ["gene"]
    for clone in ("218", "421"):
        for treatment in ("DMSO", "OPN9643", "OPN9652"):
            for rep in (1, 2, 3):
                columns.append(f"{clone}_{treatment}_{rep}")

    with open(path, "w", encoding="utf-8") as f:
        f.write("\t".join(columns) + "\n")
        for symbol, base in {"BIRC3": 100, "JUND": 80, "JUN": 60, "FOSL2": 40}.items():
            row = [symbol]
            for clone in ("218", "421"):
                for treatment in ("DMSO", "OPN9643", "OPN9652"):
                    scale = {"DMSO": 1.0, "OPN9643": 0.7, "OPN9652": 0.5}[treatment]
                    row.extend([str(base * scale)] * 3)
            f.write("\t".join(row) + "\n")

    result = analyze_gse259389(path)
    assert result["dataset"] == "GSE259389"
    assert result["status"] == "descriptive_only"
    assert result["contrasts"]["218"]["OPN9652"]["BIRC3"]["ratio"] < 1
    assert result["contrasts"]["421"]["OPN9643"]["JUN"]["ratio"] < 1


def test_gse259389_fails_without_both_matched_clones(tmp_path):
    path = tmp_path / "matrix.txt"
    with open(path, "w", encoding="utf-8") as f:
        f.write("gene\t218_DMSO_1\t218_DMSO_2\t218_DMSO_3\t218_OPN9643_1\t218_OPN9643_2\t218_OPN9643_3\t218_OPN9652_1\t218_OPN9652_2\t218_OPN9652_3\n")
        for symbol in GENES:
            f.write(symbol + "\t" + "\t".join(["1"] * 9) + "\n")
    with pytest.raises(AssertionError, match="need >=3 421 DMSO replicates"):
        analyze_gse259389(path)
