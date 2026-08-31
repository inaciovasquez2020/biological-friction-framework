from copy import deepcopy
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from infra.ci.verify_melanoma_interaction_graph import load_certificate, verify_graph


MRD_GAPS = [
    "pigmented_redistribution_gap",
    "smc_redistribution_gap",
    "sox10_dual_vulnerability_gap",
]

CROSS_STATE_GAPS = [
    "adenosine_ligand_sink_gap",
    "cse_state_mapping_gap",
    "eif4a_cross_state_gap",
]

COUPLED_ROUTE_GAPS = [
    "rac1_fak_mapk_generality_gap",
]

EXPECTED_UNRESOLVED = sorted(
    [
        "apoe_dissemination_release",
        "fancd2_mapki_in_vivo_gap",
        "ferroptosis_handoff_gap",
        "polk_stress_tolerance",
        *MRD_GAPS,
        *CROSS_STATE_GAPS,
        *COUPLED_ROUTE_GAPS,
    ]
)


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
    cert["declared_unresolved"] = sorted(
        [
            "apoe_ferroptosis_resistance",
            "apoe_immune_escape",
            "fancd2_mapki_in_vivo_gap",
            "ferroptosis_handoff_gap",
            "polk_stress_tolerance",
            *MRD_GAPS,
            *CROSS_STATE_GAPS,
            *COUPLED_ROUTE_GAPS,
        ]
    )

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
    cert["declared_unresolved"] = sorted(
        EXPECTED_UNRESOLVED
        + ["kdm5b_persister_reservoir", "kdm5b_reseed"]
    )

    result = verify_graph(cert)
    assert "kdm5b_persister_reservoir" in result["reachable_malignant"]
    assert "kdm5b_reseed" in result["reachable_malignant"]


def test_sox10_control_blocks_state_but_not_redundancy_gap():
    result = verify_graph(load_certificate())
    assert "sox10_low_mrd" not in result["reachable_malignant"]
    assert "sox10_dual_vulnerability_gap" in result["reachable_malignant"]

    cert = deepcopy(load_certificate())
    cert["active_controls"].remove("C_SOX10_LOW")
    cert["declared_unresolved"] = sorted(EXPECTED_UNRESOLVED + ["sox10_low_mrd"])
    result = verify_graph(cert)
    assert "sox10_low_mrd" in result["reachable_malignant"]


def test_smc_control_blocks_state_but_not_redistribution_gap():
    result = verify_graph(load_certificate())
    assert "smc_cd36_persister" not in result["reachable_malignant"]
    assert "smc_redistribution_gap" in result["reachable_malignant"]

    cert = deepcopy(load_certificate())
    cert["active_controls"].remove("C_SMC_METABOLIC")
    cert["declared_unresolved"] = sorted(EXPECTED_UNRESOLVED + ["smc_cd36_persister"])
    result = verify_graph(cert)
    assert "smc_cd36_persister" in result["reachable_malignant"]
    assert "pigmented_mitf_persister" not in result["reachable_malignant"]
    assert "ncsc_nongenetic_escape" not in result["reachable_malignant"]
    assert "sox10_low_mrd" not in result["reachable_malignant"]


def test_smc_natural_trajectory_is_exposed_when_destination_control_is_removed():
    cert = deepcopy(load_certificate())
    cert["active_controls"].remove("C_SMC_METABOLIC")
    cert["active_controls"].remove("C_PIGMENTED")
    cert["declared_unresolved"] = sorted(
        EXPECTED_UNRESOLVED + ["smc_cd36_persister", "pigmented_mitf_persister"]
    )
    result = verify_graph(cert)
    assert "smc_cd36_persister" in result["reachable_malignant"]
    assert "pigmented_mitf_persister" in result["reachable_malignant"]


