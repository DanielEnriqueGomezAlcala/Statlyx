import pandas as pd
import os
from typing import Any

# Charts
from charts.static.shared.line_chart import static_chart_lines
from charts.static.shared.table_chart import static_chart_table
from charts.static.tipology_breakdown.resume_chart import (
    static_chart_bars_breakdown_resume,
)

# Utils
from utils.image import save_chart_image
from utils.logger import get_logger

# LLM
from functions.llm.llm import generate_text
from functions.llm.prompts.subject_analisis import (
    PromptResumenDesgloseTipologia,
    PromptAnalisisPar,
)

# Constants
from constants import CURSOS, TASAS_SUBJECT as TASAS, TIPOLOGIAS

logger = get_logger(__name__)


def generate_tipology_breakdown(
    df: pd.DataFrame,
    directory: str,
    chart_types: list[str],
    institucion: str = "",
    titulacion: str = "",
    target_value=None,
    limit_value=None,
):
    """Genera el análisis desglosado por tipología de asignatura.

    Produce gráficas de líneas y/o tabla para cada tasa académica agrupada por
    curso y tipología, junto con un texto analítico generado por IA y una gráfica
    de resumen global.

    Args:
        df: DataFrame con los datos de las asignaturas.
        directory: Directorio donde se guardarán las imágenes de las gráficas.
        chart_types: Lista de tipos de gráfica a generar. Valores posibles:
            ``"graficas-lineas"`` y ``"graficas-tablas"``.
        institucion: Nombre de la institución para los prompts de IA.
        titulacion: Nombre de la titulación para los prompts de IA.
        target_value: Valor de la tasa objetivo para las líneas de referencia.
        limit_value: Valor de la tasa límite para las líneas de referencia.

    Returns:
        Diccionario con claves ``resume_chart_path``, ``resume_text`` y ``breakdown``
        (lista de cursos con tipologías y tasas anidadas).
    """
    breakdown_data: dict[str, Any] = {
        "resume_text": None,
        "breakdown": [],
    }

    line_chart = "graficas-lineas" in chart_types
    table_chart = "graficas-tablas" in chart_types

    for curso, df_curso in df.groupby("Curso", observed=True):
        curso_nombre = CURSOS.get(curso, str(curso))
        logger.info("Tipology breakdown — curso: %s", curso_nombre)
        course_data: dict[str, Any] = {"name": curso_nombre, "tipologies": []}

        for tipologia, df_tipologia in df_curso.groupby("Tipologia", observed=True):
            tipologia_nombre = TIPOLOGIAS.get(tipologia, str(tipologia))
            tipologia_data: dict[str, Any] = {"name": tipologia_nombre, "rates": []}

            for rate_col, rate_name in TASAS.items():
                if rate_col not in df_tipologia.columns:
                    continue

                df_rate = df_tipologia[["Asignatura", "Anio", rate_col]].dropna().copy()
                df_rate = df_rate.sort_values("Anio")
                if df_rate.empty:
                    continue

                chart_name = f"{curso_nombre}_{tipologia}_{rate_col}".replace(
                    " ", "_"
                ).replace("/", "-")
                tasa_data: dict[str, Any] = {"name": rate_name, "text": None}

                if line_chart:
                    fig = static_chart_lines(
                        df_rate,
                        rate_col,
                        target_value=target_value,
                        limit_value=limit_value,
                    )
                    img_path = os.path.join(directory, f"graf_{chart_name}_line.png")
                    save_chart_image(fig, img_path, border=6)
                    tasa_data["line_chart_path"] = img_path

                if table_chart:
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
                prompt = PromptAnalisisPar(
                    universidad=institucion,
                    titulacion=titulacion,
                    contexto_grupo=f"{curso_nombre} – {tipologia_nombre}",
                    tasa_nombre=TASAS[rate_col],
                    objetivo=target_value,
                    limite=limit_value,
                    datos=pivot.to_string(),
                ).build()
                tasa_data["text"] = generate_text(prompt)

                tipologia_data["rates"].append(tasa_data)

            course_data["tipologies"].append(tipologia_data)

        breakdown_data["breakdown"].append(course_data)

    # Resume
    df_agrupado = (
        df[["Tipologia", "Tasa_Exito", "Tasa_Rendimiento"]]
        .groupby("Tipologia")[["Tasa_Exito", "Tasa_Rendimiento"]]
        .mean()
        .reset_index()
    )

    prompt = PromptResumenDesgloseTipologia(
        universidad=institucion,
        titulacion=titulacion,
        datos=df_agrupado.to_string(index=False),
    ).build()
    breakdown_data["resume_text"] = generate_text(prompt)

    fig = static_chart_bars_breakdown_resume(
        df_agrupado, "Resumen de Medias por Tipología"
    )
    img_path = os.path.join(directory, "graf_resumen_medias_tipologia.png")
    save_chart_image(fig, img_path, width=1200)
    breakdown_data["resume_chart_path"] = img_path

    return breakdown_data
