import pandas as pd
import pytest

from utils.filter_by_year import filter_by_year


@pytest.fixture
def df():
    return pd.DataFrame(
        {
            "Anio": ["2018-19", "2020-21", "2022-23", "2023-24", None],
            "Valor": [1, 2, 3, 4, 5],
        }
    )


def test_rows_in_range_included(df):
    result = filter_by_year(df, 2020, 2022)
    assert set(result["Anio"]) == {"2020-21", "2022-23"}


def test_rows_outside_range_excluded(df):
    result = filter_by_year(df, 2020, 2022)
    assert "2018-19" not in result["Anio"].values
    assert "2023-24" not in result["Anio"].values


def test_nan_anio_discarded_without_error(df):
    result = filter_by_year(df, 2018, 2024)
    assert result["Anio"].notna().all()
