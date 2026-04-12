"""
Gráfico de tabla estático compartido para el análisis a nivel de asignatura.
"""

import plotly.graph_objects as go
import pandas as pd
from colors.colors import COLOR_HEADER


def static_chart_table(df, rate):
    """
    Genera gráfico de tabla Plotly para los datos de las asignaturas.

    Args:
        df: DataFrame con los datos de las asignaturas.
        rate: Tasa a visualizar.
    """
    anios_ordenados = sorted(df["Anio"].unique())

    pivot = df.pivot_table(
        index="Asignatura", columns="Anio", values=rate, aggfunc="mean"
    )  # Se crea la tabla pivot
    pivot = pivot.reindex(columns=anios_ordenados)  # Se reindexa la tabla pivot

    asignaturas = pivot.index.tolist()

    header_values = ["<b>Asignatura</b>"] + [
        f"<b>{a}</b>" for a in anios_ordenados
    ]  # Se crean las etiquetas para la cabecera

    cell_values = [asignaturas]  # Se crean las etiquetas para las filas
    for anio in anios_ordenados:
        col = (
            pivot[anio]
            if anio in pivot.columns
            else pd.Series([None] * len(asignaturas))
        )
        cell_values.append([f"{v:.1f}%" if pd.notna(v) else "—" for v in col])

    fill_colors = [["white"] * len(asignaturas)]
    for anio in anios_ordenados:
        col = (
            pivot[anio]
            if anio in pivot.columns
            else pd.Series([None] * len(asignaturas))
        )
        colors = []
        for v in col:
            if pd.isna(v):
                colors.append("#f5f5f5")
            elif v >= 75:
                colors.append("#d4edda")
            elif v >= 50:
                colors.append("#fff3cd")
            else:
                colors.append("#f8d7da")
        fill_colors.append(colors)

    fig = go.Figure(
        data=[
            go.Table(
                columnwidth=[300] + [120] * len(anios_ordenados),
                header=dict(  # Cabecera de la tabla
                    values=header_values,
                    fill_color=COLOR_HEADER,
                    align=["left"] + ["center"] * len(anios_ordenados),
                    font=dict(color="white", size=12),
                    line_color="white",
                    height=35,
                ),
                cells=dict(  # Celdas de la tabla
                    values=cell_values,
                    fill_color=fill_colors,
                    align=["left"] + ["center"] * len(anios_ordenados),
                    font=dict(color="black", size=11),
                    line_color="lightgray",
                ),
            )
        ]
    )

    fig.update_layout(  # Layout de la grafica
        height=max(500, len(asignaturas) * 120),
        margin=dict(l=10, r=10, t=10, b=10),
    )

    return fig
