"""Reusable data quality checks for the healthcare pipeline."""

import pandas as pd


def null_rate(df: pd.DataFrame, column: str) -> float:
    """Return the fraction of null values in a column."""
    if column not in df.columns:
        raise KeyError(f"Missing required column: {column}")
    return float(df[column].isna().mean())


def assert_required_columns(df: pd.DataFrame, columns: list[str]) -> None:
    """Raise an error when required columns are absent."""
    missing = sorted(set(columns) - set(df.columns))
    if missing:
        raise ValueError(f"Missing required columns: {missing}")


def assert_unique(df: pd.DataFrame, column: str) -> None:
    """Raise an error when a key contains duplicates."""
    if df[column].duplicated().any():
        raise ValueError(f"Column is not unique: {column}")
