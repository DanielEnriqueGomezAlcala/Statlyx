from pptx import Presentation

from functions.write_presentation.slides import (
    section_slide, chart_slide,
)

def degree_section(presentacion: Presentation, degree_data: list):
    section_slide(presentacion, "Análisis por titulación")
    for tasa in degree_data:
        img_line = tasa.get('line_chart_path')
        img_table = tasa.get('table_chart_path')
        chart_slide(presentacion, tasa['name'], img_line, tasa.get('text'), img_table)