import pandas as pd
import pytest

from functions.check_data.subject_analisis.check_table_call import check_table_call


def test_empty_df_raises():
    with pytest.raises(ValueError, match="La tabla de convocatorias está vacía"):
        check_table_call(pd.DataFrame())


def test_missing_columns_raises():
    df = pd.DataFrame({"Curso": ["2022-2023"]})
    with pytest.raises(
        ValueError, match="La tabla de convocatorias no tiene las columnas"
    ):
        check_table_call(df)


def test_valid_df_returns_true(tabla_call):
    assert check_table_call(tabla_call) is True
