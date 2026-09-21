import pandas as pd
import pytest

from functions.check_data.degree_analisis.check_table_4 import check_table_4


def test_empty_df_raises():
    with pytest.raises(ValueError, match="La tabla 4 está vacía"):
        check_table_4(pd.DataFrame())


def test_missing_rows_raises():
    df = pd.DataFrame({"Unnamed: 0": ["fila irrelevante"], "2022-23": [0.0]})
    with pytest.raises(ValueError, match="La tabla 4 no contiene las filas requeridas"):
        check_table_4(df)


def test_valid_df_returns_true(tabla_4):
    assert check_table_4(tabla_4) is True
