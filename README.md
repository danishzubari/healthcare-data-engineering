# Healthcare Data Engineering Platform

[![Pipeline](https://github.com/danishzubari/healthcare-data-engineering/actions/workflows/pipeline.yml/badge.svg)](https://github.com/danishzubari/healthcare-data-engineering/actions/workflows/pipeline.yml)

An end-to-end data engineering portfolio project built around public US healthcare data from the Centers for Medicare & Medicaid Services (CMS).

## Live project

**GitHub Pages:** `https://danishzubari.github.io/healthcare-data-engineering/`

The Pages site is built from generated analytics produced by the automated pipeline.

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
Interactive dashboard
          |
          v
GitHub Pages
```

## Engineering capabilities demonstrated

- REST/API healthcare data ingestion
- Pagination and retry/backoff
- Raw-to-analytics transformation
- Schema and data-quality validation
- Duplicate handling
- Analytical SQL
- Automated tests with pytest
- GitHub Actions CI/CD
- Automated GitHub Pages deployment
- Static JavaScript dashboard

## Data source

The initial source is the CMS Provider Data Catalog **Doctors & Clinicians** dataset (`mj5m-pzi6`). The pipeline uses the CMS datastore API and does not commit the full source dataset to Git.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Development run
python -m src.ingestion.run_pipeline --max-rows 10000

# Full source run
python -m src.ingestion.run_pipeline

pytest -q
```

The pipeline writes the raw extract to `data/raw/providers.csv` and compact analytical outputs to `data/analytics/`.

## Automated deployment

Every push to `main` runs tests, executes a 10,000-row CMS pipeline build, generates dashboard datasets, and deploys the `dashboard/` directory to GitHub Pages. A manual full-size run can be triggered later when the workflow is adjusted for the desired refresh size.

## Repository structure

```text
.github/workflows/     CI and deployment automation
src/ingestion/         CMS extraction and pipeline runner
src/transformation/   cleaning and standardization
src/quality/           data quality checks
src/analytics/         analytical metrics
tests/                 automated tests
sql/                   analytical SQL
dashboard/             GitHub Pages application
docs/                  architecture and methodology
data/analytics/        compact generated dashboard datasets
```

## Portfolio talking points

This project is deliberately structured as an engineering system rather than a notebook-only analysis. The key design decision is to keep large raw source data outside Git while generating small, versionable analytical outputs for the presentation layer. The workflow provides a reproducible path from an external healthcare source to a public data product.

## Responsible use

This project uses public provider metadata for engineering demonstration. It is not a clinical decision-support system and should not be used to make medical decisions.
