import plotly.express as px
import plotly.graph_objects as go

colores_genero = {"Hombres": "#1f77b4", "Mujeres": "#e377c2", "Ambos Sexos": "#7f7f7f"}

# Gráfico de líneas de rendimiento por carrera
def GlineasRendimiento(df, carrera):
    df_rendimiento = df[(df['Tasa'] == "Rendimiento") & (df['Valor'] > 0) & (df['Carrera'] == carrera)]

    fig = px.line(
        df_rendimiento, x="Anio", y="Valor", color="Genero",
        title=f"Evolución del Rendimiento: {carrera}",
        markers=True,
        labels={"Valor": "Porcentaje (%)", "Anio": "Curso Académico"},
        color_discrete_map=colores_genero,
    )

    fig.write_image(f"../output/graph/LineasRendimiento_{carrera}.png")

# Comparacion del rendimiento de una carrera con la media universitaria
def GcomparacionMedia(df, carrera):

    ultimo_anio = df['Anio'].max()
    val_carrera = df[(df['Carrera'] == carrera) & (df['Anio'] == ultimo_anio) & (df['Tasa'] == "Rendimiento") & (df['Genero'] == "Ambos Sexos")]['Valor'].values[0]
    val_media = df[(df['Carrera'] == "Todos los ámbitos") & (df['Anio'] == ultimo_anio) & (df['Tasa'] == "Rendimiento") & (df['Genero'] == "Ambos Sexos")]['Valor'].values[0]

    fig = go.Figure()

    # Barra de la carrera
    fig.add_trace(go.Bar(
        x=[carrera],
        y=[val_carrera],
        name=carrera,
        marker_color='#1f77b4',
        text=[f"{val_carrera}%"],
        textposition='auto',
    ))

    # Línea horizontal para la media
    fig.add_shape(
        type="line",
        x0=-0.5, x1=0.5, y0=val_media, y1=val_media,
        line=dict(color="Red", width=3, dash="dashdot"),
    )

    # Anotación para la media
    fig.add_annotation(
        x=0.5, y=val_media,
        text=f"Media Univ: {val_media}%",
        showarrow=False,
        yshift=10,
        font=dict(color="red", size=12)
    )

    fig.update_layout(
        title=f"Rendimiento en {carrera} vs Media Universidad",
        yaxis=dict(title="Porcentaje", range=[0, 100]),
        template="plotly_white",
        height=500,
        width=600
    )

    fig.write_image(f"../output/graph/ComparacionMedia_{carrera}.png")

# Tabla de resumen con datos del último año

def GtablaResumen(df, carrera):

    ultimo_anio = df['Anio'].max()

    # Resumen de los últimos 3 años
    df_tabla = df[(df['Genero'] != "Ambos Sexos") & (df['Carrera'] == carrera) & (df['Anio'] >= ultimo_anio)]

    fig = go.Figure(data=[go.Table(
        header=dict(values=['Tasa', 'Género', 'Valor (%)'],
                    fill_color='paleturquoise', align='left'),
        cells=dict(values=[df_tabla.Tasa, df_tabla.Genero, df_tabla.Valor],
                    fill_color='lavender', align='left'))
    ])
    
    fig.write_image(f"../output/graph/TablaResumen_{carrera}.png")

# Grafico brecha entre hombres y mujeres

def GbrechaGenero(df, carrera):

    df_gap = df[(df['Genero'].isin(['Mujeres', 'Hombres'])) & 
                (df['Tasa'] == "Rendimiento") & 
                (df['Carrera'] == carrera)].copy()

    df_pivot = df_gap.pivot(index='Anio', columns='Genero', values='Valor').reset_index()

    df_pivot = df_pivot.sort_values('Anio')

    fig = go.Figure()

    for i, row in df_pivot.iterrows():
        fig.add_shape(
            type="line",
            x0=row['Hombres'], x1=row['Mujeres'],
            y0=row['Anio'], y1=row['Anio'],
            line=dict(color="#dcdcdc", width=3)
        )

    fig.add_trace(go.Scatter(
        x=df_pivot['Hombres'], 
        y=df_pivot['Anio'],
        mode='markers',
        name='Hombres',
        marker=dict(color='#1f77b4', size=12, symbol='circle'),
        hovertemplate="Hombres: %{x}%<extra></extra>"
    ))

    fig.add_trace(go.Scatter(
        x=df_pivot['Mujeres'], 
        y=df_pivot['Anio'],
        mode='markers',
        name='Mujeres',
        marker=dict(color='#e377c2', size=12, symbol='circle'),
        hovertemplate="Mujeres: %{x}%<extra></extra>"
    ))

    for i, row in df_pivot.iterrows():
        brecha = row['Mujeres'] - row['Hombres']
        pos_x = max(row['Mujeres'], row['Hombres']) + 1 
        
        fig.add_annotation(
            x=pos_x, y=row['Anio'],
            text=f"Δ {brecha:+.2f}%",
            showarrow=False,
            xanchor="left",
            font=dict(size=10, color="gray")
        )

    fig.update_layout(
        title=dict(
            text=f"<b>Brecha de Género en Rendimiento</b><br>Carrera: Informática",
            font=dict(size=18)
        ),
        xaxis=dict(
            title="Tasa de Rendimiento (%)",
            gridcolor='#f0f0f0',
            range=[df_gap['Valor'].min() - 5, df_gap['Valor'].max() + 8]
        ),
        yaxis=dict(title="Curso Académico", gridcolor='#f0f0f0'),
        margin=dict(l=100, r=80, t=80, b=50),
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=500
    )

    fig.show()