import pytest
from pydantic import ValidationError

from functions.llm.prompts.subject_analisis import (
    PromptAnalisisPar,
    PromptPeoresAsignaturas,
    PromptResumenDesgloseConvocatoria,
    PromptResumenDesgloseCurso,
    PromptResumenDesgloseMencion,
    PromptResumenDesgloseTipologia,
)

SIMPLE_CLASSES = [
    PromptResumenDesgloseCurso,
    PromptResumenDesgloseTipologia,
    PromptResumenDesgloseMencion,
    PromptResumenDesgloseConvocatoria,
    PromptPeoresAsignaturas,
]

ARGS = {
    "universidad": "ULL",
    "titulacion": "Ingeniería Informática",
    "datos": "dato: 75%",
}

PAR_ARGS = {**ARGS, "contexto_grupo": "Grupo A", "tasa_nombre": "Tasa de Éxito"}


@pytest.mark.parametrize("cls", SIMPLE_CLASSES)
def test_build_returns_nonempty(cls):
    assert cls(**ARGS).build()


@pytest.mark.parametrize("cls", SIMPLE_CLASSES)
def test_build_contains_injected_values(cls):
    prompt = cls(**ARGS).build()
    assert "ULL" in prompt
    assert "Ingeniería Informática" in prompt
    assert "dato: 75%" in prompt


@pytest.mark.parametrize("cls", SIMPLE_CLASSES)
def test_empty_universidad_raises(cls):
    with pytest.raises(ValidationError):
        cls(universidad="", titulacion="Ingeniería", datos="datos")


@pytest.mark.parametrize("cls", SIMPLE_CLASSES)
def test_empty_titulacion_raises(cls):
    with pytest.raises(ValidationError):
        cls(universidad="ULL", titulacion="", datos="datos")


@pytest.mark.parametrize("cls", SIMPLE_CLASSES)
def test_empty_datos_raises(cls):
    with pytest.raises(ValidationError):
        cls(universidad="ULL", titulacion="Ingeniería", datos="")


def test_par_build_returns_nonempty():
    assert PromptAnalisisPar(**PAR_ARGS).build()


def test_par_build_contains_injected_values():
    prompt = PromptAnalisisPar(**PAR_ARGS).build()
    assert "ULL" in prompt
    assert "Ingeniería Informática" in prompt
    assert "dato: 75%" in prompt
    assert "Grupo A" in prompt
    assert "Tasa de Éxito" in prompt


def test_par_build_without_optional_fields():
    prompt = PromptAnalisisPar(**PAR_ARGS).build()
    assert "No se han definido umbrales de referencia." in prompt


def test_par_build_with_optional_fields():
    prompt = PromptAnalisisPar(**PAR_ARGS, objetivo=90.0, limite=70.0).build()
    assert "90.0%" in prompt
    assert "70.0%" in prompt


def test_par_empty_universidad_raises():
    with pytest.raises(ValidationError):
        PromptAnalisisPar(
            universidad="",
            titulacion="Ing",
            datos="d",
            contexto_grupo="A",
            tasa_nombre="TE",
        )


def test_par_empty_titulacion_raises():
    with pytest.raises(ValidationError):
        PromptAnalisisPar(
            universidad="ULL",
            titulacion="",
            datos="d",
            contexto_grupo="A",
            tasa_nombre="TE",
        )


def test_par_empty_datos_raises():
    with pytest.raises(ValidationError):
        PromptAnalisisPar(
            universidad="ULL",
            titulacion="Ing",
            datos="",
            contexto_grupo="A",
            tasa_nombre="TE",
        )
