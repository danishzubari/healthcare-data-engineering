# Healthcare Data Engineering Platform

[![Pipeline](https://github.com/danishzubari/healthcare-data-engineering/actions/workflows/pipeline.yml/badge.svg)](https://github.com/danishzubari/healthcare-data-engineering/actions/workflows/pipeline.yml)

An end-to-end data engineering portfolio project built around public US healthcare data from the Centers for Medicare & Medicaid Services (CMS).

The project demonstrates API/data ingestion, data quality, transformation, analytics modeling, automated testing, CI/CD, and publication through GitHub Pages.

## Architecture

```text
CMS public data
      |
      v
Python ingestion
      |
      v
Raw data layer
      |
      v
Validation + quality checks
      |
      v
Transformation / analytical model
      |
      +------> SQL analytics
      |
      v
Static dashboard
      |
      v
GitHub Pages

GitHub Actions automates the pipeline and deployment.
```

## Project goals

- Build a reproducible healthcare data pipeline.
- Separate extraction, transformation, quality, and analytics concerns.
- Produce small, versionable analytical outputs rather than committing large raw files.
- Demonstrate production-oriented engineering practices in a public repository.

## Technology

- Python
- Pandas
- Requests
- SQL
- Pytest
- GitHub Actions
- GitHub Pages
- HTML / CSS / JavaScript

## Data source

The first pipeline targets the CMS Provider Data Catalog and the Doctors & Clinicians dataset. See `docs/methodology.md` for source and methodology notes.

## Repository structure

```text
.github/workflows/     CI and deployment automation
src/ingestion/         CMS extraction
src/transformation/   cleaning and standardization
src/quality/           data quality checks
src/analytics/         analytical metrics
tests/                 automated tests
sql/                   analytical SQL
dashboard/             GitHub Pages site
docs/                  architecture and methodology
data/analytics/        small generated dashboard datasets
```

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m src.ingestion.cms_api
python -m src.transformation.transform
python -m src.analytics.metrics
pytest
```

## Engineering roadmap

- [x] Repository foundation
- [x] Modular pipeline skeleton
- [x] Automated quality checks
- [x] CI workflow
- [ ] CMS production ingestion
- [ ] Provider analytical model
- [ ] Healthcare KPI dashboard
- [ ] GitHub Pages deployment

## Responsible use

This project uses public aggregate/provider metadata for engineering demonstration. It is not a clinical decision-support system and should not be used to make medical decisions.
