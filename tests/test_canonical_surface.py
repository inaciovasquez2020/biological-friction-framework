from pathlib import Path

def test_canonical_files_exist():
    for f in ["README.md", "STATUS.md", "FREEZE.md", "CITATION.cff"]:
        assert Path(f).exists(), f

def test_readme_mentions_boundary():
    txt = Path("README.md").read_text()
    assert "Canonical Boundary" in txt
    assert "STATUS.md" in txt
    assert "FREEZE.md" in txt

def test_status_scope():
    txt = Path("STATUS.md").read_text()
    assert "Biological Friction Framework" in txt
    assert "main is canonical" in txt

def test_freeze_lists_surface():
    txt = Path("FREEZE.md").read_text()
    for f in ["README.md", "STATUS.md", "FREEZE.md", "CITATION.cff"]:
        assert f in txt
