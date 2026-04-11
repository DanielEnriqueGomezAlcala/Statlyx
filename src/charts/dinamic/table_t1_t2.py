import plotly.graph_objects as go
from colors.colors import COLORS


def dinamic_table_t1_t2(df):
    """
    Genera un objeto Plotly de tipo Tabla para visualizar los datos de las asignaturas.

    Args:
        df: DataFrame con los datos de las asignaturas.
    """
    fig = go.Figure(
        data=[
            go.Table(
                header=dict(  # Cabecera de la tabla
                    values=[
                        "<b>Codigo Asignatura</b>",
                        "<b>Tipologia</b>",
                        "<b>Curso</b>",
                        "<b>Cuatrimestre</b>",
                        "<b>Mencion</b>",
                        "<b>Año</b>",
                        "<b>Matriculados</b>",
                        "<b>Asignatura</b>",
                        "<b>Tasa Rendimiento</b>",
                        "<b>Tasa Exito</b>",
                    ],
                    fill_color=COLORS["primary"],
                    align="center",
                    font=dict(color="white", size=12),
                    line_color="black",
                    height=35,
                ),
                cells=dict(  # Celdas de la tabla
                    values=[
                        df[col].tolist()
                        for col in [
                            "Codigo",
                            "Tipologia",
                            "Curso",
                            "Cuatrimestre",
                            "Mencion",
                            "Anio",
                            "Matriculados",
                            "Asignatura",
                            "Tasa_Rendimiento",
                            "Tasa_Exito",
                        ]
                    ],
                    fill_color="white",
                    align=["center"],
                    font=dict(color="black", size=12),
                    line_color="black",
                    height=30,
                ),
            )
        ]
    )

    fig.update_layout(  # Layout de la tabla - Titulo y margenes
        title="<b>Tabla de Datos - Nivel Asignatura</b>",
        title_font_color=COLORS["primary"],
        margin=dict(l=10, r=10, t=60, b=10),
    )
    return fig
