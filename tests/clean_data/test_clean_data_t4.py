EXPECTED_COLUMNS = {
    "Anio",
    "Tasa_Exito",
    "Tasa_Abandono",
    "Tasa_Rendimiento",
    "Tasa_Eficiencia",
    "Tasa_Graduacion",
}


def test_one_row_per_year(tabla_4, df_degrees):
    year_cols = [c for c in tabla_4.columns if c != "Unnamed: 0"]
    assert len(df_degrees) == len(year_cols)


def test_only_five_indicators(df_degrees):
    assert set(df_degrees.columns) == EXPECTED_COLUMNS


def test_column_renaming(df_degrees):
    for old_col in [
        "Unnamed: 0",
        "Indicador",
        "Tasa éxito",
        "Tasa abandono",
        "Tasa rendimiento",
        "Tasa eficiencia",
        "Tasa graduación",
    ]:
        assert old_col not in df_degrees.columns
