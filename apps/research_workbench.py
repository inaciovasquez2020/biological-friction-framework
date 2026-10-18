from __future__ import annotations
import hashlib, io, json, math
from datetime import datetime, timezone
import pandas as pd
import streamlit as st

APP_VERSION = "BFF Research Workbench 0.1.0"
DEFAULT_A = ["WNT2B","WNT5A","WNT7B","WNT8B","FZD1","FZD2","FZD4","FZD5","FZD7","FZD8","FZD10","LRP5","LRP6","DKK2","SFRP2","SFRP4","PYGO1","DVL1"]
DEFAULT_B = ["RNF43"]

def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()

def parse_gene_list(text: str) -> list[str]:
    return list(dict.fromkeys(x.strip().upper() for x in text.replace(";", ",").replace("\n", ",").split(",") if x.strip()))

def safe_auc(labels: list[int], scores: list[float]) -> float | None:
    positives, negatives = sum(labels), len(labels) - sum(labels)
    if positives == 0 or negatives == 0: return None
    order = sorted(range(len(scores)), key=lambda i: scores[i])
    ranks = [0.0] * len(scores); i = 0
    while i < len(order):
        j = i + 1
        while j < len(order) and scores[order[j]] == scores[order[i]]: j += 1
        rank = ((i + 1) + j) / 2
        for k in range(i, j): ranks[order[k]] = rank
        i = j
    rank_sum = sum(ranks[i] for i, y in enumerate(labels) if y == 1)
    return (rank_sum - positives * (positives + 1) / 2) / (positives * negatives)

def score_row(row: pd.Series, group_a: list[str], group_b: list[str], transform: str, minimum: int):
    a = [g for g in group_a if g in row.index and pd.notna(row[g])]
    b = [g for g in group_b if g in row.index and pd.notna(row[g])]
    if len(a) < minimum or not b:
        raise ValueError(f"insufficient coverage: group A {len(a)}/{len(group_a)}, group B {len(b)}/{len(group_b)}")
    values = {}
    for gene in a + b:
        value = float(row[gene])
        if not math.isfinite(value): raise ValueError(f"non-finite value in {gene}")
        if transform == "log1p":
            if value < 0: raise ValueError(f"log1p requires nonnegative values; {gene}={value}")
            value = math.log1p(value)
        values[gene] = value
    score = sum(values[g] for g in a) / len(a) - sum(values[g] for g in b) / len(b)
    return score, {"group_a_used": a, "group_b_used": b, "formula": "mean(group A) - mean(group B)", "transformation": transform}

