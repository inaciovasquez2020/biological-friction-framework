import importlib.util
from pathlib import Path
import pandas as pd
import pytest

PATH = Path(__file__).parents[1] / "apps" / "research_workbench.py"
spec = importlib.util.spec_from_file_location("research_workbench", PATH)
app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app)

def test_gene_list_normalizes_and_deduplicates():
    assert app.parse_gene_list("wnt2b; WNT5A, wnt2b") == ["WNT2B", "WNT5A"]

def test_auc_perfect_reverse_and_ties():
    assert app.safe_auc([0,0,1,1],[0.1,0.2,0.8,0.9]) == 1.0
    assert app.safe_auc([0,0,1,1],[0.9,0.8,0.2,0.1]) == 0.0
    assert app.safe_auc([0,1],[1.0,1.0]) == 0.5
    assert app.safe_auc([1,1],[1.0,2.0]) is None

def test_score_formula_and_coverage():
    score, detail = app.score_row(pd.Series({"A":3.0,"B":1.0,"C":1.0}),["A","B"],["C"],"none",2)
    assert score == 1.0
    assert detail["group_a_used"] == ["A","B"]

def test_log1p_rejects_negative_values():
    with pytest.raises(ValueError, match="nonnegative"):
        app.score_row(pd.Series({"A":-1.0,"C":0.0}),["A"],["C"],"log1p",1)
