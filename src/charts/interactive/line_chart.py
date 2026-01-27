import plotly.graph_objects as go

def grafico_lineas_interactivo(df):
    fig = go.Figure()
            
    fig.add_trace(go.Scatter(
        x=df['Anio'],
        y=df['Valor'],
        mode='lines+markers',
        name='Evolución',
        line=dict(color='#4B1E78', width=3),
        marker=dict(size=10, symbol='diamond')
    ))
    
    fig.update_layout(
        title="Evolución Temporal de la Tasa",
        xaxis_title="Año",
        yaxis_title="Valor (%)",
        yaxis=dict(ticksuffix="%", gridcolor='lightgrey'),
        plot_bgcolor='white',
        height=500
    )

    return fig