"""Regression tests for repository-contained graph evidence files.

No biological hypothesis or certificate data is modified. Standard library only.
"""
import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "infra" / "ci" / "verify_melanoma_interaction_graph.py"
spec = importlib.util.spec_from_file_location("melanoma_graph_verifier", SOURCE)
verifier = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verifier)


class EvidenceContainmentTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        base = Path(self.tmp.name)
        self.repo = base / "repo"
        (self.repo / "docs").mkdir(parents=True)
        (self.repo / "docs" / "inside.md").write_text("internal", encoding="utf-8")
        self.external = base / "external.md"
        self.external.write_text("external", encoding="utf-8")
        (self.repo / "docs" / "escape.md").symlink_to(self.external)
        (self.repo / "docs" / "internal_link.md").symlink_to(self.repo / "docs" / "inside.md")

    def verify(self, paths):
        with patch.object(verifier, "ROOT", self.repo):
            verifier._require_evidence(paths)

    def test_valid_internal(self): self.verify(["docs/inside.md"])
    def test_valid_internal_symlink(self): self.verify(["docs/internal_link.md"])
    def test_parent_escape(self):
        with self.assertRaises(AssertionError): self.verify(["../external.md"])
    def test_absolute_escape(self):
        with self.assertRaises(AssertionError): self.verify([str(self.external)])
    def test_symlink_escape(self):
        with self.assertRaises(AssertionError): self.verify(["docs/escape.md"])
    def test_missing(self):
        with self.assertRaises(AssertionError): self.verify(["docs/missing.md"])
    def test_empty_list(self):
        with self.assertRaises(AssertionError): self.verify([])
    def test_empty_string(self):
        with self.assertRaises(AssertionError): self.verify([""])
    def test_non_string(self):
        with self.assertRaises(AssertionError): self.verify([None])

if __name__ == "__main__":
    unittest.main()
