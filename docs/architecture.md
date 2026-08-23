# Architecture

## Current implementation

The repository is structured as a layered pipeline:

1. **Ingestion** — retrieve source data through a small, testable HTTP client.
2. **Transformation** — normalize columns and remove exact duplicates.
3. **Quality** — validate required fields, null rates and uniqueness constraints.
4. **Analytics** — produce reusable categorical metrics such as record counts and shares.
5. **Presentation** — publish a static dashboard through GitHub Pages.
6. **Automation** — run tests automatically with GitHub Actions.

## Target architecture

```text
CMS Provider Data Catalog
          |
          v
      Ingestion
          |
          v
      Raw layer
          |
          v
   Quality validation
          |
          v
   Transformation
          |
          v
 Analytical datasets
      /          \
     v            v
    SQL       Dashboard
                 |
                 v
           GitHub Pages
```

Large raw datasets should be downloaded during pipeline execution rather than committed to Git. Only small analytical outputs and code belong in the repository.
