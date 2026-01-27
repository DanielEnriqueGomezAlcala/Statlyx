import pandas as pd
import numpy as np
import plotly.graph_objects as go
from pathlib import Path
from datetime import datetime
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Inches
from charts.static.line_chart import grafico_lineas
from charts.static.table_chart import grafico_tabla
import io

def escribir_informe(carrera, universidad, df, nombre_informe="informe_academico", filtros_aplicados=None):
    try:
        # base_path debe apuntar al directorio raíz del proyecto (TFG), no a src
        base_path = Path(__file__).parent.parent.parent
        output_dir_temp = base_path / "output" / "temp"
        output_dir_temp.mkdir(parents=True, exist_ok=True)

        # Determinar la tasa desde el dataframe
        if 'Tasa' in df.columns and len(df) > 0:
            tasa = df['Tasa'].iloc[0]
        else:
            tasa = "Rendimiento"

        # Crear y guardar gráficos como imágenes
        img1_path = output_dir_temp / f"lineas_{tasa.lower()}.png"
        print(img1_path)
        img2_path = output_dir_temp / f"tabla_{tasa.lower()}.png"

        # grafico_lineas(df, tasa, img1_path)
        # grafico_tabla(df, tasa, img2_path)

        plantilla_path = base_path / "templates" / f"Informe-exito.docx"
        doc = DocxTemplate(plantilla_path)
        fecha_hoy = datetime.now().strftime("%d/%m/%Y")
        ultimo_anio = df['Anio'].max() if len(df) > 0 and 'Anio' in df.columns else "N/A"
        
        if len(df) > 0 and 'Anio' in df.columns and 'Valor' in df.columns:
            valor_ultimo_anio = df[df['Anio'] == ultimo_anio]['Valor'].values[0]
        else:
            valor_ultimo_anio = 0

        contexto = {
            "carrera": carrera,
            "fecha": fecha_hoy,
            "autor": "Generado por Sistema de Análisis de Rendimiento Académico",
            "universidad": universidad,
            "ultimo_anio": ultimo_anio,
            "valor_ultimo_anio": f"{valor_ultimo_anio}",
            "grafica_lineas_exito": InlineImage(doc, str(img1_path), width=Inches(5)),
            "grafica_tabla_exito": InlineImage(doc, str(img2_path), width=Inches(5)),
        }
        
        # Agregar filtros si se proporcionan
        if filtros_aplicados:
            contexto.update(filtros_aplicados)

        doc.render(contexto)
        
        # Guardar en buffer en lugar de archivo
        docx_buffer = io.BytesIO()
        doc.save(docx_buffer)
        docx_buffer.seek(0)

        # Limpiar directorio temporal DESPUÉS de guardar el documento
        for temp_file in output_dir_temp.iterdir():
            if temp_file.is_file():
                temp_file.unlink()

        print(f"Informe generado exitosamente en buffer")
        return True, "Informe generado exitosamente", docx_buffer, f"{nombre_informe}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"

    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        print(f"Error detallado: {error_detail}")
        return False, str(e), None, None
    