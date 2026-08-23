# Methodology

## Source

The project uses public data from the US Centers for Medicare & Medicaid Services (CMS) Provider Data Catalog.

The initial production source is the Doctors & Clinicians dataset. Source selection is intentional: it is large enough to demonstrate ingestion and transformation while remaining publicly accessible and machine-readable.

## Privacy and responsible use

The project does not require patient-level protected health information. It is an engineering demonstration using public provider metadata. Results are descriptive analytics and are not clinical recommendations.

## Reproducibility

The pipeline should record the source endpoint, extraction timestamp, row count and validation results for each run. Raw data is treated as an external source artifact rather than a Git repository asset.

## Planned metrics

- Provider counts by state
- Provider counts by specialty
- Telehealth availability
- Geographic concentration
- Data completeness and uniqueness
