import pandas as pd
import pytest
from unittest.mock import MagicMock

from functions.generate_information.subject_analisis.subject_breakdown import (
    generate_subject_breakdown,
)

MODULE = "functions.generate_information.subject_analisis.subject_breakdown"


@pytest.fixture
def df():
    return pd.DataFrame(
        {
            "Curso": [1, 1, 2],
            "Cuatrimestre": [1, 1, 1],
            "Asignatura": ["MAT", "FIS", "PRG"],
            "Anio": ["2022-23", "2022-23", "2022-23"],
            "Tasa_Exito": [88.0, 85.0, 90.0],
            "Tasa_Rendimiento": [70.0, 68.0, 75.0],
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
    result = generate_subject_breakdown(
        df, str(tmp_path), [], institucion="ULL", titulacion="Informática"
    )
    assert "breakdown" in result
    assert "resume_text" in result


def test_groups_by_curso_and_cuatrimestre(df, tmp_path, mocker):
    _common_mocks(mocker)
    result = generate_subject_breakdown(
        df, str(tmp_path), [], institucion="ULL", titulacion="Informática"
    )
    assert len(result["breakdown"]) == 2
    assert len(result["breakdown"][0]["quarter"]) == 1
