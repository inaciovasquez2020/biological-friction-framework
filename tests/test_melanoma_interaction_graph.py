from copy import deepcopy
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from infra.ci.verify_melanoma_interaction_graph import load_certificate, verify_graph


EXPECTED_UNRESOLVED = [
    "apoe_dissemination_release",
    "ferroptosis_handoff_gap",
    "polk_stress_tolerance",
]


def test_conditional_interaction_graph_passes():
    result = verify_graph(load_certificate())
    assert result["valid"] is True
    assert result["claim"] == "conditional"
    assert result["reachable_malignant"] == EXPECTED_UNRESOLVED


def test_closed_claim_rejected_while_malignant_states_are_reachable():
    cert = deepcopy(load_certificate())
    cert["claim"] = "closed"
    cert["declared_unresolved"] = []

    with pytest.raises(AssertionError, match="closed claim invalid"):
        verify_graph(cert)


def test_conditional_claim_must_declare_all_reachable_escape_states():
    cert = deepcopy(load_certificate())
    cert["declared_unresolved"] = []

    with pytest.raises(AssertionError, match="declare exactly all reachable malignant states"):
        verify_graph(cert)


def test_apoe_reduction_probe_exposes_signed_tradeoff():
    cert = deepcopy(load_certificate())
    cert["active_controls"].remove("PROBE_APOE_REDUCTION")
    cert["declared_unresolved"] = [
        "apoe_ferroptosis_resistance",
        "apoe_immune_escape",
        "ferroptosis_handoff_gap",
        "polk_stress_tolerance",
    ]

    result = verify_graph(cert)
    assert "apoe_dissemination_release" not in result["reachable_malignant"]
    assert "apoe_ferroptosis_resistance" in result["reachable_malignant"]
    assert "apoe_immune_escape" in result["reachable_malignant"]


def test_ferroptosis_endpoint_control_does_not_close_handoff_gap():
    result = verify_graph(load_certificate())
    assert "ln_fsp1_escape" not in result["reachable_malignant"]
    assert "hemato_gpx4_escape" not in result["reachable_malignant"]
    assert "ferroptosis_handoff_gap" in result["reachable_malignant"]


def test_kdm5b_control_blocks_persister_and_reseed_states():
    result = verify_graph(load_certificate())
    assert "kdm5b_persister_reservoir" not in result["reachable_malignant"]
    assert "kdm5b_reseed" not in result["reachable_malignant"]

    cert = deepcopy(load_certificate())
    cert["active_controls"].remove("C_KDM5B_RESEED")
    cert["declared_unresolved"] = EXPECTED_UNRESOLVED + [
        "kdm5b_persister_reservoir",
        "kdm5b_reseed",
    ]

    result = verify_graph(cert)
    assert "kdm5b_persister_reservoir" in result["reachable_malignant"]
    assert "kdm5b_reseed" in result["reachable_malignant"]
