"""
Gráfico de barras de resumen de tasas por mención.
"""

import plotly.graph_objects as go
from colors.colors import COLORS


def static_chart_bars_breakdown_resume(df, titulo_grafica):
    """
    Genera gráfico de resumen de tasas de éxito y rendimiento por mención.

    Args:
        df: DataFrame con los datos de las menciones.
    """
    df_medias = df.dropna(
        subset=["Tasa_Exito", "Tasa_Rendimiento"], how="all"
    ).sort_values(
        "Mencion"
    )  # Se eliminan las filas con valores nulos y se ordenan las menciones
    etiquetas_x = df_medias["Mencion"].astype(
        str
    )  # Se crean las etiquetas para el eje x

    fig = go.Figure()

    if "Tasa_Exito" in df_medias.columns:  # Se añade la traza para la tasa de éxito
        fig.add_trace(
            go.Bar(
                x=etiquetas_x,
                y=df_medias["Tasa_Exito"],
                name="Media Tasa de Éxito",
                marker_color=COLORS["primary"],
                text=df_medias["Tasa_Exito"].round(2).astype(str) + "%",
                textposition="outside",
                textfont=dict(size=18),
                hovertemplate="Mención: %{x}<br>Éxito: %{y:.2f}%<extra></extra>",
            )
        )

    if (
        "Tasa_Rendimiento" in df_medias.columns
    ):  # Se añade la traza para la tasa de rendimiento
        fig.add_trace(
            go.Bar(
                x=etiquetas_x,
                y=df_medias["Tasa_Rendimiento"],
                name="Media Tasa de Rendimiento",
                marker_color=COLORS["secondary"],
                text=df_medias["Tasa_Rendimiento"].round(2).astype(str) + "%",
                textposition="outside",
                textfont=dict(size=18),
                hovertemplate="Mención: %{x}<br>Rendimiento: %{y:.2f}%<extra></extra>",
            )
        )

    fig.update_layout(  # Layout de la grafica
        showlegend=True,
        font=dict(size=18, color="black"),
        title=dict(text=titulo_grafica, x=0.5, font=dict(size=28, color="black")),
        barmode="group",
        plot_bgcolor="white",
        legend=dict(
            orientation="v",
            yanchor="top",
            y=-2,
            xanchor="center",
            x=0.5,
            font=dict(size=20),
        ),
        margin=dict(r=50, t=100, l=100, b=100),
    )

    fig.update_xaxes(  # Layout del eje x
        tickangle=-45,
        showgrid=False,
        linecolor="black",
        ticks="outside",
        tickfont=dict(size=20),
        type="category",
        categoryorder="array",
        categoryarray=list(etiquetas_x.values),
    )

    fig.update_yaxes(  # Layout del eje y
        range=[0, 115],
        showgrid=True,
        gridcolor="lightgray",
        linecolor="black",
        ticksuffix="%",
        tickformat=".1f",
        tickfont=dict(size=20),
    )

    return fig
