import plotly.graph_objects as go

COLORES = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f']

def static_chart_bars_breakdown_resume(df, titulo_grafica):
    df_medias = df.dropna(subset=['Tasa_Exito', 'Tasa_Rendimiento'], how='all').sort_values(['Curso', 'Cuatrimestre'])
    etiquetas_x = df_medias['Curso'].astype(str) + ' - C' + df_medias['Cuatrimestre'].astype(str)

    fig = go.Figure()

    if 'Tasa_Exito' in df_medias.columns:
        fig.add_trace(go.Bar(
            x=etiquetas_x,
            y=df_medias['Tasa_Exito'],
            name='Media Tasa de Éxito',
            marker_color=COLORES[0],
            text=df_medias['Tasa_Exito'].round(2).astype(str) + '%',
            textposition='outside',
            textfont=dict(size=18),
            hovertemplate='Curso: %{x}<br>Éxito: %{y:.2f}%<extra></extra>'
        ))

    if 'Tasa_Rendimiento' in df_medias.columns:
        fig.add_trace(go.Bar(
            x=etiquetas_x,
            y=df_medias['Tasa_Rendimiento'],
            name='Media Tasa de Rendimiento',
            marker_color=COLORES[1],
            text=df_medias['Tasa_Rendimiento'].round(2).astype(str) + '%',
            textposition='outside',
            textfont=dict(size=18),
            hovertemplate='Curso: %{x}<br>Rendimiento: %{y:.2f}%<extra></extra>'
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
            y=-0.5,
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
