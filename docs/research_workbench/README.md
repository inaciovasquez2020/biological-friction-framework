# BFF Research Workbench

A configurable app for expression-matrix quality checks and exploratory gene-score evaluation.

## Run locally

Requires Python 3.11 or newer.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-workbench.txt
streamlit run apps/research_workbench.py
```

## Run the container

Build from the repository root:

```bash
docker build -t bff-research-workbench:local .
docker run --rm -p 8501:8501 bff-research-workbench:local
```

Open `http://localhost:8501`. The container accepts uploaded CSV files through the Streamlit interface and does not fetch research data automatically. The image is intended for local research use.

A GitHub Actions workflow builds the container on pull requests and publishes it to GitHub Container Registry (GHCR) only when a version tag matching `v*` is pushed. After this work is merged and a version tag is deliberately created, the image name will be:

```text
ghcr.io/inaciovasquez2020/biological-friction-framework:<version>
```

For example, replace `<version>` with the published tag. Check the package visibility and repository link in GitHub Packages before sharing the image. A configured workflow is not evidence that an image has already been published.

## Input

Upload a CSV with one sample per row and one column per gene, plus optional `sample_id` and `outcome` columns. Example values below are synthetic:

```csv
sample_id,outcome,WNT2B,WNT5A,FZD1,RNF43
S01,NONRESPONDER,1.2,0.8,2.1,0.4
S02,RESPONDER,0.4,0.3,0.7,2.2
```

## Workflows

- **Data quality audit:** missing/nonnumeric values, negative values, unique values, and outcome counts.
- **Evaluate a predefined score:** starts with the exploratory melanoma Wnt gene groups.
- **Explore a custom gene score:** set custom gene groups and transformation.

Scores use `mean(group A) - mean(group B)`. The transformation and gene groups are recorded in the downloadable JSON receipt. Descriptive AUROC is available when two outcome labels are present. It is not independent validation.

## Limitations

The current melanoma Wnt candidate has reported AUROC 0.5208 on 24 GSE165745 samples. The source preprocessing is unresolved; selecting `log1p` does not make it validated. No clinical validity, calibration, treatment benefit, or safety is established. Do not use for diagnosis or treatment decisions.

## Privacy

Local use is preferred for sensitive research data. A hosted deployment processes uploaded files on that deployment's server. Do not upload direct identifiers or protected health information unless the environment and governance have been independently approved.

## Outputs

The app can download a quality-audit JSON receipt, per-sample scores CSV, blocked-sample CSV, and a run JSON receipt. All receipts mark clinical validity as `NOT_ESTABLISHED`.
