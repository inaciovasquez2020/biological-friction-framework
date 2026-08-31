from copy import deepcopy
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from infra.ci.verify_melanoma_interaction_graph import load_certificate, verify_graph


def test_conditional_interaction_graph_passes():
    result = verify_graph(load_certificate())
    assert result["valid"] is True
    assert result["claim"] == "conditional"
    assert result["reachable_malignant"] == ["polk_stress_tolerance"]


def test_closed_claim_rejected_while_polk_is_reachable():
    cert = deepcopy(load_certificate())
    cert["claim"] = "closed"
    cert["declared_unresolved"] = []

    with pytest.raises(AssertionError, match="closed claim invalid"):
        verify_graph(cert)


def test_conditional_claim_must_declare_reachable_escape():
    cert = deepcopy(load_certificate())
    cert["declared_unresolved"] = []

    with pytest.raises(AssertionError, match="declare exactly all reachable malignant states"):
        verify_graph(cert)
