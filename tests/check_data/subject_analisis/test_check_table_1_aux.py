import pandas as pd
import pytest

from functions.check_data.subject_analisis.check_table_1_aux import check_table_1_aux


def test_empty_df_raises():
    with pytest.raises(ValueError):
        check_table_1_aux(pd.DataFrame())


def test_missing_columns_raises():
    df = pd.DataFrame({"Código": [1]})
    with pytest.raises(ValueError):
        check_table_1_aux(df)


def test_valid_df_returns_true(tabla_aux):
    assert check_table_1_aux(tabla_aux) is True
