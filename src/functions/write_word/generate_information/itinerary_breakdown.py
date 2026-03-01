import pandas as pd
import os
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm

# LLM
from functions.llm.llm import generate_text
from functions.llm.prompts import plantilla_resumen_itinerarios

# Charts
from charts.static.line_chart import static_chart_lines
from charts.static.bar_chart_itineraries_breakdown import static_chart_bars_itineraries_breakdown

def generate_itinerary_breakdown(df: pd.DataFrame, directory: str, tpl: DocxTemplate, institucion: str = "", titulacion: str = ""):
    itinerary_breakdown = {
        'resume_chart': "",
        'resume_text': "",
        'breakdown': [],
    }
    
    for curso, df_curso in df.groupby('Curso', observed=True):
        course_data = {'name': curso, 'itineraries': []}
        
        for itinerary, df_itinerary in df_curso.groupby('Itinerario', observed=True):
            itinerary_data = {'name': itinerary, 'rates': []}

            for rate, df_rate in df_itinerary.groupby('Tasa', observed=True):
                chart_title = f"{itinerary} - Tasa de {rate.lower()}"
                fig = static_chart_lines(df_rate, chart_title)
                chart_name = f"{curso}_{itinerary}_{rate}".replace(" ", "_").replace("/", "-")
                img_name = f"graf_{chart_name}.png"
                img_path = os.path.join(directory, img_name)
                fig.write_image(img_path, width=1200, height=700, scale=2)
                img_obj = InlineImage(tpl, img_path, width=Mm(160))
                itinerary_data['rates'].append({
                    'name': f"Tasa de {rate.lower()}",
                    'chart': img_obj
                })
            
            course_data['itineraries'].append(itinerary_data)
        itinerary_breakdown['breakdown'].append(course_data)
    
    chart_title = "Resumen de Medias por Itinerario"
    fig = static_chart_bars_itineraries_breakdown(df, chart_title)
    chart_name = "resumen_medias_itinerario".replace(" ", "_").replace("/", "-")
    img_name = f"graf_{chart_name}.png"
    img_path = os.path.join(directory, img_name)
    fig.write_image(img_path, width=1200, height=700, scale=2)
    img_obj = InlineImage(tpl, img_path, width=Mm(160))
    itinerary_breakdown['resume_chart'] = img_obj

    datos_agrupados = df.groupby(['Itinerario', 'Tasa'])['Valor'].mean().reset_index()
    datos_agrupados['Valor'] = datos_agrupados['Valor'].round(2)
    datos = datos_agrupados.to_string(index=False)

    prompt = plantilla_resumen_itinerarios.substitute(
        universidad=institucion,
        titulacion=titulacion,
        datos=datos
    )
    itinerary_breakdown['resume_text'] = generate_text(prompt)

    return itinerary_breakdown