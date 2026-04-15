"""
Función para generar una presentación PowerPoint a partir de los datos proporcionados.
"""

import os
import time
import pandas as pd
from datetime import datetime

from pptx import Presentation
from utils.logger import get_logger

from functions.generate_information import (
    generate_call_breakdown,
    generate_degree_breakdown,
    generate_mention_breakdown,
    generate_subject_breakdown,
    generate_tipology_breakdown,
    generate_subject_conclusions,
)
from functions.write_presentation.constants import (
    ENUM_CURSOS,
    ORDEN_CURSOS,
    SLIDE_W,
    SLIDE_H,
)
from functions.write_presentation.sections import (
    call_section,
    degree_section,
    mention_section,
    subject_section,
    typology_section,
)
from functions.write_presentation.slides import (
    info_slide,
    title_slide,
    conclusions_slide,
)

logger = get_logger(__name__)


def write_presentation(
    df,
    df_t4,
    df_conv,
    ruta_plantilla: str,
    directorio: str,
    chart_selector: list,
    chart_types=None,
    institucion: str = "",
    titulacion: str = "",
    target_value=None,
    limit_value=None,
) -> str:
    """
    Genera una presentación PowerPoint a partir de los DataFrames proporcionados.

    Args:
        df: DF con datos de asignaturas.
        df_t4: DF con datos de indicadores de titulación.
        df_conv: DF con datos de convocatorias.
        ruta_plantilla: Ruta absoluta al archivo .pptx de plantilla.
        directorio: Directorio donde se guardará la presentación generada.
        chart_selector: Lista de identificadores de sección a incluir.
        chart_types: Tipos de gráfica a generar para cada sección.
        institucion: Nombre de la institución.
        titulacion: Nombre de la titulación.
        target_value: Valor de la tasa objetivo para las líneas de referencia.
        limit_value: Valor de la tasa límite para las líneas de referencia.

    Returns:
        Ruta absoluta al archivo .pptx generado.
    """

    logger.info("Iniciando generación PPTX — secciones: %s", chart_selector)
    t0 = time.time()
    df["Curso"] = df["Curso"].map(ENUM_CURSOS)
    df["Curso"] = pd.Categorical(df["Curso"], categories=ORDEN_CURSOS, ordered=True)
    df = df.sort_values("Curso").dropna(subset=["Curso"])

    anios = df["Anio"].dropna().str.extract(r"(\d{4})")[0].astype(int)
    rango_anios = f"{anios.min()} — {anios.max()}" if not anios.empty else ""
    tipologias = ", ".join(sorted(df["Tipologia"].dropna().unique()))
    cursos_presentes = [c for c in ORDEN_CURSOS if c in df["Curso"].values]
    cursos_str = ", ".join(cursos_presentes)

    course_data = {}
    if "desglose-curso" in chart_selector:
        logger.info("Generando desglose por curso...")
        course_data = generate_subject_breakdown(
            df,
            directorio,
            chart_types,
            institucion,
            titulacion,
            target_value,
            limit_value,
        )

    tipologies_data = {}
    if "desglose-tipologia" in chart_selector:
        logger.info("Generando desglose por tipología...")
        tipologies_data = generate_tipology_breakdown(
            df,
            directorio,
            chart_types,
            institucion,
            titulacion,
            target_value,
            limit_value,
        )

    mentions_data = {}
    if "desglose-menciones" in chart_selector:
        logger.info("Generando desglose por mención...")
        df_mentions = df[df["Mencion"] != "No aplica"]
        mentions_data = generate_mention_breakdown(
            df_mentions,
            directorio,
            chart_types,
            institucion,
            titulacion,
            target_value,
            limit_value,
        )

    convocatoria_data = {}
    if "desglose-convocatoria" in chart_selector:
        logger.info("Generando desglose por convocatoria...")
        df_conv_filtered = df_conv[df_conv["Grupo"].isin([1, 2])]
        convocatoria_data = generate_call_breakdown(
            df_conv_filtered,
            directorio,
            chart_types,
            institucion,
            titulacion,
            target_value,
            limit_value,
        )

    degree_data = {}
    if "analisis-titulacion" in chart_selector:
        logger.info("Generando análisis por titulación...")
        degree_data = generate_degree_breakdown(
            df_t4, directorio, chart_types, institucion, titulacion
        )

    prs = Presentation(ruta_plantilla)
    prs.slide_width = SLIDE_W
    prs.slide_height = SLIDE_H

    fecha = datetime.now().strftime("%d/%m/%Y")
    title_slide(prs, institucion, titulacion, fecha)
    info_slide(prs, rango_anios, tipologias, cursos_str)

    if degree_data.get("tasas"):
        degree_section(prs, degree_data)

    mostrar_asignatura = any(
        v in chart_selector
        for v in [
            "desglose-curso",
            "desglose-tipologia",
            "desglose-menciones",
            "desglose-convocatoria",
        ]
    )

    subject_conclusions = {}
    if mostrar_asignatura:
        logger.info("Generando conclusiones de asignaturas...")
        subject_conclusions = generate_subject_conclusions(df, institucion, titulacion)

    if course_data:
        subject_section(prs, course_data)

    if tipologies_data:
        typology_section(prs, tipologies_data)

    if mentions_data:
        mention_section(prs, mentions_data)

    if convocatoria_data:
        call_section(prs, convocatoria_data)

    if subject_conclusions.get("conclusion_text") or subject_conclusions.get(
        "recommendations_bullets"
    ):
        conclusions_slide(
            prs,
            "Conclusiones y recomendaciones por asignatura",
            conclusion=subject_conclusions.get("conclusion_text"),
            bullets=subject_conclusions.get("recommendations_bullets"),
        )

    ruta_guardado = os.path.join(
        directorio,
        f"{institucion}_{titulacion}_{datetime.now().strftime('%Y%m%d')}.pptx",
    )
    prs.save(ruta_guardado)
    logger.info(
        "PPTX guardado en %.1fs: %s", time.time() - t0, os.path.basename(ruta_guardado)
    )
    return ruta_guardado
