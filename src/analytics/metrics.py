"""Healthcare analytics functions."""

import pandas as pd


def records_by_column(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """Return record counts and shares for a categorical column."""
    counts = df[column].fillna("Unknown").value_counts(dropna=False).rename("record_count")
    result = counts.reset_index()
    result.columns = [column, "record_count"]
    result["share"] = result["record_count"] / result["record_count"].sum()
    return result
