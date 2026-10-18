import pandas as pd
import pytest

from infra.ci.audit_melanoma_wnt_inputs import (
    REFERENCE_GENE,
    RESISTANCE_GENES,
    calculate_frozen_score,
    reconcile_ids,
)


def expression_fixture():
    genes = list(RESISTANCE_GENES) + [REFERENCE_GENE]
    return pd.DataFrame({
        "Gene": genes,
        "S001": [10.0] * len(RESISTANCE_GENES) + [2.0],
        "S002": [8.0] * len(RESISTANCE_GENES) + [1.0],
    })


def test_score_requires_scale_and_mapping_gates():
    frame = expression_fixture()
    with pytest.raises(ValueError, match="scale"):
        calculate_frozen_score(frame, scale_verified=False, sample_mapping_verified=True)
    with pytest.raises(ValueError, match="sample IDs"):
        calculate_frozen_score(frame, scale_verified=True, sample_mapping_verified=False)


def test_score_uses_frozen_formula_without_silent_gene_drop():
    result = calculate_frozen_score(
        expression_fixture(), scale_verified=True, sample_mapping_verified=True
    )
    assert result["S001"] == pytest.approx(8.0)
    assert result["S002"] == pytest.approx(7.0)


def test_missing_gene_fails_closed():
    frame = expression_fixture().iloc[:-2].copy()
    with pytest.raises(ValueError, match="required genes missing"):
        calculate_frozen_score(frame, scale_verified=True, sample_mapping_verified=True)


def test_log1p_rejects_negative_values():
    frame = expression_fixture()
    frame.loc[0, "S001"] = -0.1
    with pytest.raises(ValueError, match="negative"):
        calculate_frozen_score(
            frame, scale_verified=True, sample_mapping_verified=True, transform="log1p"
        )


def test_different_ids_do_not_establish_independence_without_crosswalk():
    result = reconcile_ids(
        ["R001", "R002"], ["H098", "H100"], identity_crosswalk_verified=False
    )
    assert result["status"] == "unresolved_identifier_crosswalk"
    assert result["independence_established"] is False


def test_verified_shared_ids_detect_overlap():
    result = reconcile_ids(
        ["P01", "P02"], ["P02", "P03"], identity_crosswalk_verified=True
    )
    assert result["overlap_ids"] == ["P02"]
    assert result["status"] == "overlap_detected"
    assert result["independence_established"] is False
