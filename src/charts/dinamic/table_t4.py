"""
Tabla dinámica de datos de titulación.
"""

import plotly.graph_objects as go
from colors.colors import COLORS


def dinamic_table_t4(df):
    """
    Genera un objeto Plotly de tipo Tabla para visualizar los datos de la titulación.

    Args:
        df: DataFrame con los datos de la titulación.
    """
    if df.empty:
        return go.Figure()

    fig = go.Figure(
        data=[
            go.Table(
                header=dict(  # Cabecera de la tabla
                    values=[
                        "<b>Año</b>",
                        "<b>Tasa Graduación</b>",
                        "<b>Tasa Abandono</b>",
                        "<b>Tasa Eficiencia</b>",
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
                            "Anio",
                            "Tasa_Graduacion",
                            "Tasa_Abandono",
                            "Tasa_Eficiencia",
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
        title="<b>Tabla de Datos - Nivel Titulación</b>",
        title_font_color=COLORS["primary"],
        margin=dict(l=10, r=10, t=60, b=10),
    )
    return fig
