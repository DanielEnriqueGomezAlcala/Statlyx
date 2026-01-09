"""
Gráficos interactivos para el Dashboard
Estos gráficos retornan objetos Plotly Figure que pueden ser usados directamente en Dash
"""

import plotly.express as px
import plotly.graph_objects as go

# Colores institucionales
colores_genero = {"Hombres": "#1f77b4", "Mujeres": "#e377c2", "Ambos Sexos": "#7f7f7f"}


def crear_lineas_rendimiento(df, carrera):
    """
    Líneas de evolución del rendimiento por género
    
    Args:
        df: DataFrame con los datos
        carrera: Nombre de la carrera a visualizar
        
    Returns:
        fig: Objeto plotly.graph_objects.Figure
    """
    df_rendimiento = df[
        (df['Tasa'] == "Rendimiento") & 
        (df['Valor'] > 0) & 
        (df['Carrera'] == carrera)
    ]
    
    fig = px.line(
        df_rendimiento, 
        x="Anio", y="Valor", color="Genero",
        title=f"Evolución del Rendimiento: {carrera}",
        markers=True,
        labels={"Valor": "Porcentaje (%)", "Anio": "Curso Académico"},
        color_discrete_map=colores_genero,
    )
    
    fig.update_layout(
        template="plotly_white",
        hovermode='x unified',
        height=500
    )
    
    return fig


def crear_comparacion_media(df, carrera):
    """
    Comparación con barra vertical y línea de media
    
    Args:
        df: DataFrame con los datos
        carrera: Nombre de la carrera a visualizar
        
    Returns:
        fig: Objeto plotly.graph_objects.Figure
    """
    ultimo_anio = df['Anio'].max()
    
    # Valor de la carrera
    val_carrera_data = df[
        (df['Carrera'] == carrera) & 
        (df['Anio'] == ultimo_anio) & 
        (df['Tasa'] == "Rendimiento") & 
        (df['Genero'] == "Ambos Sexos")
    ]['Valor'].values
    
    # Media global
    val_media_data = df[
        (df['Carrera'] == "Todos los ámbitos") & 
        (df['Anio'] == ultimo_anio) & 
        (df['Tasa'] == "Rendimiento") & 
        (df['Genero'] == "Ambos Sexos")
    ]['Valor'].values
    
    val_carrera = val_carrera_data[0] if len(val_carrera_data) > 0 else 0
    val_media = val_media_data[0] if len(val_media_data) > 0 else 0
    
    fig = go.Figure()
    
    # Barra de la carrera
    fig.add_trace(go.Bar(
        x=[carrera],
        y=[val_carrera],
        name=carrera,
        marker_color='#1f77b4',
        text=[f"{val_carrera:.1f}%"],
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
        text=f"Media Univ: {val_media:.1f}%",
        showarrow=False,
        yshift=10,
        font=dict(color="red", size=12)
    )
    
    fig.update_layout(
        title=f"Rendimiento en {carrera} vs Media Universidad ({ultimo_anio})",
        yaxis=dict(title="Porcentaje (%)", range=[0, 100]),
        template="plotly_white",
        height=500,
        showlegend=False
    )
    
    return fig


def crear_tabla_resumen(df, carrera):
    """
    Tabla con datos del último año académico
    
    Args:
        df: DataFrame con los datos
        carrera: Nombre de la carrera a visualizar
        
    Returns:
        fig: Objeto plotly.graph_objects.Figure
    """
    ultimo_anio = df['Anio'].max()
    
    df_tabla = df[
        (df['Genero'] != "Ambos Sexos") & 
        (df['Carrera'] == carrera) & 
        (df['Anio'] >= ultimo_anio)
    ]
    
    fig = go.Figure(data=[go.Table(
        header=dict(
            values=['Tasa', 'Género', 'Valor (%)'],
            fill_color='paleturquoise',
            align='left',
            font=dict(size=12, color='black')
        ),
        cells=dict(
            values=[df_tabla.Tasa, df_tabla.Genero, df_tabla.Valor.round(2)],
            fill_color='lavender',
            align='left',
            font=dict(size=11)
        )
    )])
    
    fig.update_layout(
        title=f"Resumen del Año Académico {ultimo_anio}",
        height=300,
        margin=dict(l=10, r=10, t=40, b=10)
    )
    
    return fig


def crear_brecha_genero(df, carrera):
    """
    Gráfico de mancuernas mostrando la brecha entre Hombres y Mujeres
    
    Args:
        df: DataFrame con los datos
        carrera: Nombre de la carrera a visualizar
        
    Returns:
        fig: Objeto plotly.graph_objects.Figure
    """
    # Filtrar datos
    df_gap = df[
        (df['Genero'].isin(['Mujeres', 'Hombres'])) & 
        (df['Tasa'] == "Rendimiento") & 
        (df['Carrera'] == carrera)
    ].copy()
    
    # Pivotar
    df_pivot = df_gap.pivot(
        index='Anio', 
        columns='Genero', 
        values='Valor'
    ).reset_index()
    
    # Ordenar por año
    df_pivot = df_pivot.sort_values('Anio')
    
    fig = go.Figure()
    
    # Añadir las líneas de la "mancuerna"
    for i, row in df_pivot.iterrows():
        fig.add_shape(
            type="line",
            x0=row['Hombres'], x1=row['Mujeres'],
            y0=row['Anio'], y1=row['Anio'],
            line=dict(color="#dcdcdc", width=3)
        )
    
    # Puntos de Hombres
    fig.add_trace(go.Scatter(
        x=df_pivot['Hombres'], 
        y=df_pivot['Anio'],
        mode='markers',
        name='Hombres',
        marker=dict(color='#1f77b4', size=12, symbol='circle'),
        hovertemplate="Hombres: %{x:.2f}%<extra></extra>"
    ))
    
    # Puntos de Mujeres
    fig.add_trace(go.Scatter(
        x=df_pivot['Mujeres'], 
        y=df_pivot['Anio'],
        mode='markers',
        name='Mujeres',
        marker=dict(color='#e377c2', size=12, symbol='circle'),
        hovertemplate="Mujeres: %{x:.2f}%<extra></extra>"
    ))
    
    # Añadir anotaciones de brecha
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
    
    # Configurar layout
    fig.update_layout(
        title=dict(
            text=f"<b>Brecha de Género en Rendimiento</b><br>Carrera: {carrera}",
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
        legend=dict(
            orientation="h", 
            yanchor="bottom", 
            y=1.02, 
            xanchor="right", 
            x=1
        ),
        height=500,
        hovermode='y'
    )
    
    return fig

