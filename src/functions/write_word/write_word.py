"""
Función para generar un informe Word a partir de los datos proporcionados.
"""

from docxtpl import DocxTemplate, InlineImage
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Mm
import os
import time
import pandas as pd
from datetime import datetime
from typing import Any

from utils.logger import get_logger
from functions.generate_information import (
    generate_call_breakdown,
    generate_degree_breakdown,
    generate_mention_breakdown,
    generate_subject_breakdown,
    generate_tipology_breakdown,
    generate_subject_conclusions,
)
from constants import CURSOS, ORDEN_CURSOS

logger = get_logger(__name__)


def enrich_with_inline(item: dict, tpl, width=Mm(150)):
    """
    Convierte las rutas de imágenes de un diccionario en objetos InlineImage para docxtpl.

    Args:
        item: Diccionario de datos que puede contener las claves line_chart_path,
            table_chart_path y resume_chart_path.
        tpl: Plantilla DocxTemplate a la que están vinculadas las imágenes.
        width: Anchura de las gráficas de línea y tabla. Por defecto Mm(150).
            Las gráficas de resumen usan siempre Mm(155).
    """
    if item.get("line_chart_path"):
        item["line_chart"] = InlineImage(tpl, item["line_chart_path"], width=width)
    if item.get("table_chart_path"):
        item["table_chart"] = InlineImage(tpl, item["table_chart_path"], width=width)
    if item.get("resume_chart_path"):
        item["resume_chart"] = InlineImage(
            tpl, item["resume_chart_path"], width=Mm(155)
        )


def compute_numbering(contexto: dict) -> dict:
    """
    Calcula los números y títulos de sección del documento Word.

    Args:
        contexto: Diccionario con las claves mostrar_analisis_titulacion,
            mostrar_analisis_asignatura y las claves de cada desglose.

    Returns:
        Diccionario con las claves de numeración
    """
    n: dict[str, int | str] = {}
    sec = 0

    if contexto.get("mostrar_analisis_titulacion"):
        sec += 1
        n["n_titulacion"] = sec
        n["titulo_titulacion"] = f"{sec}."

    if contexto.get("mostrar_analisis_asignatura"):
        sec += 1
        n["n_asignatura"] = sec
        n["titulo_asignatura"] = f"{sec}."

        sub = 0
        if contexto.get("mostrar_desglose_curso"):
            sub += 1
            n["n_desglose_curso"] = sub
            n["titulo_desglose_curso"] = f"{sec}.{sub}."

        if contexto.get("mostrar_desglose_tipologia"):
            sub += 1
            n["n_desglose_tipologia"] = sub
            n["titulo_desglose_tipologia"] = f"{sec}.{sub}."

        if contexto.get("mostrar_desglose_menciones"):
            sub += 1
            n["n_desglose_menciones"] = sub
            n["titulo_desglose_menciones"] = f"{sec}.{sub}."

        if contexto.get("mostrar_desglose_convocatoria"):
            sub += 1
            n["n_desglose_convocatoria"] = sub
            n["titulo_desglose_convocatoria"] = f"{sec}.{sub}."

    for key in (
        "n_titulacion",
        "n_asignatura",
        "n_desglose_curso",
        "n_desglose_tipologia",
        "n_desglose_menciones",
        "n_desglose_convocatoria",
        "titulo_titulacion",
        "titulo_asignatura",
        "titulo_desglose_curso",
        "titulo_desglose_tipologia",
        "titulo_desglose_menciones",
        "titulo_desglose_convocatoria",
    ):
        n.setdefault(key, "")

    return n


