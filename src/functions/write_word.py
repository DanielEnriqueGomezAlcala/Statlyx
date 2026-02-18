from docxtpl import DocxTemplate, InlineImage
from typing import Dict, Any
from io import BytesIO
import os
from docx.shared import Mm
from datetime import datetime

from graphs.static.course_lines import create_static_graph_course_lines
from graphs.static.course_table import create_static_graph_course_table
from graphs.static.general_lines import create_static_graph_general_lines
from graphs.static.general_table import create_static_graph_general_table
from graphs.static.type_lines import create_static_graph_type_lines
from graphs.static.type_table import create_static_graph_type_table
from graphs.static.subject_lines import create_static_graph_subject_lines


def rellenar_plantilla(df, ruta_plantilla: str, institucion: str = None, titulacion: str = None) -> BytesIO:
    # Verificar que la plantilla existe
    if not os.path.exists(ruta_plantilla):
        raise FileNotFoundError(f"La plantilla no existe: {ruta_plantilla}")
    
    try:
        # Cargar la plantilla
        doc = DocxTemplate(ruta_plantilla)
        
        # Nombres para los gráficos
        nombre_institucion = institucion or 'Sin nombre'
        nombre_titulacion = titulacion or 'Sin titulación'
        
        # Generar gráficas de líneas de curso
        img_course_lines_bytes = create_static_graph_course_lines(df, nombre_institucion, nombre_titulacion)
        img_course_lines = InlineImage(doc, img_course_lines_bytes, width=Mm(150))
        
        # Generar tabla de curso
        img_course_table_bytes = create_static_graph_course_table(df, nombre_institucion, nombre_titulacion)
        img_course_table = InlineImage(doc, img_course_table_bytes, width=Mm(150))
        
        # Generar gráficas de líneas generales
        img_general_lines_bytes = create_static_graph_general_lines(df, nombre_institucion, nombre_titulacion)
        img_general_lines = InlineImage(doc, img_general_lines_bytes, width=Mm(150))
        
        # Generar tabla general
        img_general_table_bytes = create_static_graph_general_table(df, nombre_institucion, nombre_titulacion)
        img_general_table = InlineImage(doc, img_general_table_bytes, width=Mm(150))
        
        # Generar gráficas de líneas por tipo
        img_type_lines_bytes = create_static_graph_type_lines(df, nombre_institucion, nombre_titulacion)
        img_type_lines = InlineImage(doc, img_type_lines_bytes, width=Mm(150))
        
        # Generar tabla por tipo
        img_type_table_bytes = create_static_graph_type_table(df, nombre_institucion, nombre_titulacion)
        img_type_table = InlineImage(doc, img_type_table_bytes, width=Mm(150))
        
        # Generar gráficas de líneas por asignatura
        img_subject_lines_bytes = create_static_graph_subject_lines(df, nombre_institucion, nombre_titulacion)
        img_subject_lines = InlineImage(doc, img_subject_lines_bytes, width=Mm(150))
        
        # Preparar los datos para la plantilla
        datos = {
            'RangoAniosSeleccionado': ', '.join(sorted(df['Anio'].astype(str).unique().tolist())) if 'Anio' in df.columns else 'Todos',
            'TiposAsignaturasSeleccionado': ', '.join(df['Tipo'].unique().tolist()) if 'Tipo' in df.columns else 'Todos',
            'CursosSeleccionado': ', '.join(df['Curso'].unique().tolist()) if 'Curso' in df.columns else 'Todos',
            'NombreInstitucion': nombre_institucion,
            'NombreTitulacion': nombre_titulacion,
            'FechaCreacion': datetime.now().strftime('%d/%m/%Y'),
            'GraficoTablaGeneral': img_general_table,
            'GraficoLineasGeneral': img_general_lines,
            'AsignaturasSeleccionado': ', '.join(df['Asignatura'].unique().tolist()) if 'Asignatura' in df.columns else 'Todas',
            'GraficoLineasTasasAsignatura': img_subject_lines,
            'GraficoTablaCurso': img_course_table,
            'GraficoLineasCurso': img_course_lines,
            'GraficoTablaTipologia': img_type_table,
            'GraficoLineasTipologia': img_type_lines,
        }
        
        # Rellenar la plantilla con los datos
        doc.render(datos)
        
        # Guardar el documento en un buffer en memoria
        buffer = BytesIO()
        doc.save(buffer)
        buffer.seek(0)  # Volver al inicio del buffer
        
        return buffer
        
    except Exception as e:
        raise Exception(f"Error al procesar la plantilla: {str(e)}")

