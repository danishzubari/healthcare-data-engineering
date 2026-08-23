# Healthcare Data Engineering Platform

[![Pipeline](https://github.com/danishzubari/healthcare-data-engineering/actions/workflows/pipeline.yml/badge.svg)](https://github.com/danishzubari/healthcare-data-engineering/actions/workflows/pipeline.yml)

An end-to-end data engineering portfolio project built around public US healthcare data from the Centers for Medicare & Medicaid Services (CMS).

## Architecture

```text
CMS Provider Data Catalog
          |
          v
Paginated Python ingestion
          |
          v
Raw provider dataset
          |
          v
Schema + data-quality checks
          |
          v
Standardization + deduplication
          |
          +------> SQL analytics
          |
          v
State / specialty aggregates
          |
          v
Interactive GitHub Pages dashboard
```

## Engineering capabilities demonstrated

- REST/API-style healthcare data ingestion
- Pagination and retry/backoff
- Raw-to-analytics transformation
- Schema and data-quality validation
- Duplicate handling
- Analytical SQL
- Automated tests with pytest
- GitHub Actions CI/CD
- Static web publishing through GitHub Pages

## Data source

The initial source is the CMS Provider Data Catalog **Doctors & Clinicians** dataset (`mj5m-pzi6`). The pipeline uses the CMS datastore API and does not commit the full source dataset to Git.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Development run: ingest 10,000 records
python -m src.ingestion.run_pipeline --max-rows 10000

# Full source run: omit --max-rows
python -m src.ingestion.run_pipeline

pytest -q
```

The pipeline writes the raw extract to `data/raw/providers.csv` and compact analytical outputs to `data/analytics/`.

## Repository structure

```text
.github/workflows/     CI and deployment automation
src/ingestion/         CMS extraction and pipeline runner
src/transformation/   cleaning and standardization
src/quality/           data quality checks
src/analytics/         analytical metrics
tests/                 automated tests
sql/                   analytical SQL
dashboard/             GitHub Pages site
docs/                  architecture and methodology
data/analytics/        small generated dashboard datasets
```

## Roadmap

- [x] Repository foundation
- [x] CMS paginated ingestion client
- [x] Retry/backoff and schema validation
- [x] Transformation and analytics modules
- [x] Analytical SQL
- [x] Automated tests
- [ ] Production pipeline run in GitHub Actions
- [ ] Interactive KPI dashboard
- [ ] GitHub Pages deployment
- [ ] Data-quality report in dashboard

## Responsible use

This project uses public provider metadata for engineering demonstration. It is not a clinical decision-support system and should not be used to make medical decisions.
