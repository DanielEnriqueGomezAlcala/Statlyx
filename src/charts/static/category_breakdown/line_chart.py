import plotly.graph_objects as go

COLORES = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f']

def static_chart_lines(df, rate, target_value=None, limit_value=None):
    fig = go.Figure()

    asignaturas = df['Asignatura'].unique()
    anios_ordenados = sorted(df['Anio'].unique())
    bottom_margin = max(100, len(asignaturas) * 40)
    height = 600 + bottom_margin

    for i, asignatura in enumerate(asignaturas):
        datos_asig = df[df['Asignatura'] == asignatura]

        datos_asig = datos_asig.sort_values('Anio')

        color_actual = COLORES[i % len(COLORES)]

        fig.add_trace(go.Scatter(
            x=datos_asig['Anio'].astype(str),
            y=datos_asig[rate],
            mode='lines+markers',
            name=asignatura,
            line=dict(color=color_actual, width=4),
            marker=dict(size=12, color=color_actual),
            hovertemplate='<b>%s</b><br>Año: %%{x}<br>Valor: %%{y:.2f}%%<extra></extra>' % asignatura
        ))

    fig.update_layout(
        height=height,
        showlegend=True,
        font=dict(size=18, color='black'),
        plot_bgcolor='white',
        legend=dict(
            orientation="v",      
            yanchor="top",        
            y=-0.3,               
            xanchor="center",     
            x=0.5,                
            font=dict(size=20)
        ),
        margin=dict(r=50, t=20, l=100, b=bottom_margin)
    )

    fig.update_xaxes(
        tickangle=-45,
        showgrid=False,
        linecolor='black',
        ticks='outside',
        tickfont=dict(size=20),
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
        tickfont=dict(size=20)
    )

    if target_value is not None:
        fig.add_hline(
            y=target_value,
            line=dict(color='green', width=2, dash='dash'),
            annotation_text=f'Objetivo: {target_value}%',
            annotation_position='top right',
            annotation_font=dict(size=16, color='green'),
        )

    if limit_value is not None:
        fig.add_hline(
            y=limit_value,
            line=dict(color='red', width=2, dash='dash'),
            annotation_text=f'Límite: {limit_value}%',
            annotation_position='bottom right',
            annotation_font=dict(size=16, color='red'),
        )

    return fig
