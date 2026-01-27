import plotly.graph_objects as go

def grafico_tabla(df, tasa, ruta):
    fig = go.Figure(data=[go.Table(
        header=dict(
            values=["<b>Año</b>", "<b>Tasa de Éxito (%)</b>", "<b>P25 (%)</b>", "<b>P50 (%)</b>", "<b>P75 (%)</b>"],
            fill_color='#4B1E78', # Morado oscuro similar al de tu imagen
            align='center',
            font=dict(color='white', size=12),
            line_color='black',
            height=35
        ),
        cells=dict(
            values=[df[col] for col in df.columns],
            fill_color='white',
            align=['center'],
            font=dict(color='black', size=12),
            line_color='black',
            height=30
        )
    )])

    fig.update_layout(
        title=f"<b>Evolución en la tasa de {tasa} por cohorte de egreso</b>",
        margin=dict(l=10, r=10, t=60, b=10)
    )

    fig.write_image(f"{ruta}", width=800, height=500)
