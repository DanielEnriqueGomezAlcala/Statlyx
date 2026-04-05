from docxtpl import DocxTemplate
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import os
import pandas as pd
from datetime import datetime

from functions.generate_information.subject_analisis.subject_breakdown import generate_subject_breakdown
from functions.generate_information.subject_analisis.tipology_breakdown import generate_tipology_breakdown
from functions.generate_information.subject_analisis.mention_breakdown import generate_mention_breakdown
from functions.generate_information.subject_analisis.call_breakdown import generate_call_breakdown
from functions.generate_information.degree_analisis.degree_breakdown import generate_degree_breakdown

ENUM_CURSOS = {1: "Primero", 2: "Segundo", 3: "Tercero", 4: "Cuarto", 5: "Quinto", 6: "Sexto"}
ORDEN_CURSOS = ["Primero", "Segundo", "Tercero", "Cuarto", "Quinto", "Sexto"]

def compute_numbering(contexto: dict) -> dict:
    n = {}
    sec = 0

    if contexto.get('mostrar_analisis_titulacion'):
        sec += 1
        n['n_titulacion'] = sec
        n['titulo_titulacion'] = f"{sec}."

    if contexto.get('mostrar_analisis_asignatura'):
        sec += 1
        n['n_asignatura'] = sec
        n['titulo_asignatura'] = f"{sec}."

        sub = 0
        if contexto.get('mostrar_desglose_curso'):
            sub += 1
            n['n_desglose_curso'] = sub
            n['titulo_desglose_curso'] = f"{sec}.{sub}."

        if contexto.get('mostrar_desglose_tipologia'):
            sub += 1
            n['n_desglose_tipologia'] = sub
            n['titulo_desglose_tipologia'] = f"{sec}.{sub}."

        if contexto.get('mostrar_desglose_menciones'):
            sub += 1
            n['n_desglose_menciones'] = sub
            n['titulo_desglose_menciones'] = f"{sec}.{sub}."

        if contexto.get('mostrar_desglose_convocatoria'):
            sub += 1
            n['n_desglose_convocatoria'] = sub
            n['titulo_desglose_convocatoria'] = f"{sec}.{sub}."

    for key in ('n_titulacion', 'n_asignatura', 'n_desglose_curso',
                'n_desglose_tipologia', 'n_desglose_menciones', 'n_desglose_convocatoria',
                'titulo_titulacion', 'titulo_asignatura', 'titulo_desglose_curso',
                'titulo_desglose_tipologia', 'titulo_desglose_menciones', 'titulo_desglose_convocatoria'):
        n.setdefault(key, '')

    return n


def write_word(df, df_t4, df_conv, ruta_plantilla: str, directorio: str, chart_selector: str, chart_types=None, institucion: str = "", titulacion: str = "", target_value=None, limit_value=None):
    tpl = DocxTemplate(ruta_plantilla)

    df['Curso'] = df['Curso'].map(ENUM_CURSOS)
    df['Curso'] = pd.Categorical(df['Curso'], categories=ORDEN_CURSOS, ordered=True)
    df = df.sort_values('Curso').dropna(subset=['Curso'])

    # Calcular filtros a partir del df
    anios = df['Anio'].dropna().str.extract(r'(\d{4})')[0].astype(int)
    rango_anios = f"{anios.min()} — {anios.max()}" if not anios.empty else ''

    tipologias = ', '.join(sorted(df['Tipologia'].dropna().unique()))

    cursos_presentes = [c for c in ORDEN_CURSOS if c in df['Curso'].values]
    cursos_str = ', '.join(cursos_presentes)

    course_data = {}
    if "desglose-curso" in chart_selector:
        course_data = generate_subject_breakdown(df, directorio, tpl, chart_types, institucion, titulacion, target_value, limit_value)

    tipologies_data = {}
    if "desglose-tipologia" in chart_selector:
        tipologies_data = generate_tipology_breakdown(df, directorio, tpl, chart_types, institucion, titulacion, target_value, limit_value)
    
    mentions_data = {}
    if "desglose-menciones" in chart_selector:
        df_mentions = df[df['Mencion'] != 'No aplica']
        mentions_data = generate_mention_breakdown(df_mentions, directorio, tpl, chart_types, institucion, titulacion, target_value, limit_value)
    
    convocatoria_data = {}
    if "desglose-convocatoria" in chart_selector:
        df_conv = df_conv[df_conv['Grupo'].isin([1, 2])]
        convocatoria_data = generate_call_breakdown(df_conv, directorio, tpl, chart_types, institucion, titulacion, target_value, limit_value)

    degree_data = []
    if "analisis-titulacion" in chart_selector:
        degree_data = generate_degree_breakdown(df_t4, directorio, tpl, chart_types, institucion, titulacion)

    mostrar_asignatura = any(v in chart_selector for v in ["desglose-curso", "desglose-tipologia", "desglose-menciones", "desglose-convocatoria"])

    contexto = {
        # Datos de la institución
        'NombreInstitucion': institucion,
        'NombreTitulacion': titulacion,
        'FechaCreacion': datetime.now().strftime('%Y-%m-%d'),
        # Datos de los filtros
        'RangoAniosSeleccionado': rango_anios,
        'TiposAsignaturasSeleccionado': tipologias,
        'CursosSeleccionados': cursos_str,
        # Datos del análisis por asignatura
        'mostrar_analisis_asignatura': mostrar_asignatura,
        'mostrar_desglose_curso': "desglose-curso" in chart_selector,
        'mostrar_desglose_tipologia': "desglose-tipologia" in chart_selector,
        'mostrar_desglose_menciones': "desglose-menciones" in chart_selector,
        'mostrar_desglose_convocatoria': "desglose-convocatoria" in chart_selector,
        'course_data': course_data,
        'tipologies_data': tipologies_data,
        'mentions_data': mentions_data,
        'convocatoria_data': convocatoria_data,
        # Datos del análisis por titulación
        'mostrar_analisis_titulacion': "analisis-titulacion" in chart_selector,
        'degree_data': degree_data,
    }

    # print(contexto)

    contexto.update(compute_numbering(contexto))

    tpl.render(contexto)

    updatefields = OxmlElement('w:updateFields')
    updatefields.set(qn('w:val'), 'true')
    tpl.docx.settings.element.append(updatefields)

    ruta_guardado = os.path.join(directorio, f'{institucion}_{titulacion}_{datetime.now().strftime("%Y%m%d")}.docx')
    tpl.save(ruta_guardado)

    return ruta_guardado
