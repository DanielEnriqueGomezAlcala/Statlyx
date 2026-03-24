import plotly.graph_objects as go
import pandas as pd

COLOR_HEADER = '#5C068C'


def static_chart_table(df, rate):
    anios_ordenados = sorted(df['Anio'].unique())

    # Pivot: fila por asignatura, columna por año
    pivot = df.pivot_table(index='Asignatura', columns='Anio', values=rate, aggfunc='mean')
    pivot = pivot.reindex(columns=anios_ordenados)

    asignaturas = pivot.index.tolist()

    # Cabecera
    header_values = ['<b>Asignatura</b>'] + [f'<b>{a}</b>' for a in anios_ordenados]

    # Valores de celda: columna de nombres + una columna por año
    cell_values = [asignaturas]
    for anio in anios_ordenados:
        col = pivot[anio] if anio in pivot.columns else pd.Series([None] * len(asignaturas))
        cell_values.append([f'{v:.1f}%' if pd.notna(v) else '—' for v in col])

    # Color de fondo por rango de valor
    fill_colors = [['white'] * len(asignaturas)]  # columna de asignaturas, sin color
    for anio in anios_ordenados:
        col = pivot[anio] if anio in pivot.columns else pd.Series([None] * len(asignaturas))
        colors = []
        for v in col:
            if pd.isna(v):
                colors.append('#f5f5f5')
            elif v >= 75:
                colors.append('#d4edda')
            elif v >= 50:
                colors.append('#fff3cd')
            else:
                colors.append('#f8d7da')
        fill_colors.append(colors)

    fig = go.Figure(data=[go.Table(
        columnwidth=[300] + [120] * len(anios_ordenados),
        header=dict(
            values=header_values,
            fill_color=COLOR_HEADER,
            align=['left'] + ['center'] * len(anios_ordenados),
            font=dict(color='white', size=12),
            line_color='white',
            height=35,
        ),
        cells=dict(
            values=cell_values,
            fill_color=fill_colors,
            align=['left'] + ['center'] * len(anios_ordenados),
            font=dict(color='black', size=11),
            line_color='lightgray',
            height=28,
        ),
    )])

    height = 35 + len(asignaturas) * 50 + 120  # header + rows + margins

    fig.update_layout(
        height=height,
        margin=dict(l=10, r=10, t=10, b=10),
    )

    return fig
