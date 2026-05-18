import pandas as pd
import pytest
from unittest.mock import MagicMock

from functions.generate_information.subject_analisis.call_breakdown import (
    generate_call_breakdown,
)

MODULE = "functions.generate_information.subject_analisis.call_breakdown"


@pytest.fixture
def df():
    return pd.DataFrame(
        {
            "Curso": [1, 1, 2],
            "Convocatoria": ["Enero", "Mayo", "Enero"],
            "Grupo": [1, 1, 1],
            "Asignatura": ["MAT", "FIS", "PRG"],
            "Anio": ["2022-23", "2022-23", "2022-23"],
            "Tasa_Eficiencia": [0.88, 0.85, 0.90],
            "Tasa_Exito": [0.70, 0.68, 0.75],
        }
    )


def _common_mocks(mocker):
    mocker.patch(f"{MODULE}.generate_text", return_value="texto generado")
    mocker.patch(f"{MODULE}.save_chart_image")
    mocker.patch(f"{MODULE}.static_chart_lines", return_value=MagicMock())
    mocker.patch(f"{MODULE}.static_chart_table", return_value=MagicMock())
    mocker.patch(
        f"{MODULE}.static_chart_bars_breakdown_resume", return_value=MagicMock()
    )


def test_output_has_expected_keys(df, tmp_path, mocker):
    _common_mocks(mocker)
    result = generate_call_breakdown(
        df, str(tmp_path), [], institucion="ULL", titulacion="Informática"
    )
    assert "breakdown" in result
    assert "resume_text" in result


def test_single_group_does_not_raise(tmp_path, mocker):
    _common_mocks(mocker)
    df_single = pd.DataFrame(
        {
            "Curso": [1, 1],
            "Convocatoria": ["Enero", "Enero"],
            "Grupo": [1, 1],
            "Asignatura": ["MAT", "FIS"],
            "Anio": ["2022-23", "2023-24"],
            "Tasa_Eficiencia": [0.88, 0.85],
            "Tasa_Exito": [0.70, 0.68],
        }
    )
    result = generate_call_breakdown(
        df_single, str(tmp_path), [], institucion="ULL", titulacion="Informática"
    )
    assert len(result["breakdown"]) == 1
    assert (
        result["breakdown"][0]["calls"][0]["groups"][0]["name"]
        == "Grupo 1 (Turno mañana)"
    )
