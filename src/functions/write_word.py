from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import os
import pandas as pd
from datetime import datetime

from graphs.static.asig_cuatri_curso import create_static_graph_asignatura_cuatrimestre_curso
from graphs.static.itinerario import create_static_graph_itinerario
from graphs.static.resumen import create_bar_graph_medias_tipologia

def write_word(df, ruta_plantilla: str, directorio: str, chart_selector: str, institucion: str = "", titulacion: str = ""):
    tpl = DocxTemplate(ruta_plantilla)
    
    informe_estructurado = []
    datos_itinerario = []
    datos_tipologia = []

    orden_cursos = ["Primero", "Segundo", "Tercero", "Cuarto"]
    orden_cuat = ["Primero", "Segundo", "Anual"]
 
    df['Curso'] = pd.Categorical(df['Curso'], categories=orden_cursos, ordered=True)
    df['Cuatrimestre'] = pd.Categorical(df['Cuatrimestre'], categories=orden_cuat, ordered=True)

    df = df.sort_values(['Curso', 'Cuatrimestre'])

    if "cuatrimestre-curso" in chart_selector:
        # 1. Agrupamos por Curso
        for curso, df_curso in df.groupby('Curso', observed=True):
            datos_curso = {'nombre': curso, 'tasas': []}
            
            # 2. Agrupamos por Tasa
            for tasa, df_tasa in df_curso.groupby('Tasa', observed=True):
                datos_tasa = {'nombre': tasa, 'cuatrimestres': []}
                
                # 3. Agrupamos por Cuatrimestre y Itinerario
                # Usamos dropna=False por si Itinerario es NaN en algún caso
                for (cuat, itin), df_final in df_tasa.groupby(['Cuatrimestre', 'Itinerario']):
                    
                    # --- AQUÍ USAMOS TU LÓGICA DE GRÁFICA ---
                    
                    # Definimos el título que aparecerá dentro de la gráfica
                    titulo_grafica = f"{curso} - {tasa} - {cuat} - {itin}"
                    
                    # Llamamos a la función refactorizada para obtener el objeto Figure
                    fig = create_static_graph_asignatura_cuatrimestre_curso(df_final, titulo_grafica)
                    
                    # Definimos nombre de archivo único y ruta
                    # Limpiamos caracteres raros para el nombre del archivo
                    nombre_clean = f"{curso}_{tasa}_{cuat}_{itin}".replace(" ", "_").replace("/", "-")
                    nombre_img = f"graf_{nombre_clean}.png"
                    img_path = os.path.join(directorio, nombre_img)
                    
                    # Guardamos la imagen físicamente en el directorio temporal
                    # scale=2 o 3 para alta calidad en Word
                    fig.write_image(img_path, width=1200, height=700, scale=2)
                    
                    # Creamos el objeto InlineImage para docxtpl
                    img_obj = InlineImage(tpl, img_path, width=Mm(160)) # 160mm suele encajar bien en A4
                    
                    # Añadimos a la estructura de datos
                    datos_tasa['cuatrimestres'].append({
                        'curso': curso,
                        'tasa': tasa,
                        'cuat_nombre': cuat,
                        'itinerario': itin,
                        'grafica': img_obj
                    })
                
                datos_curso['tasas'].append(datos_tasa)
            
            informe_estructurado.append(datos_curso)
    
    if "itinerario" in chart_selector:

        for curso, df_curso in df.groupby('Curso', observed=True):
            datos_curso = {'nombre': curso, 'itinerarios': []}
            
            for itin, df_itin in df_curso.groupby('Itinerario', observed=True):
                datos_itin = {'nombre': itin, 'tasas': []}
                
                if (itin == "General"): # Solo queremos las gráficas de itinerarios
                    continue
                
                for tasa, df_tasa in df_itin.groupby('Tasa', observed=True):
                    titulo_grafica = f"{itin} - Tasa de {tasa.lower()}"
                    fig = create_static_graph_itinerario(df_tasa, titulo_grafica)
                    # Limpiamos nombre del archivo
                    nombre_clean = f"{itin} - Tasa de {tasa.lower()}".replace(" ", "_").replace("/", "-")
                    nombre_img = f"graf_itin_{nombre_clean}.png"
                    img_path = os.path.join(directorio, nombre_img)

                    fig.write_image(img_path, width=1200, height=700, scale=2)
                    img_obj = InlineImage(tpl, img_path, width=Mm(160))

                    datos_itin['tasas'].append({
                        'nombre': f"Tasa de {tasa.lower()}",
                        'grafica': img_obj
                    })

                datos_curso['itinerarios'].append(datos_itin)

            datos_itinerario.append(datos_curso)
    
    if "tipologia" in chart_selector:
        
        for curso, df_curso in df.groupby('Curso', observed=True):
            datos_curso = {'nombre': curso, 'tipologias': []}
            
            for tipo, df_tipo in df_curso.groupby('Tipo', observed=True):
                datos_tipo = {'nombre': tipo, 'tasas': []}
                
                for tasa, df_tasa in df_tipo.groupby('Tasa', observed=True):
                    titulo_grafica = f"Tasa de {tasa.lower()}"
                    fig = create_static_graph_itinerario(df_tasa, titulo_grafica)

                    nombre_clean = f"Tasa de {tasa.lower()}".replace(" ", "_").replace("/", "-")
                    nombre_img = f"graf_tipo_{nombre_clean}.png"
                    img_path = os.path.join(directorio, nombre_img)

                    fig.write_image(img_path, width=1200, height=700, scale=2)
                    img_obj = InlineImage(tpl, img_path, width=Mm(160))

                    datos_tipo['tasas'].append({
                        'nombre': f"Tasa de {tasa.lower()}",
                        'grafica': img_obj
                    })

                datos_curso['tipologias'].append(datos_tipo)

            datos_tipologia.append(datos_curso)

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
        'datos': informe_estructurado,
        'datos_itinerario': datos_itinerario,
        'datos_tipologia': datos_tipologia
    }
    
    tpl.render(contexto)

    updatefields = OxmlElement('w:updateFields')
    updatefields.set(qn('w:val'), 'true')
    tpl.docx.settings.element.append(updatefields)

    ruta_guardado = os.path.join(directorio, f'{institucion}_{titulacion}_{datetime.now().strftime('%Y%m%d')}.docx')
    tpl.save(ruta_guardado)
    
    return ruta_guardado
    