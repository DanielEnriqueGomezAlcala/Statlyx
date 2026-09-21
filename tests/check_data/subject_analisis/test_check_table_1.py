import pandas as pd
import pytest

from functions.check_data.subject_analisis.check_table_1 import check_table_1


def test_empty_df_raises():
    with pytest.raises(ValueError, match="La tabla 1 está vacía"):
        check_table_1(pd.DataFrame())


def test_missing_columns_raises():
    df = pd.DataFrame({"Ass Codnum": [1]})
    with pytest.raises(ValueError, match="La tabla 1 no tiene las columnas requeridas"):
        check_table_1(df)


def test_valid_df_returns_true(tabla_1):
    assert check_table_1(tabla_1) is True
