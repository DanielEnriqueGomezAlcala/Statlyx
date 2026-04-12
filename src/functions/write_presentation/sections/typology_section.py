from pptx import Presentation

from functions.write_presentation.slides import (
    section_slide,
    resume_slide,
    chart_slide,
)


def typology_section(presentacion: Presentation, tipologies_data: dict):
    """
    Genera la sección de análisis por tipología.

    Args:
        presentacion: Plantilla de PowerPoint.
        tipologies_data: Datos de la tipología.
    """
    section_slide(presentacion, "Análisis por asignatura", "Desglose por tipología")
    resume_slide(
        presentacion,
        "Resumen por tipología",
        tipologies_data.get("resume_chart_path"),
        tipologies_data.get("resume_text"),
    )
    for course in tipologies_data.get("breakdown", []):
        for tipologia in course.get("tipologies", []):
            for tasa in tipologia.get("rates", []):
                title = f"{course['name']} — {tipologia['name']} — {tasa['name']}"
                img_line = tasa.get("line_chart_path")
                img_table = tasa.get("table_chart_path")
                chart_slide(presentacion, title, img_line, tasa.get("text"), img_table)
