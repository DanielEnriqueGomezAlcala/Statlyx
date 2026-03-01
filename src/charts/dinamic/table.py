import plotly.graph_objects as go
import pandas as pd

# Funcion que crea una tabla de datos de manera dinamica usando plotly
def dinamic_table(df):
    fig = go.Figure(data=[go.Table(
        header=dict(
            values=["<b>Año</b>", "<b>Tasa</b>", "<b>Curso</b>", "<b>Cuatrimestre</b>", "<b>Asignatura</b>", "<b>Valor</b>", "<b>Convocatoria</b>", "<b>Tipología</b>", "<b>Itinerario</b>"],
            fill_color='#5C068C',
            align='center',
            font=dict(color='white', size=12),
            line_color='black',
            height=35
        ),
        cells=dict(
            values=[df[col].tolist() for col in ["Anio", "Tasa", "Curso", "Cuatrimestre", "Asignatura", "Valor", "Convocatoria", "Tipo", "Itinerario"]],
            fill_color='white',
            align=['center'],
            font=dict(color='black', size=12),
            line_color='black',
            height=30
        )
    )])

    fig.update_layout(
        title="<b>Datos Detallados</b>",
        title_font_color='#5C068C',
        margin=dict(l=10, r=10, t=60, b=10)
    )
    return fig

