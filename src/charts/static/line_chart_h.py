import math
import pandas as pd
import plotly.graph_objects as go

COLORES = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f',
           '#bcbd22', '#17becf', '#aec7e8', '#ffbb78', '#98df8a', '#ff9896', '#c5b0d5', '#c49c94']

MAX_PER_COL = 5


def static_chart_lines_h(df, titulo_grafica):
    fig = go.Figure()

    asignaturas = df['Asignatura'].unique()
    anios_ordenados = sorted(df['Anio'].unique())
    n = len(asignaturas)

    for i, asignatura in enumerate(asignaturas):
        datos_asig = df[df['Asignatura'] == asignatura].sort_values('Anio')
        color_actual = COLORES[i % len(COLORES)]
        legend_ref = "legend2" if i >= MAX_PER_COL else "legend"

        fig.add_trace(go.Scatter(
            x=datos_asig['Anio'].astype(str),
            y=datos_asig['Valor'],
            mode='lines+markers',
            name=asignatura,
            line=dict(color=color_actual, width=6),
            marker=dict(size=18, color=color_actual),
            legend=legend_ref,
            hovertemplate='<b>%s</b><br>Año: %%{x}<br>Valor: %%{y:.2f}%%<extra></extra>' % asignatura
        ))

    legend_common = dict(
        orientation="v",
        yanchor="top",
        y=-0.18,
        font=dict(size=50),
        traceorder="normal",
        itemsizing="constant",
    )

    if n <= MAX_PER_COL:
        legend1 = dict(**legend_common, xanchor="center", x=0.5)
        layout_legends = dict(legend=legend1)
    else:
        legend1 = dict(**legend_common, xanchor="right", x=0.48)
        legend2 = dict(**legend_common, xanchor="left", x=0.52)
        layout_legends = dict(legend=legend1, legend2=legend2)

    fig.update_layout(
        width=3508,
        height=1800,
        showlegend=True,
        font=dict(size=50, color='black'),
        title=dict(
            text=titulo_grafica,
            x=0.5,
            font=dict(size=80, color='black')
        ),
        plot_bgcolor='white',
        margin=dict(r=50, t=150, l=150, b=550),
        **layout_legends
    )

    fig.update_xaxes(
        tickangle=-45,
        showgrid=False,
        linecolor='black',
        ticks='outside',
        tickfont=dict(size=50),
        type='category',
        categoryorder='array',
        categoryarray=[str(a) for a in anios_ordenados]
    )

    fig.update_yaxes(
        range=[0, 105],
        showgrid=True,
        gridcolor='lightgray',
        linecolor='black',
        ticksuffix="%",
        tickformat=".1f",
        tickfont=dict(size=50)
    )

    return fig
