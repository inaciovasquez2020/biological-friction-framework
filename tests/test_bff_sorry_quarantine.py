from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

def test_bff_sorry_quarantine_verifier_passes():
    subprocess.run(
        [sys.executable, "scripts/verify_bff_sorry_quarantine.py"],
        cwd=ROOT,
        check=True,
    )

def test_bff_sorry_quarantine_boundary_tokens():
    text = (ROOT / "docs/status/BFF_SORRY_QUARANTINE_2026_05_02.md").read_text()
    assert "Registry ID: BFF-SQ-2026-05-02" in text
    assert "Removing or quarantining `sorry` tokens does not imply theorem-level closure." in text
    assert "no unconditional theorem-level closure claim is allowed" in text
    assert "theorem-level closure remains blocked" in text
