import pandas as pd
import pytest
from unittest.mock import MagicMock

from functions.generate_information.subject_analisis.mention_breakdown import (
    generate_mention_breakdown,
)

MODULE = "functions.generate_information.subject_analisis.mention_breakdown"


@pytest.fixture
def df():
    return pd.DataFrame(
        {
            "Mencion": ["Mención A", "Mención A", "Mención B"],
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
    result = generate_mention_breakdown(
        df, str(tmp_path), [], institucion="ULL", titulacion="Informática"
    )
    assert "breakdown" in result
    assert "resume_text" in result


def test_single_mencion_does_not_raise(tmp_path, mocker):
    _common_mocks(mocker)
    df_single = pd.DataFrame(
        {
            "Mencion": ["Mención A", "Mención A"],
            "Asignatura": ["MAT", "FIS"],
            "Anio": ["2022-23", "2023-24"],
            "Tasa_Exito": [88.0, 85.0],
            "Tasa_Rendimiento": [70.0, 68.0],
        }
    )
    result = generate_mention_breakdown(
        df_single, str(tmp_path), [], institucion="ULL", titulacion="Informática"
    )
    assert len(result["breakdown"]) == 1
