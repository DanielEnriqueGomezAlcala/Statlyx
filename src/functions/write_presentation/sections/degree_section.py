"""
Sección de análisis por indicadores a nivel de titulación
"""

from pptx import Presentation

from functions.write_presentation.slides import (
    section_slide,
    chart_slide,
    conclusions_slide,
)


def degree_section(presentacion: Presentation, degree_data: dict):
    """
    Genera la sección de análisis por titulación.

    Args:
        presentacion: Plantilla de PowerPoint.
        degree_data: Datos de la titulación.
    """
    section_slide(presentacion, "Análisis por titulación")
    for tasa in degree_data.get("tasas", []):
        img_line = tasa.get("line_chart_path")
        img_table = tasa.get("table_chart_path")
        chart_slide(presentacion, tasa["name"], img_line, tasa.get("text"), img_table)
    conclusions_slide(
        presentacion,
        "Resumen y recomendaciones",
        conclusion=degree_data.get("resume_conclusion"),
        bullets=degree_data.get("resume_bullets"),
    )
