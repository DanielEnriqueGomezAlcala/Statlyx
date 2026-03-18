import plotly.graph_objects as go

COLORES = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f']

def static_chart_lines(df, titulo_grafica, rate):
    fig = go.Figure()

    asignaturas = df['Asignatura'].unique()
    anios_ordenados = sorted(df['Anio'].unique())

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
        showlegend=True,
        font=dict(size=18, color='black'), 
        title=dict(
            text=titulo_grafica,
            x=0.5,
            font=dict(size=28, color='black')
        ),
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

    return fig
