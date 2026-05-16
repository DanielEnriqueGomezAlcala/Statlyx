import pandas as pd
from functions.clean_data.clean_data_t1t2 import clean_data_t1t2

EXPECTED_COLUMNS = {
    "Codigo",
    "Tipologia",
    "Curso",
    "Anio",
    "Matriculados",
    "Asignatura",
    "Tasa_Rendimiento",
    "Tasa_Exito",
    "Cuatrimestre",
    "Mencion",
}


def test_output_columns(df_subjects):
    assert set(df_subjects.columns) == EXPECTED_COLUMNS


def test_column_renaming(df_subjects):
    for old_col in [
        "Ass Codnum",
        "Curso Aca",
        "Nummat",
        "Tasa Rend",
        "Tasa Exito",
        "Mención",
    ]:
        assert old_col not in df_subjects.columns


def test_duplicates_removed(tabla_1, tabla_2, tabla_aux):
    tabla_2_dup = pd.concat([tabla_2, tabla_2], ignore_index=True)
    result = clean_data_t1t2(tabla_1, tabla_2_dup, tabla_aux)
    assert not result.duplicated().any()
