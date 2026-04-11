from dash import html, dcc
import dash_mantine_components as dmc
from colors.colors import COLORS


def preview():
    """
    Sección de previsualización de datos.

    Returns:
        html.Div: Div con el contenido de la sección de previsualización de datos.
    """
    return html.Div(
        [
            dmc.Center(
                [
                    dmc.Paper(
                        [
                            html.Div(id="metrics-section"),
                            dmc.Stack(
                                [
                                    dmc.Group(
                                        [
                                            dmc.Title(
                                                "Previsualización de datos", order=4
                                            ),
                                            dmc.SegmentedControl(
                                                id="table-selector",
                                                value="t1t2",
                                                data=[
                                                    {
                                                        "value": "t1t2",
                                                        "label": "Datos a nivel asignatura",
                                                    },
                                                    {
                                                        "value": "t4",
                                                        "label": "Datos a nivel titulación",
                                                    },
                                                    {
                                                        "value": "conv",
                                                        "label": "Datos a nivel convocatorias",
                                                    },
                                                ],
                                                color=COLORS["primary"],
                                            ),
                                        ],
                                        justify="space-between",
                                        mb="md",
                                    ),
                                    html.Div(
                                        [
                                            # Grafico de datos de asignatura
                                            html.Div(
                                                dcc.Graph(
                                                    id="data-table-t1t2",
                                                    config={"displayModeBar": False},
                                                ),
                                                id="data-table-t1t2-container",
                                            ),
                                            # Grafico de datos de titulación
                                            html.Div(
                                                dcc.Graph(
                                                    id="data-table-t4",
                                                    config={"displayModeBar": False},
                                                ),
                                                id="data-table-t4-container",
                                                style={"display": "none"},
                                            ),
                                            # Grafico de datos de convocatorias
                                            html.Div(
                                                dcc.Graph(
                                                    id="data-table-conv",
                                                    config={"displayModeBar": False},
                                                ),
                                                id="data-table-conv-container",
                                                style={"display": "none"},
                                            ),
                                        ],
                                        style={"position": "relative"},
                                    ),
                                ],
                                gap="sm",
                                style={"padding": "20px"},
                            ),
                        ],
                        shadow="xs",
                        radius="md",
                        style={"marginBottom": "20px", "width": "80%"},
                    )
                ]
            ),
        ]
    )
