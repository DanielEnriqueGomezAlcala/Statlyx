import pytest
from pydantic import ValidationError

from functions.llm.prompts.base import BasePrompt


def test_empty_universidad_raises():
    with pytest.raises(ValidationError):
        BasePrompt(universidad="", titulacion="Ingeniería", datos="datos")


def test_empty_titulacion_raises():
    with pytest.raises(ValidationError):
        BasePrompt(universidad="ULL", titulacion="", datos="datos")


def test_empty_datos_raises():
    with pytest.raises(ValidationError):
        BasePrompt(universidad="ULL", titulacion="Ingeniería", datos="")


def test_whitespace_only_field_raises():
    with pytest.raises(ValidationError):
        BasePrompt(universidad="   ", titulacion="Ingeniería", datos="datos")


def test_build_raises_not_implemented():
    prompt = BasePrompt(universidad="ULL", titulacion="Ingeniería", datos="datos")
    with pytest.raises(NotImplementedError):
        prompt.build()
