import math
import pandas as pd
import os
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm

# LLM
from functions.llm.llm import generate_text
from functions.llm.prompts import plantilla_resumen_curso, plantilla_resumen_curso_tasa

# Charts
from charts.static.line_chart import static_chart_lines
from charts.static.bar_chart_breakdown_resume import static_chart_bars_breakdown_resume

CHUNK_SIZE = 5


def _chunk_list(lst, max_size):
    n = len(lst)
    if n == 0:
        return
    num_chunks = math.ceil(n / max_size)
    base = n // num_chunks
    remainder = n % num_chunks
    start = 0
    for i in range(num_chunks):
        size = base + (1 if i < remainder else 0)
        yield lst[start:start + size]
        start += size


def generate_career_breakdown(df: pd.DataFrame, directory: str, tpl: DocxTemplate, institucion: str = "", titulacion: str = ""):
    career_breakdown = {
        'resume_chart': "",
        'resume_text': "",
        'breakdown': [],
    }

    df = df.melt(
        id_vars=['Codigo', 'Tipologia', 'Curso', 'Anio', 'Asignatura', 'Matriculados'],
        value_vars=['Tasa_Rendimiento', 'Tasa_Exito'],
        var_name='Tasa',
        value_name='Valor'
    )

    for curso, df_curso in df.groupby('Curso', observed=True):
        course_data = {'name': curso, 'rates': []}

        for rate, df_rate in df_curso.groupby('Tasa', observed=True):
            asignaturas = (
                df_rate.groupby('Asignatura')['Valor']
                .mean()
                .sort_values(ascending=False)
                .index.tolist()
            )
            chunks = list(_chunk_list(asignaturas, CHUNK_SIZE))
            rate_charts = []

            for i, chunk in enumerate(chunks):
                df_chunk = df_rate[df_rate['Asignatura'].isin(chunk)]
                if (rate == 'Tasa_Exito'):
                    chart_title = f"Tasa de Éxito — {curso} (parte {i + 1})"
                else:
                    chart_title = f"Tasa de Rendimiento — {curso} (parte {i + 1})"
                fig = static_chart_lines(df_chunk, chart_title, 'Valor')
                chart_name = f"{curso}_{rate}_chunk_{i+1}".replace(" ", "_").replace("/", "-")
                img_path = os.path.join(directory, f"graf_{chart_name}.png")
                fig.write_image(img_path, width=1200, height=700, scale=2)
                rate_charts.append(InlineImage(tpl, img_path, width=Mm(160)))

            datos = (
                df_rate.groupby(['Asignatura', 'Anio'])['Valor']
                .mean()
                .reset_index()
                .round(2)
                .to_string(index=False)
            )
            prompt = plantilla_resumen_curso_tasa.substitute(
                universidad=institucion,
                titulacion=titulacion,
                curso=curso,
                tasa=rate,
                datos=datos
            )

            if (rate == 'Tasa_Exito'):
                rate_name = "Tasa Éxito"
            else:
                rate_name = "Tasa Rendimiento"
            
            course_data['rates'].append({
                'name': rate_name,
                'charts': rate_charts,
                'text': generate_text(prompt)
            })

        career_breakdown['breakdown'].append(course_data)

    chart_title = "Resumen de Medias por Curso y Cuatrimestre"
    fig = static_chart_bars_breakdown_resume(df, chart_title)
    chart_name = "resumen_medias_curso_cuatrimestre"
    img_path = os.path.join(directory, f"graf_{chart_name}.png")
    fig.write_image(img_path, width=1200, height=700, scale=2)
    career_breakdown['resume_chart'] = InlineImage(tpl, img_path, width=Mm(160))

    datos_agrupados = df.groupby(['Curso', 'Tasa'])['Valor'].mean().reset_index()
    datos_agrupados['Valor'] = datos_agrupados['Valor'].round(2)
    datos = datos_agrupados.to_string(index=False)

    prompt = plantilla_resumen_curso.substitute(
        universidad=institucion,
        titulacion=titulacion,
        datos=datos
    )
    career_breakdown['resume_text'] = generate_text(prompt)

    return career_breakdown
