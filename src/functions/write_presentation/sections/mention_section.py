from pptx import Presentation

from functions.write_presentation.slides import (
    section_slide, resume_slide, chart_slide,
)

def mention_section(presentacion: Presentation, mentions_data: dict):
    section_slide(presentacion, "Análisis por asignatura", "Desglose por menciones/itinerarios")
    resume_slide(
        presentacion, "Resumen por mención",
        mentions_data.get('resume_chart_path'),
        mentions_data.get('resume_text'),
    )
    for mention in mentions_data.get('breakdown', []):
        for tasa in mention.get('rates', []):
            title = f"{mention['name']} — {tasa['name']}"
            img_line = tasa.get('line_chart_path')
            img_table = tasa.get('table_chart_path')
            chart_slide(presentacion, title, img_line, tasa.get('text'), img_table)