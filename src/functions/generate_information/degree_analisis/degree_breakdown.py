"""
Generación del análisis de indicadores a nivel de titulación
"""

import json
import pandas as pd
import os
from typing import Any

# utils
from utils.logger import get_logger

# LLM
from functions.llm.llm import generate_text

from functions.llm.prompts.degree_analisis import (
    PromptTasaExito,
    PromptTasaRendimiento,
    PromptTasaAbandono,
    PromptTasaGraduacion,
    PromptTasaEficiencia,
    PromptResumenDesgloseTitulacion,
)

# Charts
from charts.static.degree_breakdown.line_chart import static_chart_lines
from charts.static.degree_breakdown.table_chart import static_chart_table

# utils
from utils.image import save_chart_image

# constants
from constants import TASAS_DEGREE as TASAS

logger = get_logger(__name__)

PROMPT_CLASSES = {
    "Tasa_Exito": PromptTasaExito,
    "Tasa_Rendimiento": PromptTasaRendimiento,
    "Tasa_Eficiencia": PromptTasaEficiencia,
    "Tasa_Graduacion": PromptTasaGraduacion,
    "Tasa_Abandono": PromptTasaAbandono,
}

LOWER_IS_BETTER = {"Tasa_Abandono"}


def generate_degree_breakdown(
    df: pd.DataFrame,
    directory: str,
    chart_types: list[str],
    institucion: str = "",
    titulacion: str = "",
    target_graduacion=None,
    target_abandono=None,
    target_eficiencia=None,
):
    """Genera el análisis de los indicadores de titulación.

    Args:
        df: DF con los indicadores de titulación por año.
        directory: Directorio donde se guardarán las imágenes y texto de las gráficas.
        chart_types: gráficos seleccionados en el dashboard.
        institucion: nombre de la institución.
        titulacion: nombre de la titulación.
        target_graduacion: Valor objetivo para Tasa de Graduación.
        target_abandono: Valor objetivo para Tasa de Abandono.
        target_eficiencia: Valor objetivo para Tasa de Eficiencia.

    Returns:
        Array con los gráficos y texto de los indicadores a nivel de titulación.
    """
    target_por_tasa = {
        "Tasa_Graduacion": target_graduacion,
        "Tasa_Abandono": target_abandono,
        "Tasa_Eficiencia": target_eficiencia,
    }
    degree_breakdown: dict[str, Any] = {
        "resume_conclusion": None,
        "resume_bullets": [],
        "tasas": [],
    }

    line_chart = "graficas-lineas" in chart_types
    table_chart = "graficas-tablas" in chart_types

    df = df.sort_values("Anio")

    for col, nombre in TASAS.items():
        if col not in df.columns:
            continue
        logger.info("Degree breakdown — tasa: %s", nombre)

        df_chart = df[["Anio", col]].dropna().copy()
        df_chart = df_chart.rename(columns={col: "Valor"})
        df_chart["Asignatura"] = nombre

        tasa_data = {
            "name": nombre,
            "text": None,
        }
        chart_name = f"titulacion_{col}"

        if line_chart:
            fig = static_chart_lines(df_chart, "Valor", target_por_tasa.get(col))
            img_path = os.path.join(directory, f"graf_{chart_name}_line.png")
            save_chart_image(fig, img_path, border=6)
            tasa_data["line_chart_path"] = img_path

        if table_chart:
            fig = static_chart_table(
                df_chart, "Valor", lower_is_better=col in LOWER_IS_BETTER
            )
            img_path = os.path.join(directory, f"graf_{chart_name}_table.png")
            save_chart_image(fig, img_path)
            tasa_data["table_chart_path"] = img_path

        datos = df_chart[["Anio", "Valor"]].round(2).to_string(index=False)
        prompt = PROMPT_CLASSES[col](
            universidad=institucion,
            titulacion=titulacion,
            datos=datos,
        ).build()
        tasa_data["text"] = generate_text(prompt)

        degree_breakdown["tasas"].append(tasa_data)

    available_cols = ["Anio"] + [c for c in TASAS.keys() if c in df.columns]
    df_resumen = df[available_cols].sort_values("Anio").round(2)
    datos_resumen = df_resumen.to_string(index=False)

    logger.info("Degree breakdown — generando resumen global")
    prompt = PromptResumenDesgloseTitulacion(
        universidad=institucion,
        titulacion=titulacion,
        datos=datos_resumen,
    ).build()
    raw = generate_text(prompt)
    try:
        parsed = json.loads(raw)
        degree_breakdown["resume_conclusion"] = parsed.get("conclusion", "")
        degree_breakdown["resume_bullets"] = parsed.get("recomendaciones", [])
    except (json.JSONDecodeError, AttributeError):
        logger.warning(
            "Degree breakdown — respuesta del LLM no es JSON válido; guardando texto en bruto"
        )
        degree_breakdown["resume_conclusion"] = (
            "ERROR: La respuesta del modelo no es un JSON válido."
        )
        degree_breakdown["resume_bullets"] = []

    return degree_breakdown
