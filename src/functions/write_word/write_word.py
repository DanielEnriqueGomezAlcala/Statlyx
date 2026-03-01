from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import os
import pandas as pd
from datetime import datetime

# Generate information
from functions.write_word.generate_information.career_breakdown import generate_career_breakdown
from functions.write_word.generate_information.itinerary_breakdown import generate_itinerary_breakdown
from functions.write_word.generate_information.typology_breakdown import generate_typology_breakdown

def write_word(df, ruta_plantilla: str, directorio: str, chart_selector: str, institucion: str = "", titulacion: str = ""):
    tpl = DocxTemplate(ruta_plantilla)
    
    breakdown_data = []
    itineraries_data = []
    typologies_data = []

    orden_cursos = ["Primero", "Segundo", "Tercero", "Cuarto"]
    orden_cuat = ["Primero", "Segundo", "Anual"]
 
    df['Curso'] = pd.Categorical(df['Curso'], categories=orden_cursos, ordered=True)
    df['Cuatrimestre'] = pd.Categorical(df['Cuatrimestre'], categories=orden_cuat, ordered=True)

    df = df.sort_values(['Curso', 'Cuatrimestre'])

    if "cuatrimestre-curso" in chart_selector:
        breakdown_data = generate_career_breakdown(df, directorio, tpl, institucion, titulacion)
    
    if "itinerario" in chart_selector:
        itineraries_data = generate_itinerary_breakdown(df, directorio, tpl, institucion, titulacion)
    
    if "tipologia" in chart_selector:
        typologies_data = generate_typology_breakdown(df, directorio, tpl, institucion, titulacion)

    # Contexto final para Jinja2
    contexto = {
        'mostrar_cuatrimestre_curso': "cuatrimestre-curso" in chart_selector,
        'mostrar_itinerario': "itinerario" in chart_selector,
        'mostrar_tipologia': "tipologia" in chart_selector,
        'NombreInstitucion': institucion,
        'NombreTitulacion': titulacion,
        'FechaCreacion': datetime.now().strftime('%Y-%m-%d'),
        'RangoAniosSeleccionado': f"{df['Anio'].min()} - {df['Anio'].max()}",
        'TiposAsignaturasSeleccionado': f"{', '.join(df['Tipo'].unique())}",
        'AsignaturasSeleccionado': f"{', '.join(df['Asignatura'].unique())}",
        'CursosSeleccionado': f"{', '.join(df['Curso'].unique())}",
        'breakdown_data': breakdown_data,
        'itineraries_data': itineraries_data,
        'typologies_data': typologies_data,
    }
    
    tpl.render(contexto)

    updatefields = OxmlElement('w:updateFields')
    updatefields.set(qn('w:val'), 'true')
    tpl.docx.settings.element.append(updatefields)

    ruta_guardado = os.path.join(directorio, f'{institucion}_{titulacion}_{datetime.now().strftime('%Y%m%d')}.docx')
    tpl.save(ruta_guardado)
    
    return ruta_guardado
    