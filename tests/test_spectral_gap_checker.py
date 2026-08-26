import hashlib
import json
import math
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "urf-core" / "verification" / "checkers" / "check_spectral_gap.py"


def base_certificate():
    return {
        "id": "URF-SG-0001",
        "operator": {
            "A": [
                [0.0, 0.0, 0.0],
                [0.0, 1.0, 0.0],
                [0.0, 0.0, 2.0],
            ]
        },
        "projector": {
            "Pi": [
                [1.0, 0.0, 0.0],
                [0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0],
            ]
        },
        "claim": {"gamma": 0.5},
    }


def run_certificate(tmp_path, data, *, write_hash=True):
    cert_path = tmp_path / "URF-SG-0001.json"
    cert_path.write_text(json.dumps(data), encoding="utf-8")

    if write_hash:
        digest = hashlib.sha256(cert_path.read_bytes()).hexdigest()
        cert_path.with_suffix(".sha256").write_text(
            f"{digest}  verification/certs/URF-SG-0001.json\n",
            encoding="utf-8",
        )

    return subprocess.run(
        [sys.executable, str(CHECKER), str(cert_path)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def test_valid_certificate_passes(tmp_path):
    result = run_certificate(tmp_path, base_certificate())
    assert result.returncode == 0, result.stdout + result.stderr
    assert "PASS spectral gap on V⊥" in result.stdout


def test_rotated_projector_uses_basis_independent_vperp(tmp_path):
    # V = span((1,1,1)/sqrt(3)).  The old diagonal-mask implementation selected
    # all three coordinate axes and incorrectly retained a zero eigenvalue.
    one_third = 1.0 / 3.0
    pi = [[one_third for _ in range(3)] for _ in range(3)]
    A = [
        [2.0 / 3.0, -one_third, -one_third],
        [-one_third, 2.0 / 3.0, -one_third],
        [-one_third, -one_third, 2.0 / 3.0],
    ]
    data = base_certificate()
    data["operator"]["A"] = A
    data["projector"]["Pi"] = pi
    data["claim"]["gamma"] = 0.9

    result = run_certificate(tmp_path, data)
    assert result.returncode == 0, result.stdout + result.stderr


def test_registry_validation_is_reachable(tmp_path):
    data = base_certificate()
    data["id"] = "UNREGISTERED"
    result = run_certificate(tmp_path, data)
    assert result.returncode != 0
    assert "certificate not registered" in result.stdout


def test_missing_hash_lock_is_rejected(tmp_path):
    result = run_certificate(tmp_path, base_certificate(), write_hash=False)
    assert result.returncode != 0
    assert "sha256 lock missing" in result.stdout


def test_nonfinite_input_is_rejected(tmp_path):
    data = base_certificate()
    data["operator"]["A"][1][1] = math.inf
    result = run_certificate(tmp_path, data)
    assert result.returncode != 0
    assert "A contains NaN or Inf" in result.stdout


def test_nonsymmetric_operator_is_rejected(tmp_path):
    data = base_certificate()
    data["operator"]["A"][1][2] = 0.25
    result = run_certificate(tmp_path, data)
    assert result.returncode != 0
    assert "A is not symmetric/self-adjoint" in result.stdout


def test_nonprojector_pi_is_rejected(tmp_path):
    data = base_certificate()
    data["projector"]["Pi"][0][0] = 0.5
    result = run_certificate(tmp_path, data)
    assert result.returncode != 0
    assert "Pi is not idempotent" in result.stdout


def test_projector_must_select_zero_modes(tmp_path):
    data = base_certificate()
    data["projector"]["Pi"] = [
        [0.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0],
    ]
    result = run_certificate(tmp_path, data)
    assert result.returncode != 0
    assert "Pi does not project into ker(A)" in result.stdout
