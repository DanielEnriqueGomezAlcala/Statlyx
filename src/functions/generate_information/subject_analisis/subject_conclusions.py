"""
Generación de conclusiones y recomendaciones a nivel de asignatura.
"""

import json
import pandas as pd

# LLM
from functions.llm.llm import generate_text
from functions.llm.prompts.subject_analisis import PromptPeoresAsignaturas

# utils
from utils.logger import get_logger

logger = get_logger(__name__)


def generate_subject_conclusions(
    df: pd.DataFrame,
    institucion: str = "",
    titulacion: str = "",
) -> dict:
    """
    Genera conclusiones y recomendaciones sobre las asignaturas con peores tasas.

    Args:
        df: DF con las asignaturas y sus tasas.
        institucion: nombre de la institución.
        titulacion: nombre de la titulación.
    """
    cols = [
        c for c in ["Asignatura", "Tasa_Exito", "Tasa_Rendimiento"] if c in df.columns
    ]
    df_filtered = df[cols].copy()

    # Filtramos asignaturas sin datos de éxito o con tasa de éxito 0, ya que muy probablemente correspondan a asignaturas que no existen ahora
    df_filtered = df_filtered[df_filtered["Tasa_Exito"] > 0].dropna(
        subset=["Tasa_Exito"]
    )

    if df_filtered.empty:
        logger.warning("Subject conclusions — no hay datos válidos tras filtrar ceros")
        return {"conclusion_text": None, "recommendations_bullets": []}

    agg_cols = [
        c for c in ["Tasa_Exito", "Tasa_Rendimiento"] if c in df_filtered.columns
    ]
    df_mean = (
        df_filtered.groupby("Asignatura")[agg_cols]
        .mean()
        .round(2)
        .sort_values("Tasa_Exito")
    )

    df_worst = df_mean.head(5)

    datos = df_worst.to_string()
    prompt = PromptPeoresAsignaturas(
        universidad=institucion,
        titulacion=titulacion,
        datos=datos,
    ).build()

    raw = generate_text(prompt)
    try:
        parsed = json.loads(raw)
        conclusion_text = parsed.get("conclusion", "")
        recommendations_bullets = parsed.get("recomendaciones", [])
    except (json.JSONDecodeError, AttributeError):
        logger.warning(
            "Subject conclusions — respuesta del LLM no es JSON válido; guardando texto en bruto"
        )
        conclusion_text = "ERROR: La respuesta del modelo no es un JSON válido."
        recommendations_bullets = []

    return {
        "conclusion_text": conclusion_text,
        "recommendations_bullets": recommendations_bullets,
    }
