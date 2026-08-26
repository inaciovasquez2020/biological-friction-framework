import json
import hashlib
import sys
from pathlib import Path

import numpy as np

ATOL = 1e-9
EXPECTED_CHECKER = "verification/checkers/check_spectral_gap.py"


def fail(*parts) -> None:
    print("FAIL", *parts)
    sys.exit(1)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


if len(sys.argv) != 2:
    print("Usage: check_spectral_gap.py <certificate.json>")
    sys.exit(1)

cert_path = Path(sys.argv[1]).resolve()
sha_path = cert_path.with_suffix(".sha256")

# A registered hard-gate certificate must be hash locked.
if not sha_path.exists():
    fail("sha256 lock missing:", sha_path)

try:
    expected = sha_path.read_text(encoding="utf-8").strip().split()[0]
except (OSError, IndexError):
    fail("invalid sha256 lock:", sha_path)

got = sha256_file(cert_path)
if got != expected:
    fail("sha256 mismatch:", got, "!=", expected)

try:
    with cert_path.open("r", encoding="utf-8") as f:
        data = json.load(f)
except (OSError, json.JSONDecodeError) as exc:
    fail("invalid certificate JSON:", exc)

# Resolve the registry relative to this checker, not the caller's cwd.
registry_path = Path(__file__).resolve().parents[1] / "schema" / "cert_registry.json"
try:
    with registry_path.open("r", encoding="utf-8") as f:
        registry = json.load(f)
except (OSError, json.JSONDecodeError) as exc:
    fail("invalid certificate registry:", exc)

cid = data.get("id")
entry = registry.get("certificates", {}).get(cid)
if entry is None:
    fail("certificate not registered:", cid)

if entry.get("checker") != EXPECTED_CHECKER:
    fail("certificate registered to a different checker:", entry.get("checker"))

try:
    A = np.array(
        [[float(x) for x in row] for row in data["operator"]["A"]],
        dtype=float,
    )
    Pi = np.array(data["projector"]["Pi"], dtype=float)
    gamma = float(data["claim"]["gamma"])
except (KeyError, TypeError, ValueError) as exc:
    fail("invalid certificate fields:", exc)

# Matrix-domain and numeric sanity checks.
if A.ndim != 2 or A.shape[0] != A.shape[1] or A.shape[0] == 0:
    fail("A must be a non-empty square matrix:", A.shape)

if Pi.ndim != 2 or Pi.shape[0] != Pi.shape[1]:
    fail("Pi must be square:", Pi.shape)

if Pi.shape != A.shape:
    fail("A/Pi shape mismatch:", A.shape, Pi.shape)

if not np.all(np.isfinite(A)):
    fail("A contains NaN or Inf")

if not np.all(np.isfinite(Pi)):
    fail("Pi contains NaN or Inf")

if not np.isfinite(gamma):
    fail("gamma is NaN or Inf")

if gamma <= 0.0:
    fail("gamma must be positive:", gamma)

# The spectral-gap claim uses an ordered real spectrum, so A must be
# self-adjoint and Pi must be an orthogonal projector onto zero modes.
if not np.allclose(A.T, A, rtol=0.0, atol=ATOL):
    fail("A is not symmetric/self-adjoint")

if not np.allclose(Pi.T, Pi, rtol=0.0, atol=ATOL):
    fail("Pi is not symmetric")

if not np.allclose(Pi @ Pi, Pi, rtol=0.0, atol=ATOL):
    fail("Pi is not idempotent")

if not np.allclose(A @ Pi, np.zeros_like(A), rtol=0.0, atol=ATOL):
    fail("Pi does not project into ker(A)")

# Build an orthonormal basis for V-perp = range(I - Pi). This is basis
# independent; selecting coordinate axes from diag(I - Pi) is not.
I = np.eye(A.shape[0])
perp = I - Pi

evals_perp, evecs_perp = np.linalg.eigh(perp)
Q = evecs_perp[:, evals_perp > 0.5]

if Q.shape[1] == 0:
    fail("Vperp is zero-dimensional")

# Since A is self-adjoint and Pi projects into ker(A), this compression is the
# actual restriction of A to V-perp. eigvalsh preserves the real ordering.
B_perp = Q.T @ A @ Q
eigvals = np.linalg.eigvalsh(B_perp)
lam_min = float(eigvals[0])

if not np.isfinite(lam_min):
    fail("computed minimum eigenvalue is NaN or Inf")

if lam_min + ATOL >= gamma:
    print("PASS spectral gap on V⊥:", lam_min)
    sys.exit(0)

fail("spectral gap on V⊥:", lam_min, "<", gamma)
