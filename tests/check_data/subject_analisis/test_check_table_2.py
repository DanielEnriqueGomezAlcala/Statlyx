import pandas as pd
import pytest

from functions.check_data.subject_analisis.check_table_2 import check_table_2


def test_empty_df_raises():
    with pytest.raises(ValueError, match="La tabla 2 está vacía"):
        check_table_2(pd.DataFrame())


def test_missing_columns_raises():
    df = pd.DataFrame({"Curso Aca": ["2022-23"]})
    with pytest.raises(ValueError, match="La tabla 2 no tiene las columnas requeridas"):
        check_table_2(df)


def test_valid_df_returns_true(tabla_2):
    assert check_table_2(tabla_2) is True
