"""
Generación del desglose de tasas por mención
"""

import pandas as pd
import os
from typing import Any

# Charts
from charts.static.shared.line_chart import static_chart_lines
from charts.static.shared.table_chart import static_chart_table
from charts.static.mention_breakdown.resume_chart import (
    static_chart_bars_breakdown_resume,
)

# Utils
from utils.image import save_chart_image
from utils.logger import get_logger

# LLM
from functions.llm.llm import generate_text
from functions.llm.prompts.subject_analisis import (
    PromptResumenDesgloseMencion,
    PromptAnalisisPar,
)

# Constants
from constants import TASAS_SUBJECT as TASAS

logger = get_logger(__name__)


def generate_mention_breakdown(
    df: pd.DataFrame,
    directory: str,
    chart_types: list[str],
    institucion: str = "",
    titulacion: str = "",
    target_value=None,
    limit_value=None,
):
    """
    Genera las gráficos y texto de las tasas desglosando por mención.

    Args:
        df: DF con los datos de las asignaturas, filtrado para excluir las filas con mención "No aplica".
        directory: Directorio donde se guardarán las imágenes y texto de las gráficas.
        chart_types: gráficos seleccionados en el dashboard.
        institucion: nombre de la institución.
        titulacion: nombre de la titulación.
        target_value: valor de la tasa objetivo para las líneas de referencia.
        limit_value: valor de la tasa límite para las líneas de referencia.

    Returns:
        JSON con los gráficos y texto de las tasas desglosadas por mención.
    """
    breakdown_data: dict[str, Any] = {
        "resume_text": None,
        "breakdown": [],
    }

    line_chart = "graficas-lineas" in chart_types
    table_chart = "graficas-tablas" in chart_types

    for mention, df_mention in df.groupby("Mencion", observed=True):  # Se agrupan los datos por mención
        logger.info("Mention breakdown — mención: %s", mention)
        mention_data: dict[str, Any] = {"name": mention, "rates": []}

        for rate_col, rate_name in TASAS.items():  # Se agrupan los datos por tasa
            if rate_col not in df_mention.columns:
                continue

            df_rate = df_mention[["Asignatura", "Anio", rate_col]].dropna().copy()
            df_rate = df_rate.sort_values("Anio")
            if df_rate.empty:
                continue

            chart_name = f"{mention}_{rate_col}".replace(" ", "_").replace("/", "-")  # Nombre que se le pone al archivo con el gráfico
            tasa_data: dict[str, Any] = {"name": rate_name, "text": None}

            if line_chart:  # Se genera el gráfico de líneas
                fig = static_chart_lines(
                    df_rate,
                    rate_col,
                    target_value=target_value,
                    limit_value=limit_value,
                )
                img_path = os.path.join(directory, f"graf_{chart_name}_line.png")
                save_chart_image(fig, img_path, border=6)
                tasa_data["line_chart_path"] = img_path

            if table_chart:  # Se genera el gráfico de tabla
                fig = static_chart_table(df_rate, rate_col)
                img_path = os.path.join(directory, f"graf_{chart_name}_table.png")
                save_chart_image(fig, img_path)
                tasa_data["table_chart_path"] = img_path

            pivot = df_rate.pivot_table(index="Asignatura", columns="Anio", values=rate_col, aggfunc="mean").round(1).fillna("")
            pivot.columns = [str(c) for c in pivot.columns]
            pivot.index.name = "Asignatura"
            prompt = PromptAnalisisPar(  # Se genera el prompt para el análisis de la tasa
                universidad=institucion,
                titulacion=titulacion,
                contexto_grupo=f"Mención: {mention}",
                tasa_nombre=TASAS[rate_col],
                objetivo=target_value,
                limite=limit_value,
                datos=pivot.to_string(),
            ).build()
            tasa_data["text"] = generate_text(prompt)  # Se genera el texto de la tasa

            mention_data["rates"].append(tasa_data)  # Se agrega la tasa a la mención

        breakdown_data["breakdown"].append(mention_data)  # Se agrega la mención a la lista de menciones

    # Se genera el resumen de las tasas de éxito y rendimiento por mención
    df_agrupado = df[["Mencion", "Tasa_Exito", "Tasa_Rendimiento"]].groupby("Mencion")[["Tasa_Exito", "Tasa_Rendimiento"]].mean().reset_index()

    prompt = PromptResumenDesgloseMencion(  # Se genera el prompt para el análisis del resumen
        universidad=institucion,
        titulacion=titulacion,
        datos=df_agrupado.to_string(index=False),
    ).build()
    breakdown_data["resume_text"] = generate_text(prompt)  # Se genera el texto del resumen

    fig = static_chart_bars_breakdown_resume(  # Se genera el gráfico de barras del resumen
        df_agrupado, "Resumen de Medias por Mención"
    )
    img_path = os.path.join(directory, "graf_resumen_medias_mencion.png")
    save_chart_image(fig, img_path, width=1200)
    breakdown_data["resume_chart_path"] = img_path

    return breakdown_data
