import pandas as pd
import os

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


def generate_degree_breakdown(
    df: pd.DataFrame,
    directory: str,
    chart_types: list[str],
    institucion: str = "",
    titulacion: str = "",
):
    """Genera el análisis de los indicadores de titulación.

    Args:
        df: DF con los indicadores de titulación por año.
        directory: Directorio donde se guardarán las imágenes y texto de las gráficas.
        chart_types: gráficos seleccionados en el dashboard.
        institucion: nombre de la institución.
        titulacion: nombre de la titulación.

    Returns:
        Array con los gráficos y texto de los indicadores a nivel de titulación.
    """
    degree_breakdown = []

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
            fig = static_chart_lines(df_chart, "Valor")
            img_path = os.path.join(directory, f"graf_{chart_name}_line.png")
            save_chart_image(fig, img_path, border=6)
            tasa_data["line_chart_path"] = img_path

        if table_chart:
            fig = static_chart_table(df_chart, "Valor")
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

        degree_breakdown.append(tasa_data)

    return degree_breakdown
