from pptx import Presentation

from functions.write_presentation.slides import (
    section_slide, resume_slide, chart_slide,
)

def call_section(presentacion: Presentation, convocatoria_data: dict):
    section_slide(presentacion, "Análisis por asignatura", "Desglose por convocatoria")
    resume_slide(
        presentacion, "Resumen por convocatoria",
        convocatoria_data.get('resume_chart_path'),
        convocatoria_data.get('resume_text'),
    )
    for course in convocatoria_data.get('breakdown', []):
        for call in course.get('calls', []):
            for group in call.get('groups', []):
                for tasa in group.get('rates', []):
                    title = f"{course['name']} — {call['name']} — {group['name']} — {tasa['name']}"
                    img_line = tasa.get('line_chart_path')
                    img_table = tasa.get('table_chart_path')
                    chart_slide(presentacion, title, img_line, tasa.get('text'), img_table)