import plotly.graph_objects as go

COLORES = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f']

def static_chart_bars_typologies_resume(df, titulo_grafica): 
    df_medias = df.pivot_table(
        index='Tipo', 
        columns='Tasa',
        values='Valor',
        aggfunc='mean'
    ).reset_index()

    etiquetas_x = df_medias['Tipo']

    fig = go.Figure()

    if 'Exito' in df_medias.columns:
        fig.add_trace(go.Bar(
            x=etiquetas_x,
            y=df_medias['Exito'],
            name='Media Tasa de Éxito',
            marker_color=COLORES[0], 
            text=df_medias['Exito'].round(2).astype(str) + '%',
            textposition='outside',
            hovertemplate='Tipología: %{x}<br>Éxito: %{y:.2f}%<extra></extra>'
        ))

    if 'Rendimiento' in df_medias.columns:
        fig.add_trace(go.Bar(
            x=etiquetas_x,
            y=df_medias['Rendimiento'],
            name='Media Tasa de Rendimiento',
            marker_color=COLORES[1],
            text=df_medias['Rendimiento'].round(2).astype(str) + '%',
            textposition='outside',
            hovertemplate='Tipología: %{x}<br>Rendimiento: %{y:.2f}%<extra></extra>'
        ))

    fig.update_layout(
        title=dict(
            text=titulo_grafica,
            x=0.5,
            font=dict(size=24, color='black')
        ),
        barmode='group',
        plot_bgcolor='white',
        font=dict(size=14, color='black'),
        yaxis=dict(
            title="Media Porcentaje (%)",
            range=[0, 110],
            gridcolor='lightgray',
            ticksuffix="%"
        ),
        xaxis=dict(
            title="Tipología de Asignatura",
            linecolor='black',
            tickangle=-45
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5
        ),
        margin=dict(l=50, r=50, t=100, b=50)
    )

    return fig