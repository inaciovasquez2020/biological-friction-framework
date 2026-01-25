import json, hashlib, os, sys
import numpy as np

def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

if len(sys.argv) != 2:
    print("Usage: check_spectral_gap.py <certificate.json>")
    sys.exit(1)

cert_path = sys.argv[1]
base, _ = os.path.splitext(cert_path)
sha_path = base + ".sha256"

# Hash-lock (if .sha256 exists, enforce)
if os.path.exists(sha_path):
    expected = open(sha_path, "r", encoding="utf-8").read().strip().split()[0]
    got = sha256_file(cert_path)
    if got != expected:
        print("FAIL sha256 mismatch:", got, "!=", expected)
        sys.exit(1)

with open(cert_path, "r", encoding="utf-8") as f:
    data = json.load(f)

A = np.array([[float(x) for x in row] for row in data["operator"]["A"]], dtype=float)
Pi = np.array(data["projector"]["Pi"], dtype=float)
I = np.eye(A.shape[0])

B = (I - Pi) @ A @ (I - Pi)

mask = np.diag(I - Pi) > 0.5
B_perp = B[np.ix_(mask, mask)]

eigvals = np.linalg.eigvals(B_perp)
gamma = float(data["claim"]["gamma"])
lam_min = float(min(eigvals.real))

if lam_min + 1e-9 >= gamma:
    print("PASS spectral gap on V⊥:", lam_min)
    sys.exit(0)
else:
    print("FAIL spectral gap on V⊥:", lam_min)
    sys.exit(1)
REGISTRY_PATH = "verification/schema/cert_registry.json"

with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
    registry = json.load(f)

cid = data.get("id")
if cid not in registry["certificates"]:
    print("FAIL certificate not registered:", cid)
    sys.exit(1)
