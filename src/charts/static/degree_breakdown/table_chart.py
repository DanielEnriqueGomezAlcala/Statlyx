"""
Gráfico de tabla estático para el análisis de tasas a nivel de titulación.
"""

import plotly.graph_objects as go
import pandas as pd
from colors.colors import COLOR_HEADER


def static_chart_table(df, rate, lower_is_better=False):
    """
    Genera gráfico de tabla Plotly para los datos de la titulación.

    Args:
        df: DataFrame con los datos de las tasas a nivel de titulación.
        rate: Tasa a visualizar.
        lower_is_better: Es para invertir los colores de la tabla, en caso de que una tasa más baja sea mejor.
    """
    anios_ordenados = sorted(df["Anio"].unique())  # Se ordenan los años

    header_values = [f"<b>{a}</b>" for a in anios_ordenados]  # Se crean las etiquetas para la cabecera

    row_values = []  # Se crean las etiquetas para las filas
    for anio in anios_ordenados:
        v = df[df["Anio"] == anio][rate].values
        val = v[0] if len(v) > 0 and pd.notna(v[0]) else None  # Se obtiene el valor de la tasa
        row_values.append(f"{val:.1f}%" if val is not None else "—")  # Se añade el valor a la fila

    fill_colors = []
    for anio in anios_ordenados:
        v = df[df["Anio"] == anio][rate].values
        val = v[0] if len(v) > 0 and pd.notna(v[0]) else None
        if val is None:
            fill_colors.append("#f5f5f5")
        elif lower_is_better:
            if val <= 25:
                fill_colors.append("#d4edda")
            elif val <= 50:
                fill_colors.append("#fff3cd")
            else:
                fill_colors.append("#f8d7da")
        else:
            if val >= 75:
                fill_colors.append("#d4edda")
            elif val >= 50:
                fill_colors.append("#fff3cd")
            else:
                fill_colors.append("#f8d7da")

    fig = go.Figure(
        data=[
            go.Table(
                columnwidth=[120] * len(anios_ordenados),
                header=dict(  # Cabecera de la tabla
                    values=header_values,
                    fill_color=COLOR_HEADER,
                    align="center",
                    font=dict(color="white", size=14),
                    line_color="white",
                    height=35,
                ),
                cells=dict(  # Celdas de la tabla
                    values=[[v] for v in row_values],
                    fill_color=[[c] for c in fill_colors],
                    align="center",
                    font=dict(color="black", size=13),
                    line_color="lightgray",
                    height=35,
                ),
            )
        ]
    )

    fig.update_layout(  # Layout de la grafica
        height=120,
        margin=dict(l=10, r=10, t=10, b=10),
    )

    return fig
