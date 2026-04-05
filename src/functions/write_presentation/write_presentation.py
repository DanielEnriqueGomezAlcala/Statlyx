import os
import pandas as pd
from datetime import datetime

from pptx import Presentation

from functions.generate_information.subject_analisis.subject_breakdown import generate_subject_breakdown
from functions.generate_information.subject_analisis.tipology_breakdown import generate_tipology_breakdown
from functions.generate_information.subject_analisis.mention_breakdown import generate_mention_breakdown
from functions.generate_information.subject_analisis.call_breakdown import generate_call_breakdown
from functions.generate_information.degree_analisis.degree_breakdown import generate_degree_breakdown

from functions.write_presentation.constants import ENUM_CURSOS, ORDEN_CURSOS, SLIDE_W, SLIDE_H
from functions.write_presentation.slides.title_slide import title_slide
from functions.write_presentation.slides.info_slide import info_slide
from functions.write_presentation.sections.degree_section import degree_section
from functions.write_presentation.sections.subject_section import subject_section
from functions.write_presentation.sections.typology_section import typology_section
from functions.write_presentation.sections.mention_section import mention_section
from functions.write_presentation.sections.call_section import call_section


def write_presentation(df, df_t4, df_conv, ruta_plantilla: str, directorio: str, chart_selector: list, chart_types=None, institucion: str = "", titulacion: str = "", target_value=None, limit_value=None) -> str:
    df['Curso'] = df['Curso'].map(ENUM_CURSOS)
    df['Curso'] = pd.Categorical(df['Curso'], categories=ORDEN_CURSOS, ordered=True)
    df = df.sort_values('Curso').dropna(subset=['Curso'])

    anios = df['Anio'].dropna().str.extract(r'(\d{4})')[0].astype(int)
    rango_anios = f"{anios.min()} — {anios.max()}" if not anios.empty else ''
    tipologias = ', '.join(sorted(df['Tipologia'].dropna().unique()))
    cursos_presentes = [c for c in ORDEN_CURSOS if c in df['Curso'].values]
    cursos_str = ', '.join(cursos_presentes)

    course_data = {}
    if "desglose-curso" in chart_selector:
        course_data = generate_subject_breakdown(
            df, directorio, None, chart_types, institucion, titulacion, target_value, limit_value
        )

    tipologies_data = {}
    if "desglose-tipologia" in chart_selector:
        tipologies_data = generate_tipology_breakdown(
            df, directorio, None, chart_types, institucion, titulacion, target_value, limit_value
        )

    mentions_data = {}
    if "desglose-menciones" in chart_selector:
        df_mentions = df[df['Mencion'] != 'No aplica']
        mentions_data = generate_mention_breakdown(
            df_mentions, directorio, None, chart_types, institucion, titulacion, target_value, limit_value
        )

    convocatoria_data = {}
    if "desglose-convocatoria" in chart_selector:
        df_conv_filtered = df_conv[df_conv['Grupo'].isin([1, 2])]
        convocatoria_data = generate_call_breakdown(
            df_conv_filtered, directorio, None, chart_types, institucion, titulacion, target_value, limit_value
        )

    degree_data = []
    if "analisis-titulacion" in chart_selector:
        degree_data = generate_degree_breakdown(
            df_t4, directorio, None, chart_types, institucion, titulacion
        )

    prs = Presentation(ruta_plantilla)
    prs.slide_width = SLIDE_W
    prs.slide_height = SLIDE_H

    fecha = datetime.now().strftime('%d/%m/%Y')
    title_slide(prs, institucion, titulacion, fecha)
    info_slide(prs, rango_anios, tipologias, cursos_str)

    if degree_data:
        degree_section(prs, degree_data)

    if course_data:
        subject_section(prs, course_data)

    if tipologies_data:
        typology_section(prs, tipologies_data)

    if mentions_data:
        mention_section(prs, mentions_data)

    if convocatoria_data:
        call_section(prs, convocatoria_data)

    ruta_guardado = os.path.join(
        directorio,
        f'{institucion}_{titulacion}_{datetime.now().strftime("%Y%m%d")}.pptx',
    )
    prs.save(ruta_guardado)
    return ruta_guardado
