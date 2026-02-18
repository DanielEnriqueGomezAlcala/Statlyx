import pandas as pd
import plotly.graph_objects as go
from io import BytesIO

colores = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f']

def create_static_graph_test(df, tasa, curso, cuatrimestre, ruta_guardado, itinerario = None):
    fig = go.Figure()
    asignaturas = df['Asignatura'].unique()
    for i, asignatura in enumerate(asignaturas):
        fig.add_trace(go.Scatter(
            x=df[df['Asignatura'] == asignatura]['Anio'],
            y=df[df['Asignatura'] == asignatura]['Valor'],
            mode='lines+markers',
            name=asignatura,
            line=dict(color=colores[i], width=3),
            marker=dict(size=10, color=colores[i]),
            hovertemplate='<b>%s</b><br>Asignatura: %%{x}<br>Valor: %%{y:.2f}%%<extra></extra>' % asignatura
        ))
    fig.update_layout(
        title=dict(
            text=f'{tasa} - {curso} - {cuatrimestre} - {itinerario or "General"}',
            x=0.5,
            font=dict(size=16, color='black')
        ),
        plot_bgcolor='white',
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=1.02,
            font=dict(size=10)
        ),
        margin=dict(r=150)
    )

    fig.update_xaxes(
        tickangle=-90,
        showgrid=False,
        linecolor='black',
        ticks='outside'
    )

    fig.update_yaxes(
        range=[0, 105],
        showgrid=True,
        gridcolor='lightgray',
        linecolor='white',
        ticksuffix="%",
        tickformat=".2f"
    )

    fig.write_image(ruta_guardado, width=1200, height=700, scale=2)


# df = pd.read_csv('../../../data/prueba.csv')
# df = df[df['Tasa'] == 'Exito']
# df = df[df['Curso'] == 'Primero']
# df = df[df['Cuatrimestre'] == 'Primero']
# df = df[df['Itinerario'] == 'General']
# print(df)
# create_static_graph_test(df, 'EXITO', 'PRIMERO', '1er C', 'output/test.png')