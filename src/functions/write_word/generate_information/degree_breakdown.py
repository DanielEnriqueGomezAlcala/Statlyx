import pandas as pd
import os
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm

# LLM
from functions.llm.llm import generate_text
from functions.llm.prompts import plantilla_resumen_titulacion_tasa

# Charts
from charts.static.line_chart import static_chart_lines

TASAS = {
    'Tasa_Exito':       'Tasa de Éxito',
    'Tasa_Rendimiento': 'Tasa de Rendimiento',
    'Tasa_Eficiencia':  'Tasa de Eficiencia',
    'Tasa_Graduacion':  'Tasa de Graduación',
    'Tasa_Abandono':    'Tasa de Abandono',
}


def generate_degree_breakdown(df: pd.DataFrame, directory: str, tpl: DocxTemplate, institucion: str = "", titulacion: str = ""):
    degree_breakdown = []

    df = df.sort_values('Anio')

    for col, nombre in TASAS.items():
        if col not in df.columns:
            continue

        df_chart = df[['Anio', col]].dropna().copy()
        df_chart = df_chart.rename(columns={col: 'Valor'})
        df_chart['Asignatura'] = nombre

        fig = static_chart_lines(df_chart, nombre, 'Valor')
        chart_name = f"titulacion_{col}"
        img_path = os.path.join(directory, f"graf_{chart_name}.png")
        fig.write_image(img_path, width=1200, height=700, scale=2)
        chart = InlineImage(tpl, img_path, width=Mm(160))

        datos = df_chart[['Anio', 'Valor']].round(2).to_string(index=False)
        prompt = plantilla_resumen_titulacion_tasa.substitute(
            universidad=institucion,
            titulacion=titulacion,
            tasa=nombre,
            datos=datos
        )

        degree_breakdown.append({
            'name': nombre,
            'chart': chart,
            'text': generate_text(prompt)
        })

    return degree_breakdown
