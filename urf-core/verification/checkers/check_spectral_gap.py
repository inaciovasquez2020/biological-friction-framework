import json
import numpy as np
import sys

if len(sys.argv) != 2:
    print("Usage: check_spectral_gap.py <certificate.json>")
    sys.exit(1)

with open(sys.argv[1]) as f:
    data = json.load(f)

A = np.array([[float(x) for x in row] for row in data["operator"]["A"]])
Pi = np.array(data["projector"]["Pi"], dtype=float)
I = np.eye(A.shape[0])

# Compressed operator
B = (I - Pi) @ A @ (I - Pi)

# Extract V^⊥ by selecting rows/cols where diagonal of (I-Pi) is 1
mask = np.diag(I - Pi) > 0.5
B_perp = B[np.ix_(mask, mask)]

eigvals = np.linalg.eigvals(B_perp)
gamma = float(data["claim"]["gamma"])
lam_min = min(eigvals.real)

if lam_min + 1e-9 >= gamma:
    print("PASS spectral gap on V⊥:", lam_min)
    sys.exit(0)
else:
    print("FAIL spectral gap on V⊥:", lam_min)
    sys.exit(1)

