"""Run ingestion, transformation, quality checks and analytics locally or in CI."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from src.analytics.metrics import records_by_column
from src.ingestion.cms_api import iter_pages, rows_to_frame, validate_schema
from src.quality.data_quality import assert_required_columns
from src.transformation.transform import remove_exact_duplicates, standardize_columns

RAW_PATH = Path("data/raw/providers.csv")
ANALYTICS_PATH = Path("data/analytics")


def run(max_rows: int | None = None) -> dict[str, int]:
    frames: list[pd.DataFrame] = []

    for _, rows, _ in iter_pages(max_rows=max_rows):
        frame = rows_to_frame(rows)
        validate_schema(frame)
        frames.append(frame)

    if not frames:
        raise RuntimeError("CMS returned no records")

    raw = pd.concat(frames, ignore_index=True)
    RAW_PATH.parent.mkdir(parents=True, exist_ok=True)
    raw.to_csv(RAW_PATH, index=False)

    transformed = remove_exact_duplicates(standardize_columns(raw))
    assert_required_columns(transformed, ["npi", "pri_spec", "state", "telehlth"])

    ANALYTICS_PATH.mkdir(parents=True, exist_ok=True)
    records_by_column(transformed, "state").head(20).to_csv(
        ANALYTICS_PATH / "providers_by_state.csv", index=False
    )
    records_by_column(transformed, "pri_spec").head(20).to_csv(
        ANALYTICS_PATH / "providers_by_specialty.csv", index=False
    )

    return {"raw_rows": len(raw), "processed_rows": len(transformed)}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-rows", type=int, default=10000)
    args = parser.parse_args()
    print(run(args.max_rows))


if __name__ == "__main__":
    main()
