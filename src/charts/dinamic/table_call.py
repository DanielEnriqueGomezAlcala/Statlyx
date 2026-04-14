"""
Tabla dinámica de datos de convocatorias.
"""

import plotly.graph_objects as go
from colors.colors import COLORS


def dinamic_table_call(df):
    """
    Genera un objeto Plotly de tipo Tabla para visualizar los datos de las convocatorias.

    Args:
        df: DataFrame con los datos de las convocatorias.
    """
    fig = go.Figure(
        data=[
            go.Table(
                header=dict(  # Cabecera de la tabla
                    values=[
                        "<b>Codigo Asignatura</b>",
                        "<b>Asignatura</b>",
                        "<b>Curso</b>",
                        "<b>Grupo</b>",
                        "<b>Convocatoria</b>",
                        "<b>Tasa Eficiencia</b>",
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
                            "Asignatura",
                            "Curso",
                            "Grupo",
                            "Convocatoria",
                            "Tasa_Eficiencia",
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
        title="<b>Tabla de Datos - Nivel Convocatoria</b>",
        title_font_color=COLORS["primary"],
        margin=dict(l=10, r=10, t=60, b=10),
    )
    return fig
