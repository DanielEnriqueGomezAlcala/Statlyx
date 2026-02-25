import plotly.graph_objects as go
import pandas as pd


def create_bar_graph_medias_tipologia(df, titulo_grafica):
    # 1. Filtramos y preparamos los datos
    # Extraemos las medias de Éxito y Rendimiento por Tipo
    media_exito = df[df['Tasa'] == 'Exito'].groupby('Tipo')['Valor'].mean()
    media_rendimiento = df[df['Tasa'] == 'Rendimiento'].groupby('Tipo')['Valor'].mean()
    
    # Obtenemos las tipologías únicas para el eje X
    tipologias = media_exito.index.tolist()

    fig = go.Figure()

    # 2. Añadimos la barra de Tasa de Éxito
    fig.add_trace(go.Bar(
        x=tipologias,
        y=media_exito,
        name='Media Tasa de Éxito',
        marker_color='#1f77b4',
        text=media_exito.round(2).astype(str) + '%',
        textposition='outside',
        hovertemplate='Tipo: %{x}<br>Éxito: %{y:.2f}%<extra></extra>'
    ))

    # 3. Añadimos la barra de Tasa de Rendimiento
    fig.add_trace(go.Bar(
        x=tipologias,
        y=media_rendimiento,
        name='Media Tasa de Rendimiento',
        marker_color='#2ca02c',
        text=media_rendimiento.round(2).astype(str) + '%',
        textposition='outside',
        hovertemplate='Tipo: %{x}<br>Rendimiento: %{y:.2f}%<extra></extra>'
    ))

    # 4. Configuración del diseño (Layout)
    fig.update_layout(
        title=dict(
            text=titulo_grafica,
            x=0.5,
            font=dict(size=24, color='black')
        ),
        barmode='group', # Esto agrupa las barras por tipología
        plot_bgcolor='white',
        font=dict(size=14, color='black'),
        yaxis=dict(
            title="Porcentaje (%)",
            range=[0, 110], 
            gridcolor='lightgray',
            ticksuffix="%"
        ),
        xaxis=dict(
            title="Tipología de Asignatura",
            linecolor='black'
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

# df = pd.read_csv('data/prueba.csv', sep=',')

# fig = create_bar_graph_medias_tipologia(df, "Resumen de Medias por Tipo")
# fig.show()