def test_pigmented_control_blocks_state_but_not_redistribution_gap():
    result = verify_graph(load_certificate())
    assert "pigmented_mitf_persister" not in result["reachable_malignant"]
    assert "pigmented_redistribution_gap" in result["reachable_malignant"]

    cert = deepcopy(load_certificate())
    cert["active_controls"].remove("C_PIGMENTED")
    cert["declared_unresolved"] = sorted(EXPECTED_UNRESOLVED + ["pigmented_mitf_persister"])
    result = verify_graph(cert)
    assert "pigmented_mitf_persister" in result["reachable_malignant"]


def test_adenosine_control_blocks_escape_but_not_melanoma_ligand_sink_gap():
    result = verify_graph(load_certificate())
    assert "adenosine_immune_escape" not in result["reachable_malignant"]
    assert "adenosine_ligand_sink_gap" in result["reachable_malignant"]

    cert = deepcopy(load_certificate())
    cert["active_controls"].remove("C_ADENOSINE_LIGAND")
    cert["declared_unresolved"] = sorted(EXPECTED_UNRESOLVED + ["adenosine_immune_escape"])
    result = verify_graph(cert)
    assert "adenosine_immune_escape" in result["reachable_malignant"]


def test_cse_control_blocks_persister_but_not_state_mapping_gap():
    result = verify_graph(load_certificate())
    assert "cse_persister_survival" not in result["reachable_malignant"]
    assert "cse_state_mapping_gap" in result["reachable_malignant"]

    cert = deepcopy(load_certificate())
    cert["active_controls"].remove("C_CSE_REDOX")
    cert["declared_unresolved"] = sorted(EXPECTED_UNRESOLVED + ["cse_persister_survival"])
    result = verify_graph(cert)
    assert "cse_persister_survival" in result["reachable_malignant"]


def test_translation_control_blocks_survival_and_mutability_but_not_cross_state_gap():
    result = verify_graph(load_certificate())
    assert "eif4a_persister_survival" not in result["reachable_malignant"]
    assert "eif4a_adaptive_mutability" not in result["reachable_malignant"]
    assert "eif4a_cross_state_gap" in result["reachable_malignant"]

    cert = deepcopy(load_certificate())
    cert["active_controls"].remove("C_TRANSLATION_PERSIST")
    cert["declared_unresolved"] = sorted(
        EXPECTED_UNRESOLVED
        + ["eif4a_persister_survival", "eif4a_adaptive_mutability"]
    )
    result = verify_graph(cert)
    assert "eif4a_persister_survival" in result["reachable_malignant"]
    assert "eif4a_adaptive_mutability" in result["reachable_malignant"]


def test_rac1_composite_control_blocks_observed_route_but_not_generality_gap():
    result = verify_graph(load_certificate())
    assert "rac1_coupled_observed" not in result["reachable_malignant"]
    assert "rac1_fak_mapk_generality_gap" in result["reachable_malignant"]

    cert = deepcopy(load_certificate())
    cert["active_controls"].remove("C_RAC1_FAK_MAPK_OBSERVED")
    cert["declared_unresolved"] = sorted(EXPECTED_UNRESOLVED + ["rac1_coupled_observed"])
    result = verify_graph(cert)
    assert "rac1_coupled_observed" in result["reachable_malignant"]
    assert "rac1_fak_mapk_generality_gap" in result["reachable_malignant"]


def test_fancd2_control_blocks_direct_state_but_not_in_vivo_gap():
    result = verify_graph(load_certificate())
    assert "fancd2_replication_stress_tolerance" not in result["reachable_malignant"]
    assert "fancd2_mapki_in_vivo_gap" in result["reachable_malignant"]

    cert = deepcopy(load_certificate())
    cert["active_controls"].remove("C_FANCD2_REPLICATION_STRESS")
    cert["declared_unresolved"] = sorted(
        EXPECTED_UNRESOLVED + ["fancd2_replication_stress_tolerance"]
    )
    result = verify_graph(cert)
    assert "fancd2_replication_stress_tolerance" in result["reachable_malignant"]
    assert "fancd2_mapki_in_vivo_gap" in result["reachable_malignant"]
