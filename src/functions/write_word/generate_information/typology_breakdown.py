import pandas as pd
import os
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm

# LLM
from functions.llm.llm import generate_text
from functions.llm.prompts import plantilla_resumen_tipologia

# Charts
from charts.static.line_chart import static_chart_lines
from charts.static.bar_chart_typologies_resume import static_chart_bars_typologies_resume

def generate_typology_breakdown(df: pd.DataFrame, directory: str, tpl: DocxTemplate, institucion: str = "", titulacion: str = ""):
    typology_breakdown = {
        'resume_chart': "",
        'resume_text': "",
        'breakdown': [],
    }
    
    for curso, df_curso in df.groupby('Curso', observed=True):
        course_data = {'name': curso, 'typologies': []}
        
        for typology, df_typology in df_curso.groupby('Tipo', observed=True):
            typology_data = {'name': typology, 'rates': []}

            for rate, df_rate in df_typology.groupby('Tasa', observed=True):
                chart_title = f"{typology} - Tasa de {rate.lower()}"
                fig = static_chart_lines(df_rate, chart_title)
                chart_name = f"{curso}_{typology}_{rate}".replace(" ", "_").replace("/", "-")
                img_name = f"graf_{chart_name}.png"
                img_path = os.path.join(directory, img_name)
                fig.write_image(img_path, width=1200, height=700, scale=2)
                img_obj = InlineImage(tpl, img_path, width=Mm(160))
                typology_data['rates'].append({
                    'name': f"Tasa de {rate.lower()}",
                    'chart': img_obj
                })
            
            course_data['typologies'].append(typology_data)
        typology_breakdown['breakdown'].append(course_data)
    
    chart_title = "Resumen de Medias por Tipología"
    fig = static_chart_bars_typologies_resume(df, chart_title)
    chart_name = "resumen_medias_typology".replace(" ", "_").replace("/", "-")
    img_name = f"graf_{chart_name}.png"
    img_path = os.path.join(directory, img_name)
    fig.write_image(img_path, width=1200, height=700, scale=2)
    img_obj = InlineImage(tpl, img_path, width=Mm(160))
    typology_breakdown['resume_chart'] = img_obj


    df_agrupado = df.groupby(['Tipo', 'Tasa'])['Valor'].mean().reset_index()
    df_agrupado['Valor'] = df_agrupado['Valor'].round(2)
    datos = df_agrupado.to_string(index=False)
    
    prompt = plantilla_resumen_tipologia.substitute(
        universidad=institucion,
        titulacion=titulacion,
        datos=datos
    )
    typology_breakdown['resume_text'] = generate_text(prompt)

    return typology_breakdown