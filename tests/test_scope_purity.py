from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = [
    ROOT / "README.md",
    ROOT / "STATUS.md",
    ROOT / "FREEZE.md",
    ROOT / "CITATION.cff",
]
FORBIDDEN = [
    "Cycle--Local Rigidity",
    "FO^4",
    "spectral gap",
    "Pi_loc",
    "Pi_sa",
    "pebble saturation",
]

def test_scope_purity():
    text = "\n".join(p.read_text() for p in SCAN if p.exists())
    for s in FORBIDDEN:
        assert s not in text
