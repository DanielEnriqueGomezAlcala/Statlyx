import pandas as pd
import plotly.graph_objects as go

COLORES = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f']

def static_chart_lines_h(df, titulo_grafica):
    fig = go.Figure()
    
    asignaturas = df['Asignatura'].unique()
    
    for i, asignatura in enumerate(asignaturas):
        datos_asig = df[df['Asignatura'] == asignatura]
        
        datos_asig = datos_asig.sort_values('Anio')
        
        color_actual = COLORES[i % len(COLORES)]
        
        fig.add_trace(go.Scatter(
            x=datos_asig['Anio'],
            y=datos_asig['Valor'],
            mode='lines+markers',
            name=asignatura,
            line=dict(color=color_actual, width=6),
            marker=dict(size=18, color=color_actual),
            hovertemplate='<b>%s</b><br>Año: %%{x}<br>Valor: %%{y:.2f}%%<extra></extra>' % asignatura
        ))

    fig.update_layout(
        width=3508,
        height=1500,
        showlegend=True,
        font=dict(size=50, color='black'), 
        title=dict(
            text=titulo_grafica,
            x=0.5,
            font=dict(size=80, color='black')
        ),
        plot_bgcolor='white',
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1.02,
            xanchor="left",
            x=1.02,
            font=dict(size=50),
            traceorder="normal",
            itemsizing="constant",
        ),
        margin=dict(r=50, t=150, l=100, b=150),
    )

    fig.update_xaxes(
        tickangle=-45,
        showgrid=False,
        linecolor='black',
        ticks='outside',
        tickfont=dict(size=50)
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor='lightgray',
        linecolor='black',
        ticksuffix="%",
        tickformat=".1f",
        tickfont=dict(size=50)
    )

    return fig
