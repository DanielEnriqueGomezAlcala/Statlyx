import pandas as pd
import os
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm

# Charts
from charts.static.shared.line_chart import static_chart_lines
from charts.static.shared.table_chart import static_chart_table
from charts.static.mention_breakdown.resume_chart import static_chart_bars_breakdown_resume

# Utils
from utils.image import save_chart_image

# LLM
from functions.llm.llm import generate_text
from functions.llm.prompts.subject_analisis import PromptResumenDesgloseMencion, PromptAnalisisPar

# Constants
from constants import TASAS_SUBJECT as TASAS


def generate_mention_breakdown(df: pd.DataFrame, directory: str, tpl: DocxTemplate, chart_types: list[str], institucion: str = "", titulacion: str = "", target_value=None, limit_value=None):
    breakdown_data = {
        'resume_chart': None,
        'resume_text': None,
        'breakdown': [],
    }

    line_chart  = "graficas-lineas" in chart_types
    table_chart = "graficas-tablas" in chart_types

    for mention, df_mention in df.groupby('Mencion', observed=True):
        mention_data = {'name': mention, 'rates': []}

        for rate_col, rate_name in TASAS.items():
            if rate_col not in df_mention.columns:
                continue

            df_rate = df_mention[['Asignatura', 'Anio', rate_col]].dropna().copy()
            df_rate = df_rate.sort_values('Anio')
            if df_rate.empty:
                continue

            chart_name = f"{mention}_{rate_col}".replace(" ", "_").replace("/", "-")
            tasa_data = {'name': rate_name, 'line_chart': None, 'table_chart': None, 'text': None}

            if line_chart:
                fig = static_chart_lines(df_rate, rate_col, target_value=target_value, limit_value=limit_value)
                img_path = os.path.join(directory, f"graf_{chart_name}_line.png")
                save_chart_image(fig, img_path, border=6)
                tasa_data['line_chart'] = InlineImage(tpl, img_path, width=Mm(150))

            if table_chart:
                fig = static_chart_table(df_rate, rate_col)
                img_path = os.path.join(directory, f"graf_{chart_name}_table.png")
                save_chart_image(fig, img_path)
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
                contexto_grupo=f"Mención: {mention}",
                tasa_nombre=TASAS[rate_col],
                objetivo=target_value,
                limite=limit_value,
                datos=pivot.to_string(),
            ).build()
            tasa_data['text'] = generate_text(prompt)

            mention_data['rates'].append(tasa_data)

        breakdown_data['breakdown'].append(mention_data)

    # Resume
    df_agrupado = (
        df[['Mencion', 'Tasa_Exito', 'Tasa_Rendimiento']]
        .groupby('Mencion')[['Tasa_Exito', 'Tasa_Rendimiento']].mean()
        .reset_index()
    )

    prompt = PromptResumenDesgloseMencion(
        universidad=institucion,
        titulacion=titulacion,
        datos=df_agrupado.to_string(index=False),
    ).build()
    breakdown_data['resume_text'] = generate_text(prompt)

    fig = static_chart_bars_breakdown_resume(df_agrupado, "Resumen de Medias por Mención")
    img_path = os.path.join(directory, "graf_resumen_medias_mencion.png")
    save_chart_image(fig, img_path, width=1200)
    breakdown_data['resume_chart'] = InlineImage(tpl, img_path, width=Mm(155))

    return breakdown_data
