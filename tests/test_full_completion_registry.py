import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_full_completion_registry():
    reg = json.loads((ROOT / "docs/status/FULL_COMPLETION_REGISTRY.json").read_text())
    items = reg["items"]
    total = len(items)
    complete = sum(1 for x in items if x["status"] == "complete")
    percent = 100 * complete // total
    assert reg["scope"] == "repository-surface"
    assert reg["formula"] == "percent = 100 * complete / total"
    assert reg["expected_percent"] == percent

def test_full_completion_registry_witnesses():
    assert (ROOT / "README.md").exists()
    assert (ROOT / "STATUS.md").exists()
    assert (ROOT / "FREEZE.md").exists()
    assert (ROOT / "CITATION.cff").exists()
    assert (ROOT / "tests" / "test_canonical_surface.py").exists()
    assert (ROOT / "tests" / "test_scope_purity.py").exists()
    assert (ROOT / "tests" / "test_repo_scope_closure.py").exists()
    assert (ROOT / "archive" / "foreign-scope" / "fo4-manuscript" / "paper.tex").exists()
    assert (ROOT / "archive" / "foreign-scope" / "reintroduced" / "PSH_STATUS.md").exists()
