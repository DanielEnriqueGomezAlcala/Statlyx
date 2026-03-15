import plotly.graph_objects as go

def dinamic_table_t1_t2(df):
    fig = go.Figure(data=[go.Table(
        header=dict(
            values=["<b>Codigo Asignatura</b>", "<b>Tipologia</b>", "<b>Curso</b>", "<b>Año</b>", "<b>Matriculados</b>", "<b>Asignatura</b>", "<b>Tasa Rendimiento</b>", "<b>Tasa Exito</b>"],
            fill_color='#5C068C',
            align='center',
            font=dict(color='white', size=12),
            line_color='black',
            height=35
        ),
        cells=dict(
            values=[df[col].tolist() for col in ["Codigo", "Tipologia", "Curso", "Anio", "Matriculados", "Asignatura", "Tasa_Rendimiento", "Tasa_Exito"]],
            fill_color='white',
            align=['center'],
            font=dict(color='black', size=12),
            line_color='black',
            height=30
        )
    )])

    fig.update_layout(
        title="<b>Tabla de Datos - Nivel Asignatura</b>",
        title_font_color='#5C068C',
        margin=dict(l=10, r=10, t=60, b=10)
    )
    return fig