def write_word(
    df,
    df_t4,
    df_conv,
    ruta_plantilla: str,
    directorio: str,
    chart_selector: str,
    chart_types=None,
    institucion: str = "",
    titulacion: str = "",
    target_value=None,
    limit_value=None,
):
    """
    Genera el informe Word a partir de los datos filtrados y lo guarda en disco.

    Args:
        df: DF de asignaturas con los filtros ya aplicados.
        df_t4: DF de indicadores de titulación con los filtros ya aplicados.
        df_conv: DF de convocatorias con los filtros ya aplicados.
        ruta_plantilla: Ruta al archivo .docx de plantilla.
        directorio: Directorio donde se guardan las imágenes y el documento final.
        chart_selector: Lista de identificadores de sección a incluir
        chart_types: Lista de tipos de gráfica a generar.
        institucion: Nombre de la institución.
        titulacion: Nombre de la titulación.
        target_value: Valor de la tasa objetivo.
        limit_value: Valor de la tasa límite.

    Returns:
        Ruta absoluta del archivo .docx generado.
    """
    logger.info("Iniciando generación Word — secciones: %s", chart_selector)
    t0 = time.time()
    tpl = DocxTemplate(ruta_plantilla)  # Plantilla Word

    df["Curso"] = df["Curso"].map(CURSOS)
    df["Curso"] = pd.Categorical(df["Curso"], categories=ORDEN_CURSOS, ordered=True)
    df = df.sort_values("Curso").dropna(subset=["Curso"])

    anios = df["Anio"].dropna().str.extract(r"(\d{4})")[0].astype(int)
    rango_anios = f"{anios.min()} — {anios.max()}" if not anios.empty else ""

    tipologias = ", ".join(sorted(df["Tipologia"].dropna().unique()))

    cursos_presentes = [c for c in ORDEN_CURSOS if c in df["Curso"].values]
    cursos_str = ", ".join(cursos_presentes)

    course_data = {}
    if "desglose-curso" in chart_selector:  # Genera desglose por curso
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
        enrich_with_inline(course_data, tpl)
        for course in course_data.get("breakdown", []):
            for quarter in course.get("quarter", []):
                for rate in quarter.get("rates", []):
                    enrich_with_inline(rate, tpl)

    tipologies_data = {}
    if "desglose-tipologia" in chart_selector:  # Genera desglose por tipología
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
        enrich_with_inline(tipologies_data, tpl)
        for course in tipologies_data.get("breakdown", []):
            for tipologia in course.get("tipologies", []):
                for rate in tipologia.get("rates", []):
                    enrich_with_inline(rate, tpl)

    mentions_data = {}
    if "desglose-menciones" in chart_selector:  # Genera desglose por mención
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
        enrich_with_inline(mentions_data, tpl)
        for mention in mentions_data.get("breakdown", []):
            for rate in mention.get("rates", []):
                enrich_with_inline(rate, tpl)

    convocatoria_data = {}
    if "desglose-convocatoria" in chart_selector:  # Genera desglose por convocatoria
        logger.info("Generando desglose por convocatoria...")
        df_conv = df_conv[df_conv["Grupo"].isin([1, 2])]
        convocatoria_data = generate_call_breakdown(
            df_conv,
            directorio,
            chart_types,
            institucion,
            titulacion,
            target_value,
            limit_value,
        )
        enrich_with_inline(convocatoria_data, tpl)
        for course in convocatoria_data.get("breakdown", []):
            for call in course.get("calls", []):
                for group in call.get("groups", []):
                    for rate in group.get("rates", []):
                        enrich_with_inline(rate, tpl)

    degree_data: dict[str, Any] = {}
    if "analisis-titulacion" in chart_selector:  # Genera análisis por titulación
        logger.info("Generando análisis por titulación...")
        degree_data = generate_degree_breakdown(
            df_t4, directorio, chart_types, institucion, titulacion
        )
        for item in degree_data.get("tasas", []):
            enrich_with_inline(item, tpl, width=Mm(155))

    mostrar_asignatura = any(  # Indica si se muestra el análisis por asignatura
        v in chart_selector
        for v in [
            "desglose-curso",
            "desglose-tipologia",
            "desglose-menciones",
            "desglose-convocatoria",
        ]
    )

    subject_conclusions = {}
    if mostrar_asignatura:  # Genera conclusiones sobre las peores asignaturas
        logger.info("Generando conclusiones de asignaturas...")
        subject_conclusions = generate_subject_conclusions(df, institucion, titulacion)

    contexto = {  # Contexto de la plantilla Word
        # Datos de la institución
        "NombreInstitucion": institucion,
        "NombreTitulacion": titulacion,
        "FechaCreacion": datetime.now().strftime("%Y-%m-%d"),
        # Datos de los filtros
        "RangoAniosSeleccionado": rango_anios,
        "TiposAsignaturasSeleccionado": tipologias,
        "CursosSeleccionados": cursos_str,
        # Datos del análisis por asignatura
        "mostrar_analisis_asignatura": mostrar_asignatura,
        "mostrar_desglose_curso": "desglose-curso" in chart_selector,
        "mostrar_desglose_tipologia": "desglose-tipologia" in chart_selector,
        "mostrar_desglose_menciones": "desglose-menciones" in chart_selector,
        "mostrar_desglose_convocatoria": "desglose-convocatoria" in chart_selector,
        "course_data": course_data,
        "tipologies_data": tipologies_data,
        "mentions_data": mentions_data,
        "convocatoria_data": convocatoria_data,
        "subject_conclusions": subject_conclusions,
        # Datos del análisis por titulación
        "mostrar_analisis_titulacion": "analisis-titulacion" in chart_selector,
        "degree_data": degree_data,
    }

    contexto.update(
        compute_numbering(contexto)
    )  # Añade los números y títulos de sección

    tpl.render(contexto)  # Renderiza la plantilla Word

    # Esto es para que al abrir el documento se pida actualizar los campos
    updatefields = OxmlElement("w:updateFields")
    updatefields.set(qn("w:val"), "true")
    tpl.docx.settings.element.append(updatefields)

    ruta_guardado = os.path.join(
        directorio,
        f"{institucion}_{titulacion}_{datetime.now().strftime('%Y%m%d')}.docx",
    )
    tpl.save(ruta_guardado)
    logger.info(
        "Word guardado en %.1fs: %s", time.time() - t0, os.path.basename(ruta_guardado)
    )

    return ruta_guardado
