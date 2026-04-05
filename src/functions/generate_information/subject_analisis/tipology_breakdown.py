import pandas as pd
import os
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm

# Charts
from charts.static.shared.line_chart import static_chart_lines
from charts.static.shared.table_chart import static_chart_table
from charts.static.tipology_breakdown.resume_chart import static_chart_bars_breakdown_resume

# Utils
from utils.image import save_chart_image

# LLM
from functions.llm.llm import generate_text
from functions.llm.prompts.subject_analisis import PromptResumenDesgloseTipologia, PromptAnalisisPar

# Constants
from constants import CURSOS, TASAS_SUBJECT as TASAS, TIPOLOGIAS


def generate_tipology_breakdown(df: pd.DataFrame, directory: str, tpl: DocxTemplate, chart_types: list[str], institucion: str = "", titulacion: str = "", target_value=None, limit_value=None):
    breakdown_data = {
        'resume_chart': None,
        'resume_text': None,
        'breakdown': [],
    }

    line_chart  = "graficas-lineas" in chart_types
    table_chart = "graficas-tablas" in chart_types

    for curso, df_curso in df.groupby('Curso', observed=True):
        curso_nombre = CURSOS.get(curso, str(curso))
        course_data = {'name': curso_nombre, 'tipologies': []}

        for tipologia, df_tipologia in df_curso.groupby('Tipologia', observed=True):
            tipologia_nombre = TIPOLOGIAS.get(tipologia, str(tipologia))
            tipologia_data = {'name': tipologia_nombre, 'rates': []}

            for rate_col, rate_name in TASAS.items():
                if rate_col not in df_tipologia.columns:
                    continue

                df_rate = df_tipologia[['Asignatura', 'Anio', rate_col]].dropna().copy()
                df_rate = df_rate.sort_values('Anio')
                if df_rate.empty:
                    continue

                chart_name = f"{curso_nombre}_{tipologia}_{rate_col}".replace(" ", "_").replace("/", "-")
                tasa_data = {'name': rate_name, 'line_chart': None, 'table_chart': None, 'text': None}

                if line_chart:
                    fig = static_chart_lines(df_rate, rate_col, target_value=target_value, limit_value=limit_value)
                    img_path = os.path.join(directory, f"graf_{chart_name}_line.png")
                    save_chart_image(fig, img_path, border=6)
                    tasa_data['line_chart_path'] = img_path
                    tasa_data['line_chart'] = InlineImage(tpl, img_path, width=Mm(150))

                if table_chart:
                    fig = static_chart_table(df_rate, rate_col)
                    img_path = os.path.join(directory, f"graf_{chart_name}_table.png")
                    save_chart_image(fig, img_path)
                    tasa_data['table_chart_path'] = img_path
                    tasa_data['table_chart'] = InlineImage(tpl, img_path, width=Mm(150))

                pivot = (
                    df_rate.pivot_table(index='Asignatura', columns='Anio', values=rate_col, aggfunc='mean')
                    .round(1).fillna('')
                )
                pivot.columns = [str(c) for c in pivot.columns]
                pivot.index.name = 'Asignatura'
                prompt = PromptAnalisisPar(
                    universidad=institucion,
                    titulacion=titulacion,
                    contexto_grupo=f"{curso_nombre} – {tipologia_nombre}",
                    tasa_nombre=TASAS[rate_col],
                    objetivo=target_value,
                    limite=limit_value,
                    datos=pivot.to_string(),
                ).build()
                tasa_data['text'] = generate_text(prompt)

                tipologia_data['rates'].append(tasa_data)

            course_data['tipologies'].append(tipologia_data)

        breakdown_data['breakdown'].append(course_data)

    # Resume
    df_agrupado = (
        df[['Tipologia', 'Tasa_Exito', 'Tasa_Rendimiento']]
        .groupby('Tipologia')[['Tasa_Exito', 'Tasa_Rendimiento']].mean()
        .reset_index()
    )

    prompt = PromptResumenDesgloseTipologia(
        universidad=institucion,
        titulacion=titulacion,
        datos=df_agrupado.to_string(index=False),
    ).build()
    breakdown_data['resume_text'] = generate_text(prompt)

    fig = static_chart_bars_breakdown_resume(df_agrupado, "Resumen de Medias por Tipología")
    img_path = os.path.join(directory, "graf_resumen_medias_tipologia.png")
    save_chart_image(fig, img_path, width=1200)
    breakdown_data['resume_chart_path'] = img_path
    breakdown_data['resume_chart'] = InlineImage(tpl, img_path, width=Mm(155))

    return breakdown_data
