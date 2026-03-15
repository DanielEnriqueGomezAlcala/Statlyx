from dash import html, dcc
import dash_mantine_components as dmc
from colors.colors import COLORS

def preview():
    return html.Div([
        dmc.Center([
            dmc.Paper([
                html.Div(id="metrics-section"),
                dmc.Stack([
                    dmc.Group([
                        dmc.Title("Previsualización de datos", order=4),
                        dmc.SegmentedControl(
                            id="table-selector",
                            data=[
                                {"value": "t1t2", "label": "Datos a nivel asignatura"},
                                {"value": "t4", "label": "Datos a nivel titulación"},
                            ],
                            color=COLORS['primary'],
                        )
                    ], justify="space-between", mb="md"),
                    
                    html.Div([
                        dmc.LoadingOverlay(
                            visible=False, 
                            zIndex=1000,
                            overlayProps={"blur": 2},
                        ),
                        # Grafico de datos de asignatura
                        html.Div(
                            dcc.Graph(
                                id='data-table-t1t2',
                                config={'displayModeBar': False}
                            ),
                            id="data-table-t1t2-container",
                        ),
                        # Grafico de datos de titulación
                        html.Div(
                            dcc.Graph(
                                id='data-table-t4',
                                config={'displayModeBar': False}
                            ),
                            id="data-table-t4-container",
                            style={"display": "none"},
                        ),
                    ], style={"position": "relative"})
                    
                ], gap="sm", style={'padding': '20px'})
            ], shadow="xs", radius="md", style={'marginBottom': '20px', 'width': '80%'})
        ]),
    ])