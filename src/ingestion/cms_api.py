"""CMS Provider Data Catalog ingestion.

The CMS API exposes current datasets through a paginated datastore query API.
The dataset ID is stable across refreshes, so the pipeline can safely use the
Doctors & Clinicians dataset without hard-coding a changing distribution ID.
"""

from __future__ import annotations

import argparse
import logging
import time
from collections.abc import Iterator

import pandas as pd
import requests

CMS_BASE_URL = "https://data.cms.gov/provider-data/api/1"
DATASET_ID = "mj5m-pzi6"
# CMS documents a maximum batch size of 1,500 for the Provider Data Catalog API.
PAGE_SIZE = 1500
REQUIRED_COLUMNS = {"npi", "pri_spec", "state", "telehlth"}

LOGGER = logging.getLogger(__name__)


def fetch_page(
    session: requests.Session,
    offset: int,
    limit: int = PAGE_SIZE,
    retries: int = 5,
) -> dict:
    """Fetch one CMS API page with exponential backoff."""
    url = f"{CMS_BASE_URL}/datastore/query/{DATASET_ID}/0"
    params = {"offset": offset, "limit": min(limit, PAGE_SIZE)}

    for attempt in range(retries):
        try:
            response = session.get(url, params=params, timeout=60)
            response.raise_for_status()
            payload = response.json()
            if "results" not in payload or "count" not in payload:
                raise ValueError("Unexpected CMS API response shape")
            return payload
        except (requests.RequestException, ValueError) as exc:
            if attempt == retries - 1:
                raise
            wait = 2**attempt
            LOGGER.warning("CMS request failed (%s); retrying in %ss", exc, wait)
            time.sleep(wait)

    raise RuntimeError("Unreachable")


def iter_pages(max_rows: int | None = None) -> Iterator[tuple[int, list[dict], int]]:
    """Yield (offset, rows, total_rows) pages from CMS."""
    with requests.Session() as session:
        offset = 0
        total_rows: int | None = None
        remaining = max_rows

        while remaining is None or remaining > 0:
            requested = PAGE_SIZE if remaining is None else min(PAGE_SIZE, remaining)
            payload = fetch_page(session, offset, requested)
            rows = payload["results"]
            total_rows = int(payload["count"])

            if not rows:
                break

            yield offset, rows, total_rows
            offset += len(rows)

            if remaining is not None:
                remaining -= len(rows)

            if offset >= total_rows:
                break


def rows_to_frame(rows: list[dict]) -> pd.DataFrame:
    """Convert API rows to a standardized dataframe."""
    df = pd.DataFrame(rows)
    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.lower()
        .str.replace(r"[^a-z0-9]+", "_", regex=True)
        .str.strip("_")
    )
    return df


def validate_schema(df: pd.DataFrame) -> None:
    """Validate columns required by the analytics pipeline."""
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"CMS response missing required columns: {sorted(missing)}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest CMS Doctors & Clinicians data")
    parser.add_argument("--max-rows", type=int, default=None, help="Optional row cap for development/CI")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    rows_seen = 0

    for offset, rows, total_rows in iter_pages(args.max_rows):
        frame = rows_to_frame(rows)
        validate_schema(frame)
        rows_seen += len(frame)
        LOGGER.info("Fetched %s/%s rows", rows_seen, min(total_rows, args.max_rows or total_rows))

    LOGGER.info("CMS ingestion complete: %s rows", rows_seen)


if __name__ == "__main__":
    main()
