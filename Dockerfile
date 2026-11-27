FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

WORKDIR /app

LABEL org.opencontainers.image.title="BFF Research Workbench"
LABEL org.opencontainers.image.description="Research-only expression-matrix quality audit and exploratory gene-score workbench"
LABEL org.opencontainers.image.source="https://github.com/inaciovasquez2020/biological-friction-framework"

COPY requirements-workbench.txt /app/requirements-workbench.txt
RUN python -m pip install --upgrade pip && \
    python -m pip install -r /app/requirements-workbench.txt

COPY apps/research_workbench.py /app/apps/research_workbench.py
COPY docs/research_workbench/README.md /app/docs/research_workbench/README.md

EXPOSE 8501

CMD ["streamlit", "run", "apps/research_workbench.py", "--server.address=0.0.0.0", "--server.port=8501", "--server.headless=true"]
