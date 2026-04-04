import plotly.graph_objects as go
import pandas as pd
from colors.colors import COLOR_HEADER


def static_chart_table(df, rate):
    anios_ordenados = sorted(df['Anio'].unique())

    header_values = [f'<b>{a}</b>' for a in anios_ordenados]

    row_values = []
    for anio in anios_ordenados:
        v = df[df['Anio'] == anio][rate].values
        val = v[0] if len(v) > 0 and pd.notna(v[0]) else None
        row_values.append(f'{val:.1f}%' if val is not None else '—')

    fill_colors = []
    for anio in anios_ordenados:
        v = df[df['Anio'] == anio][rate].values
        val = v[0] if len(v) > 0 and pd.notna(v[0]) else None
        if val is None:
            fill_colors.append('#f5f5f5')
        elif val >= 75:
            fill_colors.append('#d4edda')
        elif val >= 50:
            fill_colors.append('#fff3cd')
        else:
            fill_colors.append('#f8d7da')

    fig = go.Figure(data=[go.Table(
        columnwidth=[120] * len(anios_ordenados),
        header=dict(
            values=header_values,
            fill_color=COLOR_HEADER,
            align='center',
            font=dict(color='white', size=14),
            line_color='white',
            height=35,
        ),
        cells=dict(
            values=[[v] for v in row_values],
            fill_color=[[c] for c in fill_colors],
            align='center',
            font=dict(color='black', size=13),
            line_color='lightgray',
            height=35,
        ),
    )])

    fig.update_layout(
        height=120,
        margin=dict(l=10, r=10, t=10, b=10),
    )

    return fig
