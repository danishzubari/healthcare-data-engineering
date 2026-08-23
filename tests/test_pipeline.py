import pandas as pd
import pytest

from src.analytics.metrics import records_by_column
from src.quality.data_quality import assert_required_columns, null_rate
from src.transformation.transform import remove_exact_duplicates, standardize_columns


def test_standardize_columns():
    df = pd.DataFrame({"Provider Name": ["A"]})
    result = standardize_columns(df)
    assert list(result.columns) == ["provider_name"]


def test_remove_exact_duplicates():
    df = pd.DataFrame({"npi": [1, 1, 2]})
    assert len(remove_exact_duplicates(df)) == 2


def test_null_rate():
    df = pd.DataFrame({"state": ["ON", None, "BC"]})
    assert null_rate(df, "state") == pytest.approx(1 / 3)


def test_required_columns():
    df = pd.DataFrame({"npi": [1]})
    with pytest.raises(ValueError):
        assert_required_columns(df, ["npi", "state"])


def test_records_by_column():
    df = pd.DataFrame({"state": ["CA", "CA", "NY"]})
    result = records_by_column(df, "state")
    assert result.loc[result["state"] == "CA", "record_count"].iloc[0] == 2
