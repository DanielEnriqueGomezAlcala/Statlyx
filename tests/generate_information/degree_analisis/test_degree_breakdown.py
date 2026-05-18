import json

import pandas as pd
import pytest
from unittest.mock import MagicMock

from functions.generate_information.degree_analisis.degree_breakdown import (
    generate_degree_breakdown,
)

MODULE = "functions.generate_information.degree_analisis.degree_breakdown"


@pytest.fixture
def df():
    return pd.DataFrame(
        {
            "Anio": ["2022-23", "2023-24"],
            "Tasa_Exito": [88.0, 90.0],
            "Tasa_Rendimiento": [70.0, 72.0],
        }
    )


def _common_mocks(mocker, generate_text_rv="texto"):
    mocker.patch(f"{MODULE}.generate_text", return_value=generate_text_rv)
    mocker.patch(f"{MODULE}.save_chart_image")
    mocker.patch(f"{MODULE}.static_chart_lines", return_value=MagicMock())
    mocker.patch(f"{MODULE}.static_chart_table", return_value=MagicMock())


def test_output_has_expected_keys(df, tmp_path, mocker):
    _common_mocks(mocker, json.dumps({"conclusion": "ok", "recomendaciones": ["r1"]}))
    result = generate_degree_breakdown(
        df,
        str(tmp_path),
        ["graficas-lineas", "graficas-tablas"],
        institucion="ULL",
        titulacion="Informática",
    )
    assert {"tasas", "resume_conclusion", "resume_bullets"} <= result.keys()


def test_only_present_columns_processed(df, tmp_path, mocker):
    _common_mocks(mocker, json.dumps({"conclusion": "ok", "recomendaciones": []}))
    result = generate_degree_breakdown(
        df, str(tmp_path), [], institucion="ULL", titulacion="Informática"
    )
    names = [t["name"] for t in result["tasas"]]
    assert len(names) == 2
    assert "Tasa de abandono" not in names
    assert "Tasa de graduación" not in names


def test_invalid_json_resume_does_not_raise(df, tmp_path, mocker):
    _common_mocks(mocker, "esto no es json valido")
    result = generate_degree_breakdown(
        df, str(tmp_path), [], institucion="ULL", titulacion="Informática"
    )
    assert "ERROR" in result["resume_conclusion"]
    assert result["resume_bullets"] == []
