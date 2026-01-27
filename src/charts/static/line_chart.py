import plotly.graph_objects as go

def grafico_lineas(df, tasa, ruta):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df['Anio'], y=df['P_25'],
        mode='lines', name='P25 del campo',
        line=dict(color='red', width=2)
    ))

    fig.add_trace(go.Scatter(
        x=df['Anio'], y=df['P_50'],
        mode='lines', name='P50 del campo',
        line=dict(color='black', width=2, dash='dot')
    ))

    fig.add_trace(go.Scatter(
        x=df['Anio'], y=df['P_75'],
        mode='lines', name='P75 del campo',
        line=dict(color='green', width=2)
    ))

    fig.add_trace(go.Scatter(
        x=df['Anio'], 
        y=df['Valor'], # Ejemplo visual
        mode='lines+markers', name='Titulación',
        line=dict(color='purple', width=4),
        marker=dict(symbol='diamond', size=10)
    ))

    fig.update_layout(
        title=f"Tasa de {tasa} al egreso por cohorte",
        xaxis_title="Cohorte de Egreso",
        yaxis_title=f"Tasa de {tasa} al egreso",
        yaxis=dict(
            ticksuffix="%",      # Agrega el símbolo % al eje Y
            gridcolor='lightgrey'
        ),
        plot_bgcolor='white', 
        legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5)
    )

    fig.write_image(f"{ruta}", width=800, height=500)