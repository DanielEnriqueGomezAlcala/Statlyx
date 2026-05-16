def test_eficiencia_exito_scaled(df_call):
    assert list(df_call["Tasa_Eficiencia"]) == [72.4, 68.1, 75.3]
    assert list(df_call["Tasa_Exito"]) == [89.2, 82.5, 91.0]


def test_convocatorias_mapped(df_call):
    assert set(df_call["Convocatoria"]) == {"Enero", "Mayo", "Julio"}


def test_merge_adds_curso(df_call):
    assert "Curso" in df_call.columns
    assert df_call["Curso"].notna().all()
