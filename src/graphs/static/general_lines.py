import pandas as pd
import plotly.graph_objects as go
from io import BytesIO

def create_static_graph_general_lines(df, nombre_institucion, nombre_titulacion) -> BytesIO:
    df_agrupado = df.groupby(['Anio', 'Tasa'])['Valor'].mean().reset_index()
    
    fig = go.Figure()
    
    colores = { # Definimos paleta de colores ULL
        'Exito': '#5C068C',
        'Rendimiento': '#7D3C98',
        'Abandono': '#D5D8DC'
    }
    
    # Creamos una línea para cada tasa
    for tasa in df_agrupado['Tasa'].unique():
        data_tasa = df_agrupado[df_agrupado['Tasa'] == tasa]
        fig.add_trace(go.Scatter(
            x=data_tasa['Anio'],
            y=data_tasa['Valor'],
            mode='lines+markers',
            name=tasa,
            line=dict(color=colores.get(tasa, '#5C068C'), width=3),
            marker=dict(size=10, color=colores.get(tasa, '#5C068C')),
            hovertemplate='<b>%s</b><br>Año: %%{x}<br>Valor: %%{y:.2f}%%<extra></extra>' % tasa
        ))
    
    # Actualizamos el diseño de la figura
    fig.update_layout(
        title=f"<b>Evolución de Tasas: {nombre_institucion}</b><br><sub>Titulación: {nombre_titulacion}</sub>",
        xaxis_title="Año Académico",
        yaxis_title="Porcentaje (%)",
        yaxis=dict(
            ticksuffix="%",
            gridcolor='#E5E7E9',
            range=[0, 100]
        ),
        xaxis=dict(
            gridcolor='#E5E7E9'
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.25,
            xanchor="center",
            x=0.5,
            font=dict(size=12)
        ),
        height=500,
        margin=dict(l=10, r=10, t=80, b=10)
    )

    # Convertir a imagen PNG y devolver como BytesIO
    img_bytes = fig.to_image(format="png", width=1200, height=500, scale=2)
    buffer = BytesIO(img_bytes)
    buffer.seek(0)
    return buffer