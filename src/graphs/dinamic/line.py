import plotly.graph_objects as go
import pandas as pd

def crear_grafica_lineas(df, eje_x):
    fig = go.Figure()
    
    # Colores para cada tasa
    colores = {
        'Exito': '#5C068C',
        'Rendimiento': '#7D3C98',
    }
    
    # Crear una línea para cada tasa
    for tasa in ['Rendimiento', 'Exito']:
        df_tasa = df[df['Tasa'] == tasa]
        df_agrupado = df_tasa.groupby(eje_x)['Valor'].mean().reset_index()
        
        fig.add_trace(go.Scatter(
            x=df_agrupado[eje_x],
            y=df_agrupado['Valor'],
            mode='lines+markers',
            name=tasa.lower(),
            line=dict(color=colores.get(tasa, '#5C068C'), width=3),
            marker=dict(size=10, color=colores.get(tasa, '#5C068C')),
            hovertemplate='<b>%s</b><br>%%{x}<br>%%{y:.2f}%%<extra></extra>' % tasa.lower()
        ))
    
    fig.update_layout(
        title=dict(
            text="<b>Evolución del Rendimiento y Éxito</b>",
            font=dict(size=18)
        ),
        xaxis_title=eje_x,
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
            y=0,
            xanchor="center",
            x=0.5,
            font=dict(size=12)
        ),
        height=400
    )
    
    return fig