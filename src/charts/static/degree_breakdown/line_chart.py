import plotly.graph_objects as go
from colors.colors import CHART_COLORS


def static_chart_lines(df, rate):
    """
    Genera gráfico de línea Plotly para los datos de la titulación. Contiene una única linea

    Args:
        df: DataFrame con los datos de las tasas a nivel de titulación.
        rate: Tasa a visualizar.
    """
    df = df.sort_values("Anio")  # Se ordenan los años
    anios_ordenados = sorted(df["Anio"].unique())
    color = CHART_COLORS[0]  # Se asigna el color de la linea

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(  # Se añade la traza de la tasa
            x=df["Anio"].astype(str),
            y=df[rate],
            mode="lines+markers",
            showlegend=False,
            line=dict(color=color, width=4),
            marker=dict(size=12, color=color),
            hovertemplate="Año: %{x}<br>Valor: %{y:.2f}%<extra></extra>",
        )
    )

    fig.update_layout(  # Layout de la grafica
        height=500,
        showlegend=False,
        font=dict(size=18, color="black"),
        plot_bgcolor="white",
        margin=dict(r=50, t=20, l=100, b=80),
    )

    fig.update_xaxes(  # Layout del eje x
        tickangle=-45,
        showgrid=False,
        linecolor="black",
        ticks="outside",
        tickfont=dict(size=20),
        type="category",
        categoryorder="array",
        categoryarray=[str(a) for a in anios_ordenados],
    )

    fig.update_yaxes(  # Layout del eje y
        range=[0, 105],
        showgrid=True,
        gridcolor="lightgray",
        linecolor="black",
        ticksuffix="%",
        tickformat=".1f",
        tickfont=dict(size=20),
    )

    return fig
