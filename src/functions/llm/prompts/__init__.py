
from .base import BasePrompt
from .degree_analisis import (
    PromptTasaExito,
    PromptTasaRendimiento,
    PromptTasaAbandono,
    PromptTasaGraduacion,
    PromptTasaEficiencia,
)

from .subject_analisis import (
    PromptResumenDesgloseCurso,
    PromptResumenDesgloseTipologia,
    PromptResumenDesgloseMencion,
)

__all__ = [
    "BasePrompt",
    "PromptTasaExito",
    "PromptTasaRendimiento",
    "PromptTasaAbandono",
    "PromptTasaGraduacion",
    "PromptTasaEficiencia",
    "PromptResumenDesgloseCurso",
    "PromptResumenDesgloseTipologia",
    "PromptResumenDesgloseMencion",
]
