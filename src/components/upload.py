import dash_mantine_components as dmc
from dash import html
from colors.colors import COLORS
from dash_iconify import DashIconify
from dash import dcc

def upload():
    return html.Div([
        html.Div([
            dmc.Center([
                dmc.Paper([
                    html.Div(id="upload-section"),
                    dmc.Stack([
                        dmc.Title("Subir archivos", order=4),
                        dmc.Text("Sube los tres archivos Excel para comenzar el análisis", c="dimmed", size="sm"),

                        dmc.SimpleGrid(
                            cols={"base": 1, "sm": 3},
                            spacing="md",
                            children=[
                                # Tabla 1
                                dmc.Stack([
                                    dmc.Text("Tabla 1 — Asignaturas plan PDI", size="sm", fw=500),
                                    dcc.Upload(
                                        id='upload-tabla1',
                                        children=dmc.Stack([
                                            DashIconify(icon="material-symbols:upload", width=40, color=COLORS['primary']),
                                            dmc.Text("Subir Tabla 1", size="xs", c="dimmed")
                                        ], align="center", gap="xs"),
                                        style={
                                            'width': '100%',
                                            'height': '140px',
                                            'borderWidth': '2px',
                                            'borderStyle': 'dashed',
                                            'borderRadius': '10px',
                                            'borderColor': COLORS['light'],
                                            'textAlign': 'center',
                                            'display': 'flex',
                                            'alignItems': 'center',
                                            'justifyContent': 'center',
                                            'cursor': 'pointer'
                                        },
                                        multiple=False
                                    ),
                                    html.Div(id='upload-status-tabla1')
                                ], gap="xs"),

                                # Tabla 2
                                dmc.Stack([
                                    dmc.Text("Tabla 2 — Resultados asignaturas", size="sm", fw=500),
                                    dcc.Upload(
                                        id='upload-tabla2',
                                        children=dmc.Stack([
                                            DashIconify(icon="material-symbols:upload", width=40, color=COLORS['primary']),
                                            dmc.Text("Subir Tabla 2", size="xs", c="dimmed")
                                        ], align="center", gap="xs"),
                                        style={
                                            'width': '100%',
                                            'height': '140px',
                                            'borderWidth': '2px',
                                            'borderStyle': 'dashed',
                                            'borderRadius': '10px',
                                            'borderColor': COLORS['light'],
                                            'textAlign': 'center',
                                            'display': 'flex',
                                            'alignItems': 'center',
                                            'justifyContent': 'center',
                                            'cursor': 'pointer'
                                        },
                                        multiple=False
                                    ),
                                    html.Div(id='upload-status-tabla2')
                                ], gap="xs"),

                                # Tabla 4
                                dmc.Stack([
                                    dmc.Text("Tabla 4 — Evolución indicadores", size="sm", fw=500),
                                    dcc.Upload(
                                        id='upload-tabla4',
                                        children=dmc.Stack([
                                            DashIconify(icon="material-symbols:upload", width=40, color=COLORS['primary']),
                                            dmc.Text("Subir Tabla 4", size="xs", c="dimmed")
                                        ], align="center", gap="xs"),
                                        style={
                                            'width': '100%',
                                            'height': '140px',
                                            'borderWidth': '2px',
                                            'borderStyle': 'dashed',
                                            'borderRadius': '10px',
                                            'borderColor': COLORS['light'],
                                            'textAlign': 'center',
                                            'display': 'flex',
                                            'alignItems': 'center',
                                            'justifyContent': 'center',
                                            'cursor': 'pointer'
                                        },
                                        multiple=False
                                    ),
                                    html.Div(id='upload-status-tabla4')
                                ], gap="xs"),
                            ]
                        ),

                        html.Div(id='upload-status', style={'marginTop': '10px'})
                    ], gap="sm", style={'padding': '20px'})
                ], shadow="xs", radius="md", style={'marginBottom': '20px', 'width': '80%'})
            ]),
        ])
    ])
