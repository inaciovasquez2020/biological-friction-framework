import importlib.util
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "infra" / "ci" / "preflight_mel_dfci_v2_cohort.py"
SPEC = importlib.util.spec_from_file_location("mel_dfci_preflight", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)
classify_response = MODULE.classify_response


def test_complete_response_is_responder():
    assert classify_response("Complete Response") == "RESPONDER_CR_PR"


def test_partial_response_is_responder():
    assert classify_response("Partial Response") == "RESPONDER_CR_PR"


def test_pd_is_nonresponder():
    assert classify_response("Progressive Disease") == "NONRESPONDER_PD"


def test_stable_and_mixed_are_excluded():
    assert classify_response("Stable Disease") == "EXCLUDED_NONMATCHING_OR_UNKNOWN"
    assert classify_response("Mixed Response") == "EXCLUDED_NONMATCHING_OR_UNKNOWN"


def test_common_abbreviations_are_supported():
    assert classify_response("CR") == "RESPONDER_CR_PR"
    assert classify_response("PR") == "RESPONDER_CR_PR"
    assert classify_response("PD") == "NONRESPONDER_PD"
