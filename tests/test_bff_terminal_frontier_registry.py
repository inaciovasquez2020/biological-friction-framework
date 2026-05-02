from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

def test_bff_terminal_frontier_registry_verifier_passes():
    subprocess.run(
        [sys.executable, "scripts/verify_bff_terminal_frontier_registry.py"],
        cwd=ROOT,
        check=True,
    )

def test_bff_terminal_frontier_registry_boundary_tokens():
    text = (ROOT / "docs/status/BFF_TERMINAL_FRONTIER_REGISTRY_2026_05_02.md").read_text()
    assert "Status: Conditional Framework / Repository-Surface Closed" in text
    assert "No theorem-level closure is asserted." in text
    assert "No universal biological law is asserted." in text
    assert "repository-surface closed; theorem-level claims conditional" in text
