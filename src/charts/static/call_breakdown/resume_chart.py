import pandas as pd
import plotly.graph_objects as go
from colors.colors import COLORS

CONVOCATORIAS_ORDEN = ['Enero', 'Marzo', 'Mayo', 'Julio']

def static_chart_bars_breakdown_resume(df, titulo_grafica):
    df_medias = df.dropna(subset=['Tasa_Eficiencia', 'Tasa_Exito'], how='all').copy()
    df_medias['Convocatoria'] = pd.Categorical(df_medias['Convocatoria'], categories=CONVOCATORIAS_ORDEN, ordered=True)
    df_medias = df_medias.sort_values(['Curso', 'Convocatoria'])
    etiquetas_x = df_medias['Curso'].astype(str) + ' – ' + df_medias['Convocatoria'].astype(str)

    fig = go.Figure()

    if 'Tasa_Exito' in df_medias.columns:
        fig.add_trace(go.Bar(
            x=etiquetas_x,
            y=df_medias['Tasa_Exito'],
            name='Media Tasa de Éxito',
            marker_color=COLORS['primary'],
            text=df_medias['Tasa_Exito'].round(2).astype(str) + '%',
            textposition='outside',
            textfont=dict(size=18),
            hovertemplate='Curso: %{x}<br>Éxito: %{y:.2f}%<extra></extra>'
        ))

    if 'Tasa_Eficiencia' in df_medias.columns:
        fig.add_trace(go.Bar(
            x=etiquetas_x,
            y=df_medias['Tasa_Eficiencia'],
            name='Media Tasa de Eficiencia',
            marker_color=COLORS['secondary'],
            text=df_medias['Tasa_Eficiencia'].round(2).astype(str) + '%',
            textposition='outside',
            textfont=dict(size=18),
            hovertemplate='Curso: %{x}<br>Eficiencia: %{y:.2f}%<extra></extra>'
        ))

    fig.update_layout(
        showlegend=True,
        font=dict(size=18, color='black'),
        title=dict(
            text=titulo_grafica,
            x=0.5,
            font=dict(size=28, color='black')
        ),
        barmode='group',
        plot_bgcolor='white',
        legend=dict(
            orientation="v",
            yanchor="top",
            y=-2,
            xanchor="center",
            x=0.5,
            font=dict(size=20)
        ),
        margin=dict(r=50, t=100, l=100, b=100)
    )

    fig.update_xaxes(
        tickangle=-45,
        showgrid=False,
        linecolor='black',
        ticks='outside',
        tickfont=dict(size=20),
        type='category',
        categoryorder='array',
        categoryarray=list(etiquetas_x.values)
    )

    fig.update_yaxes(
        range=[0, 115],
        showgrid=True,
        gridcolor='lightgray',
        linecolor='black',
        ticksuffix="%",
        tickformat=".1f",
        tickfont=dict(size=20)
    )

    return fig
