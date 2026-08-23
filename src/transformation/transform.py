"""Standardize raw provider datasets into analytics-ready tables."""

import pandas as pd


def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize column names for downstream processing."""
    result = df.copy()
    result.columns = (
        result.columns.astype(str)
        .str.strip()
        .str.lower()
        .str.replace(r"[^a-z0-9]+", "_", regex=True)
        .str.strip("_")
    )
    return result


def remove_exact_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Remove exact duplicate records."""
    return df.drop_duplicates().reset_index(drop=True)
