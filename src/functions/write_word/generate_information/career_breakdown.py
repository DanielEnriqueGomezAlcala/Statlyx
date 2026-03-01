import pandas as pd
import os
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm

# LLM
from functions.llm.llm import generate_text
from functions.llm.prompts import plantilla_resumen_curso_cuatrimestre

# Charts
from charts.static.line_chart import static_chart_lines
from charts.static.bar_chart_breakdown_resume import static_chart_bars_breakdown_resume

def generate_career_breakdown(df: pd.DataFrame, directory: str, tpl: DocxTemplate, institucion: str = "", titulacion: str = ""):
    career_breakdown = {
        'resume_chart': "",
        'resume_text': "",
        'breakdown': [],
    }
    
    for curso, df_curso in df.groupby('Curso', observed=True):
        course_data = {'name': curso, 'rate': []}
        
        for rate, df_rate in df_curso.groupby('Tasa', observed=True):
            rate_data = {'name': rate, 'quarters': []}

            for (quarter, itinerary), df_final in df_rate.groupby(['Cuatrimestre', 'Itinerario']):
                chart_title = f"Tasa de {rate.lower()}"
                fig = static_chart_lines(df_final, chart_title)
                
                chart_name = f"{curso}_{rate}_{quarter}_{itinerary}".replace(" ", "_").replace("/", "-")
                img_name = f"graf_{chart_name}.png"
                img_path = os.path.join(directory, img_name)
                fig.write_image(img_path, width=1200, height=700, scale=2)
                img_obj = InlineImage(tpl, img_path, width=Mm(160))
                rate_data['quarters'].append({
                    'name': quarter,
                    'itinerary': itinerary,
                    'chart': img_obj
                })

            course_data['rate'].append(rate_data)
        career_breakdown['breakdown'].append(course_data)
    
    chart_title = "Resumen de Medias por Curso y Cuatrimestre"
    fig = static_chart_bars_breakdown_resume(df, chart_title)
    chart_name = "resumen_medias_curso_cuatrimestre".replace(" ", "_").replace("/", "-")
    img_name = f"graf_{chart_name}.png"
    img_path = os.path.join(directory, img_name)
    fig.write_image(img_path, width=1200, height=700, scale=2)
    img_obj = InlineImage(tpl, img_path, width=Mm(160))
    career_breakdown['resume_chart'] = img_obj

    datos_agrupados = df.groupby(['Curso', 'Cuatrimestre', 'Tasa'])['Valor'].mean().reset_index()
    datos_agrupados['Valor'] = datos_agrupados['Valor'].round(2)
    datos = datos_agrupados.to_string(index=False)

    prompt = plantilla_resumen_curso_cuatrimestre.substitute(
        universidad=institucion,
        titulacion=titulacion,
        datos=datos
    )
    career_breakdown['resume_text'] = generate_text(prompt)

    return career_breakdown