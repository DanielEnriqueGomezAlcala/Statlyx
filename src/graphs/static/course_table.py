import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from io import BytesIO

def create_static_graph_course_table(df, nombre_institucion, nombre_titulacion) -> BytesIO:
    # Agrupar por Curso y Tasa, calculando la media del Valor
    df_agrupado = df.groupby(['Curso', 'Tasa'])['Valor'].mean().reset_index()
    df_agrupado['Valor'] = df_agrupado['Valor'].round(2)
    
    # Ordenar por Curso y Tasa
    df_agrupado = df_agrupado.sort_values(['Curso', 'Tasa'])
    
    # Obtener las tasas únicas
    tasas_unicas = df_agrupado['Tasa'].unique()
    num_tasas = len(tasas_unicas)
    
    # Crear subplots - una tabla por tasa
    fig = make_subplots(
        rows=num_tasas, 
        cols=1,
        subplot_titles=[f"<b>{tasa}</b>" for tasa in tasas_unicas],
        specs=[[{"type": "table"}] for _ in range(num_tasas)],
        vertical_spacing=0.12,
        row_heights=[300 for _ in range(num_tasas)]
    )
    
    # Crear una tabla para cada tasa
    for i, tasa in enumerate(tasas_unicas, 1):
        df_tasa = df_agrupado[df_agrupado['Tasa'] == tasa]
        
        fig.add_trace(
            go.Table(
                header=dict(
                    values=["<b>Curso</b>", "<b>Media (%)</b>"],
                    fill_color='#5C068C',
                    align='center',
                    font=dict(color='white', size=12),
                    line_color='black',
                    height=28
                ),
                cells=dict(
                    values=[df_tasa['Curso'], df_tasa['Valor']],
                    fill_color='white',
                    align=['center', 'center'],
                    font=dict(color='black', size=12),
                    line_color='black',
                    height=24
                )
            ),
            row=i, col=1
        )
    
    # Actualizar el diseño de la figura
    fig.update_layout(
        title=f"<b>Datos por Curso: {nombre_institucion}</b><br><sub>Titulación: {nombre_titulacion}</sub>",
        title_font_color='#5C068C',
        margin=dict(l=10, r=10, t=100, b=10),
        showlegend=False
    )

    # Convertir a imagen PNG y devolver como BytesIO
    img_bytes = fig.to_image(format="png", width=1200, height=num_tasas*300, scale=2)
    buffer = BytesIO(img_bytes)
    buffer.seek(0)
    return buffer