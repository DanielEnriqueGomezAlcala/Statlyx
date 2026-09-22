"""
Generación del desglose de tasas por convocatoria
"""

import pandas as pd
import os
from typing import Any

# Charts
from charts.static.shared.line_chart import static_chart_lines
from charts.static.shared.table_chart import static_chart_table
from charts.static.call_breakdown.resume_chart import static_chart_bars_breakdown_resume

# utils
from utils.image import save_chart_image
from utils.logger import get_logger

# LLM
from functions.llm.llm import generate_text
from functions.llm.prompts.subject_analisis import (
    PromptResumenDesgloseConvocatoria,
    PromptAnalisisPar,
)

# constants
from constants import CURSOS, TASAS_CALL as TASAS, CONVOCATORIAS_ORDEN, GRUPOS

logger = get_logger(__name__)


def generate_call_breakdown(
    df: pd.DataFrame,
    directory: str,
    chart_types: list[str],
    institucion: str = "",
    titulacion: str = "",
    target_value=None,
    limit_value=None,
):
    """
    Genera las gráficos y texto de las tasas desglosando por curso, convocatoria y grupo.


    Args:
        df: DF con los datos de convocatorias, filtrado a grupos 1 y 2.
        directory: Directorio donde se guardarán las imágenes y texto de las gráficas.
        chart_types: gráficos seleccionados en el dashboard.
        institucion: nombre de la institución.
        titulacion: nombre de la titulación.
        target_value: valor de la tasa objetivo para las líneas de referencia.
        limit_value: valor de la tasa límite para las líneas de referencia.

    Returns:
        JSON con los gráficos y texto de las tasas desglosadas por curso, convocatoria y grupo.
    """
    breakdown_data: dict[str, Any] = {
        "resume_text": None,
        "breakdown": [],
    }

    line_chart = "graficas-lineas" in chart_types
    table_chart = "graficas-tablas" in chart_types

    for curso, df_curso in df.groupby("Curso", observed=True):  # Se agrupan los datos por curso
        curso_nombre = CURSOS.get(curso, str(curso))
        logger.info("Call breakdown — curso: %s", curso_nombre)
        course_data: dict[str, Any] = {"name": curso_nombre, "calls": []}

        for convocatoria in CONVOCATORIAS_ORDEN:  # Se agrupan los datos por convocatoria
            df_conv = df_curso[df_curso["Convocatoria"] == convocatoria]
            if df_conv.empty:
                continue

            conv_data: dict[str, Any] = {"name": convocatoria, "groups": []}

            for grupo, df_grupo in df_conv.groupby("Grupo", observed=True):  # Se agrupan los datos por grupo
                grupo_nombre = GRUPOS.get(grupo, str(grupo))
                grupo_data: dict[str, Any] = {"name": grupo_nombre, "rates": []}

                for (
                    rate_col,
                    rate_name,
                ) in TASAS.items():  # Se agrupan los datos por tasa
                    if rate_col not in df_grupo.columns:
                        continue

                    df_rate = df_grupo[["Asignatura", "Anio", rate_col]].dropna().copy()
                    df_rate = df_rate.sort_values("Anio")
                    if df_rate.empty:
                        continue

                    chart_name = (  # Nombre que se le pone al archivo con el gráfico
                        f"{curso_nombre}_{convocatoria}_{grupo}_{rate_col}".replace(" ", "_").replace("/", "-")
                    )
                    tasa_data: dict[str, Any] = {
                        "name": rate_name,
                        "text": None,
                    }  # Se crea el diccionario con el nombre de la tasa y el texto

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

                    pivot = (
                        df_rate.pivot_table(
                            index="Asignatura",
                            columns="Anio",
                            values=rate_col,
                            aggfunc="mean",
                        )
                        .round(1)
                        .fillna("")
                    )
                    pivot.columns = [str(c) for c in pivot.columns]
                    pivot.index.name = "Asignatura"
                    prompt = PromptAnalisisPar(  # Se genera el prompt para el análisis de la tasa
                        universidad=institucion,
                        titulacion=titulacion,
                        contexto_grupo=f"{curso_nombre} – {convocatoria} – {grupo}",
                        tasa_nombre=rate_name,
                        objetivo=target_value,
                        limite=limit_value,
                        datos=pivot.to_string(),
                    ).build()
                    tasa_data["text"] = generate_text(prompt)  # Se genera el texto de la tasa

                    grupo_data["rates"].append(tasa_data)

                if grupo_data["rates"]:  # Se agrega el grupo a la convocatoria
                    conv_data["groups"].append(grupo_data)

            if conv_data["groups"]:  # Se agrega la convocatoria a la lista de convocatorias
                course_data["calls"].append(conv_data)

        breakdown_data["breakdown"].append(course_data)  # Se agrega el curso a la lista de cursos

    # Generamos el resumen de las tasas de eficiencia y éxito por curso y convocatoria
    df_agrupado = df.groupby(["Curso", "Convocatoria"])[["Tasa_Eficiencia", "Tasa_Exito"]].mean().reset_index()

    prompt = PromptResumenDesgloseConvocatoria(  # Se genera el prompt para el análisis del resumen
        universidad=institucion,
        titulacion=titulacion,
        datos=df_agrupado.to_string(index=False),
    ).build()
    breakdown_data["resume_text"] = generate_text(prompt)  # Se genera el texto del resumen

    fig = static_chart_bars_breakdown_resume(  # Se genera el gráfico de barras del resumen
        df_agrupado, "Resumen de Medias por Curso y Convocatoria"
    )
    img_path = os.path.join(directory, "graf_resumen_medias_convocatoria.png")
    save_chart_image(fig, img_path, width=1200)
    breakdown_data["resume_chart_path"] = img_path

    return breakdown_data
