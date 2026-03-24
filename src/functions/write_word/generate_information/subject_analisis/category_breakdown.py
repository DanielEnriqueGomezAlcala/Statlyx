import pandas as pd
import os
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm

# graphs
from charts.static.category_breakdown.line_chart import static_chart_lines
from charts.static.category_breakdown.table_chart import static_chart_table
from charts.static.category_breakdown.resume_chart import static_chart_bars_breakdown_resume

# LLM
from functions.llm.llm import generate_text
from functions.llm.prompts.subject_analisis import PromptResumenDesgloseTipologia, PromptResumenDesgloseMencion

TASAS = {
    'Tasa_Exito': 'Tasa de Éxito',
    'Tasa_Rendimiento': 'Tasa de Rendimiento',
}

CHUNK_SIZE = 7

CURSOS = {
    1: 'Primero',
    2: 'Segundo',
    3: 'Tercero',
    4: 'Cuarto',
    5: 'Quinto',
    6: 'Sexto',
}

TIPOLOGIAS = {
    'FORMACIÓN BÁSICA': 'Formación Básica',
    'OBLIGATORIA': 'Obligatoria',
    'OPTATIVA': 'Optativa',
    'TRABAJO FIN DE GRADO': 'Trabajo Fin de Grado',
    'PRÁCTICAS EXTERNAS': 'Prácticas Externas',
}

def generate_category_breakdown_tipologies(df: pd.DataFrame, directory: str, tpl: DocxTemplate, chart_types: list[str], institucion: str = "", titulacion: str = "", target_value=None, limit_value=None):
    breakdown_data = {
        'resume_chart': None,
        'resume_text': None,
        'breakdown': [],
    }

    line_chart = "graficas-lineas" in chart_types
    table_chart = "graficas-tablas" in chart_types

    # Breakdown by course and quarter

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

                asignaturas = df_rate['Asignatura'].unique()
                chunks = [asignaturas[i:i+CHUNK_SIZE] for i in range(0, len(asignaturas), CHUNK_SIZE)]

                tasa_data = {'name': rate_name, 'parts': []}
                chart_name = f"{curso_nombre}_{tipologia}_{rate_col}".replace(" ", "_").replace("/", "-")

                for part_idx, chunk in enumerate(chunks, 1):
                    df_chunk = df_rate[df_rate['Asignatura'].isin(chunk)]
                    suffix = f"_p{part_idx}" if len(chunks) > 1 else ""
                    part = {'line_chart': None, 'table_chart': None}

                    if line_chart:
                        fig = static_chart_lines(df_chunk, rate_col, target_value=target_value, limit_value=limit_value)
                        img_path = os.path.join(directory, f"graf_{chart_name}{suffix}_line.png")
                        fig.write_image(img_path, width=1200, scale=2)
                        part['line_chart'] = InlineImage(tpl, img_path, width=Mm(160))

                    if table_chart:
                        fig = static_chart_table(df_chunk, rate_col)
                        img_path = os.path.join(directory, f"graf_{chart_name}{suffix}_table.png")
                        fig.write_image(img_path, width=1200, scale=2)
                        part['table_chart'] = InlineImage(tpl, img_path, width=Mm(160))

                    tasa_data['parts'].append(part)

                tipologia_data['rates'].append(tasa_data)
            
            course_data['tipologies'].append(tipologia_data)
        
        breakdown_data['breakdown'].append(course_data)

    # Resume

    df_resume = df[['Curso', 'Tipologia', 'Tasa_Exito', 'Tasa_Rendimiento']]
    df_agrupado = df_resume.groupby(['Tipologia'])[['Tasa_Exito', 'Tasa_Rendimiento']].mean().reset_index()

    prompt = PromptResumenDesgloseTipologia(
        universidad=institucion,
        titulacion=titulacion,
        datos=df_agrupado.to_string(index=False),
    ).build()
    breakdown_data['resume_text'] = generate_text(prompt)

    fig = static_chart_bars_breakdown_resume(df_agrupado, "Resumen de Medias por Tipología")
    img_path = os.path.join(directory, f"graf_resumen_medias_curso_tipologia.png")
    fig.write_image(img_path, width=1200, height=700, scale=2)
    breakdown_data['resume_chart'] = InlineImage(tpl, img_path, width=Mm(160))

    return breakdown_data

def generate_category_breakdown_mentions(df: pd.DataFrame, directory: str, tpl: DocxTemplate, chart_types: list[str], institucion: str = "", titulacion: str = "", target_value=None, limit_value=None):
    breakdown_data = {
        'resume_chart': None,
        'resume_text': None,
        'breakdown': [],
    }

    line_chart = "graficas-lineas" in chart_types
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

            asignaturas = df_rate['Asignatura'].unique()
            chunks = [asignaturas[i:i+CHUNK_SIZE] for i in range(0, len(asignaturas), CHUNK_SIZE)]

            tasa_data = {'name': rate_name, 'parts': []}
            chart_name = f"{mention}_{rate_col}".replace(" ", "_").replace("/", "-")

            for part_idx, chunk in enumerate(chunks, 1):
                df_chunk = df_rate[df_rate['Asignatura'].isin(chunk)]
                suffix = f"_p{part_idx}" if len(chunks) > 1 else ""
                part = {'line_chart': None, 'table_chart': None}

                if line_chart:
                    fig = static_chart_lines(df_chunk, rate_col, target_value=target_value, limit_value=limit_value)
                    img_path = os.path.join(directory, f"graf_{chart_name}{suffix}_line.png")
                    fig.write_image(img_path, width=1200, scale=2)
                    part['line_chart'] = InlineImage(tpl, img_path, width=Mm(160))

                if table_chart:
                    fig = static_chart_table(df_chunk, rate_col)
                    img_path = os.path.join(directory, f"graf_{chart_name}{suffix}_table.png")
                    fig.write_image(img_path, width=1200, scale=2)
                    part['table_chart'] = InlineImage(tpl, img_path, width=Mm(160))

                tasa_data['parts'].append(part)

            mention_data['rates'].append(tasa_data)
        
        breakdown_data['breakdown'].append(mention_data)

    # Resume

    df_resume = df[['Mencion', 'Tasa_Exito', 'Tasa_Rendimiento']]
    df_agrupado = df_resume.groupby(['Mencion'])[['Tasa_Exito', 'Tasa_Rendimiento']].mean().reset_index()

    prompt = PromptResumenDesgloseMencion(
        universidad=institucion,
        titulacion=titulacion,
        datos=df_agrupado.to_string(index=False),
    ).build()
    breakdown_data['resume_text'] = generate_text(prompt)

    fig = static_chart_bars_breakdown_resume(df_agrupado, "Resumen de Medias por Mención")
    img_path = os.path.join(directory, f"graf_resumen_medias_mencion.png")
    fig.write_image(img_path, width=1200, height=700, scale=2)
    breakdown_data['resume_chart'] = InlineImage(tpl, img_path, width=Mm(160))

    return breakdown_data

def generate_category_breakdown(df: pd.DataFrame, directory: str, tpl: DocxTemplate, chart_types: list[str], institucion: str = "", titulacion: str = "", target_value=None, limit_value=None):
    df_mentions = df[df['Mencion'] != 'No aplica']
    breakdown_data = {
      'tipologies': generate_category_breakdown_tipologies(df, directory, tpl, chart_types, institucion, titulacion, target_value, limit_value),
      'mentions': generate_category_breakdown_mentions(df_mentions, directory, tpl, chart_types, institucion, titulacion, target_value, limit_value),
    }
    return breakdown_data