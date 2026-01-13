from pathlib import Path
from datetime import datetime
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Inches
from dash import html
from functions.charts.interactive import (
    crear_lineas_rendimiento,
    crear_comparacion_media,
    crear_tabla_resumen,
    crear_brecha_genero
)


def generar_informe_docx(carrera, universidad, df_filtrado):
    """
    Genera un informe DOCX con los gráficos de rendimiento académico
    
    Args:
        carrera (str): Nombre de la carrera
        universidad (str): Nombre de la universidad
        df_filtrado (pd.DataFrame): DataFrame filtrado con los datos de la carrera
    
    Returns:
        tuple: (success, message, docx_path o None)
    """
    try:
        # Crear directorios de salida
        base_path = Path(__file__).parent.parent.parent
        output_dir_graph = base_path / "output" / "graph"
        output_dir_graph.mkdir(parents=True, exist_ok=True)
        
        # Crear y guardar gráficos como imágenes
        fig1 = crear_lineas_rendimiento(df_filtrado, carrera)
        fig2 = crear_comparacion_media(df_filtrado, carrera)
        fig3 = crear_tabla_resumen(df_filtrado, carrera)
        fig4 = crear_brecha_genero(df_filtrado, carrera)
        
        # Guardar como imágenes PNG
        carrera_file = carrera.replace(' ', '_').replace('/', '_')
        img1_path = output_dir_graph / f"rendimiento_{carrera_file}.png"
        img2_path = output_dir_graph / f"comparacion_{carrera_file}.png"
        img3_path = output_dir_graph / f"tabla_{carrera_file}.png"
        img4_path = output_dir_graph / f"brecha_{carrera_file}.png"
        
        fig1.write_image(str(img1_path), width=1200, height=600)
        fig2.write_image(str(img2_path), width=1200, height=600)
        fig3.write_image(str(img3_path), width=1200, height=400)
        fig4.write_image(str(img4_path), width=1200, height=600)
        
        # Cargar plantilla DOCX
        template_path = base_path / "templates" / "Informe-calidad.docx"
        doc = DocxTemplate(template_path)

        fecha_hoy = datetime.now().strftime("%d/%m/%Y")

        contexto = {
            "carrera": carrera,
            "fecha": fecha_hoy,
            "autor": "Generado por Sistema de Análisis de Rendimiento Académico",
            "universidad": universidad.replace('_', ' '),
            "imagen_lineas_rendimiento": InlineImage(doc, str(img1_path), width=Inches(5)),
            "imagen_comparacion_media": InlineImage(doc, str(img2_path), width=Inches(5)),
            "imagen_tabla_resumen": InlineImage(doc, str(img3_path), width=Inches(5)),
            "imagen_brecha_genero": InlineImage(doc, str(img4_path), width=Inches(5)),
        }

        doc.render(contexto)
        
        # Guardar documento
        output_dir_docx = base_path / "output" / "informe_docx"
        output_dir_docx.mkdir(parents=True, exist_ok=True)
        docx_path = output_dir_docx / f"informe_{carrera_file}.docx"
        doc.save(str(docx_path))
        
        return True, "Informe DOCX generado exitosamente", docx_path
        
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        print(f"Error detallado: {error_detail}")
        return False, str(e), None
