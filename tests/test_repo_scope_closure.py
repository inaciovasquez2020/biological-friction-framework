from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FORBIDDEN_PATHS = [
    ROOT / "docs" / "PSH_STATUS.md",
    ROOT / "lean",
    ROOT / "toolkit" / "oblivion" / "scripts" / "cyclone_cfi_test.py",
    ROOT / "biological-friction-framework" / "paper.fdb_latexmk",
    ROOT / "biological-friction-framework" / "paper.fls",
]

def test_forbidden_paths_absent_from_live_scope():
    for p in FORBIDDEN_PATHS:
        assert not p.exists(), str(p)
