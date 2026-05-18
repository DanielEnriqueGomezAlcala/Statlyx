import pytest
from pydantic import ValidationError

from functions.llm.prompts.degree_analisis import (
    PromptResumenDesgloseTitulacion,
    PromptTasaAbandono,
    PromptTasaEficiencia,
    PromptTasaExito,
    PromptTasaGraduacion,
    PromptTasaRendimiento,
)

CLASSES = [
    PromptTasaExito,
    PromptTasaRendimiento,
    PromptTasaEficiencia,
    PromptTasaGraduacion,
    PromptTasaAbandono,
    PromptResumenDesgloseTitulacion,
]

ARGS = {
    "universidad": "ULL",
    "titulacion": "Ingeniería Informática",
    "datos": "2022-23: 80%",
}


@pytest.mark.parametrize("cls", CLASSES)
def test_build_returns_nonempty(cls):
    assert cls(**ARGS).build()


@pytest.mark.parametrize("cls", CLASSES)
def test_build_contains_injected_values(cls):
    prompt = cls(**ARGS).build()
    assert "ULL" in prompt
    assert "Ingeniería Informática" in prompt
    assert "2022-23: 80%" in prompt


@pytest.mark.parametrize("cls", CLASSES)
def test_empty_universidad_raises(cls):
    with pytest.raises(ValidationError):
        cls(universidad="", titulacion="Ingeniería", datos="datos")


@pytest.mark.parametrize("cls", CLASSES)
def test_empty_titulacion_raises(cls):
    with pytest.raises(ValidationError):
        cls(universidad="ULL", titulacion="", datos="datos")


@pytest.mark.parametrize("cls", CLASSES)
def test_empty_datos_raises(cls):
    with pytest.raises(ValidationError):
        cls(universidad="ULL", titulacion="Ingeniería", datos="")
