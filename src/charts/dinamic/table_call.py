import plotly.graph_objects as go

def dinamic_table_call(df):
    fig = go.Figure(data=[go.Table(
        header=dict(
            values=["<b>Codigo Asignatura</b>", "<b>Asignatura</b>", "<b>Curso</b>", "<b>Grupo</b>", "<b>Convocatoria</b>", "<b>Tasa Eficiencia</b>", "<b>Tasa Exito</b>"],
            fill_color='#5C068C',
            align='center',
            font=dict(color='white', size=12),
            line_color='black',
            height=35
        ),
        cells=dict(
            values=[df[col].tolist() for col in ["Codigo", "Asignatura", "Curso", "Grupo", "Convocatoria", "Tasa_Eficiencia", "Tasa_Exito"]],
            fill_color='white',
            align=['center'],
            font=dict(color='black', size=12),
            line_color='black',
            height=30
        )
    )])

    fig.update_layout(
        title="<b>Tabla de Datos - Nivel Convocatoria</b>",
        title_font_color='#5C068C',
        margin=dict(l=10, r=10, t=60, b=10)
    )
    return fig

