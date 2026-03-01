import pandas as pd
import os
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm

from functions.llm.llm import generate_text
from functions.llm.prompts import plantilla_resumen_tipologia
from charts.static.line_chart import static_chart_lines

def generate_career_breakdown(df: pd.DataFrame, directory: str, tpl: DocxTemplate):
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


    return career_breakdown