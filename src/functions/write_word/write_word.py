from docxtpl import DocxTemplate
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import os
import pandas as pd
from datetime import datetime

from functions.write_word.generate_information.career_breakdown import generate_career_breakdown
from functions.write_word.generate_information.typology_breakdown import generate_typology_breakdown
from functions.write_word.generate_information.degree_breakdown import generate_degree_breakdown

ENUM_CURSOS = {1: "Primero", 2: "Segundo", 3: "Tercero", 4: "Cuarto", 5: "Quinto", 6: "Sexto"}
ORDEN_CURSOS = ["Primero", "Segundo", "Tercero", "Cuarto", "Quinto", "Sexto"]


def write_word(df, df_t4, ruta_plantilla: str, directorio: str, chart_selector: str, chart_types=None, institucion: str = "", titulacion: str = "", target_value=None, limit_value=None):
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

    breakdown_data = {}
    if "desglose-curso" in chart_selector:
        breakdown_data = generate_career_breakdown(df, directorio, tpl, institucion, titulacion)

    typology_data = {}
    if "desglose-tipologia" in chart_selector:
        typology_data = generate_typology_breakdown(df, directorio, tpl, institucion, titulacion)

    degree_data = []
    if "analisis-titulacion" in chart_selector:
        degree_data = generate_degree_breakdown(df_t4, directorio, tpl, institucion, titulacion)

    mostrar_asignatura = any(v in chart_selector for v in ["desglose-curso", "desglose-tipologia", "desglose-convocatoria"])

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
        'mostrar_desglose_convocatoria': "desglose-convocatoria" in chart_selector,
        'breakdown_data': breakdown_data,
        'typology_data': typology_data,
        # Datos del análisis por titulación
        'mostrar_analisis_titulacion': "analisis-titulacion" in chart_selector,
        'degree_data': degree_data,
    }

    tpl.render(contexto)

    updatefields = OxmlElement('w:updateFields')
    updatefields.set(qn('w:val'), 'true')
    tpl.docx.settings.element.append(updatefields)

    ruta_guardado = os.path.join(directorio, f'{institucion}_{titulacion}_{datetime.now().strftime("%Y%m%d")}.docx')
    tpl.save(ruta_guardado)

    return ruta_guardado