def main():
    st.set_page_config(page_title="BFF Research Workbench", layout="wide")
    st.title("BFF Research Workbench")
    st.caption(f"{APP_VERSION} · configurable exploratory analysis")
    st.warning("Research use only. Not for diagnosis, treatment selection, or patient care. Do not upload identifiable or sensitive patient data to a hosted deployment.")
    st.sidebar.header("Choose workflow")
    mode = st.sidebar.radio("Workflow", ["Data quality audit", "Evaluate a predefined score", "Explore a custom gene score"])
    upload = st.sidebar.file_uploader("Expression matrix CSV", type=["csv"])
    if upload is None:
        st.info("Upload a CSV with one sample per row and gene symbols as columns.")
        st.code("sample_id,outcome,WNT2B,WNT5A,FZD1,RNF43\nS01,NONRESPONDER,1.2,0.8,2.1,0.4\nS02,RESPONDER,0.4,0.3,0.7,2.2", language="csv")
        st.write("The example values are synthetic. No data is fetched or transmitted automatically.")
        return
    raw = upload.getvalue()
    try: df = pd.read_csv(io.BytesIO(raw))
    except Exception as exc:
        st.error(f"Could not read CSV: {exc}"); return
    if df.empty:
        st.error("CSV contains no data rows."); return
    df.columns = [str(c).strip() for c in df.columns]
    st.subheader("1. Dataset")
    c1,c2,c3 = st.columns(3); c1.metric("Samples",len(df)); c2.metric("Columns",len(df.columns)); c3.metric("Input SHA-256",sha256_bytes(raw)[:12])
    st.dataframe(df.head(10), use_container_width=True)
    ids = ["(row number)"] + list(df.columns)
    id_col = st.selectbox("Sample ID column", ids, index=1 if "sample_id" in df.columns else 0)
    outcomes = ["(no outcome labels)"] + list(df.columns)
    out_default = "outcome" if "outcome" in df.columns else "(no outcome labels)"
    out_col = st.selectbox("Outcome column (optional)", outcomes, index=outcomes.index(out_default))
    reserved = {c for c in [id_col,out_col] if c not in ["(row number)","(no outcome labels)"]}
    expr = df.drop(columns=list(reserved), errors="ignore").copy()
    expr.columns = [str(c).strip().upper() for c in expr.columns]
    for col in expr.columns: expr[col] = pd.to_numeric(expr[col], errors="coerce")
    if mode == "Data quality audit":
        st.subheader("2. Data quality")
        report = pd.DataFrame([{"gene":c,"numeric_values":int(expr[c].notna().sum()),"missing_or_nonnumeric":int(expr[c].isna().sum()),"negative_values":int((expr[c]<0).sum()),"unique_values":int(expr[c].nunique())} for c in expr.columns])
        st.dataframe(report,use_container_width=True)
        if out_col != "(no outcome labels)":
            st.write("Outcome counts"); st.dataframe(df[out_col].astype(str).value_counts(dropna=False).rename_axis("outcome").reset_index(name="n"),use_container_width=True)
        receipt={"app_version":APP_VERSION,"created_utc":datetime.now(timezone.utc).isoformat(),"workflow":mode,"input_sha256":sha256_bytes(raw),"rows":len(df),"columns":list(df.columns),"quality":report.to_dict(orient="records"),"clinical_validity":"NOT_ESTABLISHED"}
        st.download_button("Download quality receipt JSON",json.dumps(receipt,indent=2),"bff_quality_audit.json","application/json")
        return
    st.subheader("2. Score definition")
    if mode == "Evaluate a predefined score":
        a_text=st.text_area("Group A genes (Wnt resistance-associated)",", ".join(DEFAULT_A),height=120)
        b_text=st.text_area("Group B genes (counter-marker)",", ".join(DEFAULT_B),height=60)
        name=st.text_input("Score name","Melanoma Wnt fixed-score candidate v1")
        frozen=st.checkbox("Gene groups and transformation were fixed before viewing outcomes",value=False)
    else:
        a_text=st.text_area("Group A genes (positive contribution)","GENE_A, GENE_B")
        b_text=st.text_area("Group B genes (subtracted contribution)","GENE_C")
        name=st.text_input("Exploratory score name","Custom exploratory gene score")
        frozen=False
    transform=st.selectbox("Expression transformation",["none","log1p"],help="Choose only a transformation justified by source documentation. For GSE165745 the original preprocessing remains unresolved.")
    minimum=st.number_input("Minimum group A genes per sample",min_value=1,max_value=100,value=5)
    st.caption("Formula: mean(transformed group A) − mean(transformed group B). This is not a fitted or clinically validated model.")
    group_a,group_b=parse_gene_list(a_text),parse_gene_list(b_text)
    missing_a=[g for g in group_a if g not in expr.columns]; missing_b=[g for g in group_b if g not in expr.columns]
    st.write(f"Group A found: {len(group_a)-len(missing_a)}/{len(group_a)} · Group B found: {len(group_b)-len(missing_b)}/{len(group_b)}")
    if missing_a: st.caption("Missing group A: "+", ".join(missing_a))
    if missing_b: st.caption("Missing group B: "+", ".join(missing_b))
    if st.button("Run analysis",type="primary"):
        if not group_a or not group_b or set(group_a)&set(group_b):
            st.error("Provide nonempty, nonoverlapping gene groups."); return
        scored,blocked=[],[]
        for ix,row in expr.iterrows():
            sid=str(df.iloc[ix][id_col]) if id_col != "(row number)" else str(ix+1)
            try:
                value,detail=score_row(row,group_a,group_b,transform,int(minimum))
                rec={"sample_id":sid,"score":value,"status":"SCORED","group_a_count":len(detail["group_a_used"]),"group_b_count":len(detail["group_b_used"])}
                if out_col != "(no outcome labels)": rec["outcome"]=str(df.iloc[ix][out_col])
                scored.append(rec)
            except Exception as exc: blocked.append({"sample_id":sid,"reason":str(exc)})
        result=pd.DataFrame(scored)
        st.subheader("3. Results")
        c1,c2=st.columns(2); c1.metric("Samples scored",len(scored)); c2.metric("Samples blocked",len(blocked))
        if not result.empty:
            st.dataframe(result,use_container_width=True)
            st.download_button("Download scores CSV",result.to_csv(index=False),"bff_sample_scores.csv","text/csv")
            st.bar_chart(result.set_index("sample_id")["score"])
        if blocked:
            with st.expander("Blocked samples"):
                st.dataframe(pd.DataFrame(blocked),use_container_width=True)
                st.download_button("Download blocked-sample report",pd.DataFrame(blocked).to_csv(index=False),"bff_blocked_samples.csv","text/csv")
        auc=None; auc_note="Not calculated."
        if out_col != "(no outcome labels)" and not result.empty:
            labels=sorted(result["outcome"].dropna().unique().tolist())
            if len(labels)==2:
                positive=st.selectbox("Outcome label treated as positive for descriptive AUROC",labels)
                if st.button("Calculate descriptive AUROC"):
                    auc=safe_auc([int(x==positive) for x in result["outcome"]],result["score"].astype(float).tolist())
                    auc_note="Descriptive performance on this uploaded cohort only; not independent validation."
                    if auc is not None: st.metric(f"AUROC for {positive}",f"{auc:.4f}"); st.caption(auc_note)
            else: st.info("AUROC requires exactly two outcome classes.")
        receipt={"app_version":APP_VERSION,"created_utc":datetime.now(timezone.utc).isoformat(),"workflow":mode,"score_name":name,"input_sha256":sha256_bytes(raw),"input_rows":len(df),"scored_rows":len(scored),"blocked_rows":len(blocked),"group_a_genes":group_a,"group_b_genes":group_b,"missing_group_a_genes":missing_a,"missing_group_b_genes":missing_b,"transformation":transform,"formula":"mean(group A) - mean(group B)","definition_frozen_before_outcome_review":bool(frozen),"auc":auc,"performance_note":auc_note,"clinical_validity":"NOT_ESTABLISHED","warnings":["Research use only; not for diagnosis or treatment selection.","User-selected gene groups and transformation require scientific justification.","Performance on the uploaded cohort is not independent validation.","No probability calibration or clinical utility analysis is performed."]}
        st.download_button("Download run receipt JSON",json.dumps(receipt,indent=2),"bff_run_receipt.json","application/json")

if __name__ == "__main__":
    main()
