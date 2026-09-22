"""
Sección de análisis por asignatura con desglose por curso y cuatrimestre
"""

from pptx import Presentation

from functions.write_presentation.slides import (
    section_slide,
    resume_slide,
    chart_slide,
)


def subject_section(presentacion: Presentation, course_data: dict):
    """
    Genera la sección de análisis por asignatura.

    Args:
        presentacion: Plantilla de PowerPoint.
        course_data: Datos de la asignatura.
    """
    section_slide(presentacion, "Análisis por asignatura", "Desglose por curso-cuatrimestre")
    resume_slide(
        presentacion,
        "Resumen por curso y cuatrimestre",
        course_data.get("resume_chart_path"),
        course_data.get("resume_text"),
    )
    for course in course_data.get("breakdown", []):
        for quarter in course.get("quarter", []):
            for tasa in quarter.get("rates", []):
                title = f"{course['name']} — {quarter['name']} — {tasa['name']}"
                img_line = tasa.get("line_chart_path")
                img_table = tasa.get("table_chart_path")
                chart_slide(presentacion, title, img_line, tasa.get("text"), img_table)
