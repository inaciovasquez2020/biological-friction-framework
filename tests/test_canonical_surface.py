from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_canonical_boundary_exists():
    for rel in ["README.md", "STATUS.md", "FREEZE.md", "CITATION.cff"]:
        assert (ROOT / rel).exists(), rel
