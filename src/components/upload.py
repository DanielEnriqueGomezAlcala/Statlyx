import dash_mantine_components as dmc
from dash import html
from components.upload_bar import upload_bar

UPLOAD_TABLES = [
    ("tabla1",    "Tabla 1 — Asignaturas plan PDI",        ""),
    ("tabla2",    "Tabla 2 — Resultados asignaturas",      ""),
    ("tabla4",    "Tabla 4 — Evolución indicadores",       ""),
    ("conv",     "Convocatorias — Datos de convocatoria", ""),
    ("adicional", "Datos adicionales — Tabla 1",           ""),
]


def upload():
    '''
    Sección de subida de archivos.
    '''
    return html.Div([
        html.Div(id="upload-section"),
        dmc.Center([
            dmc.Paper([
                dmc.Stack([
                    dmc.Title("Subir archivos", order=4),
                    dmc.Text(
                        "Sube los archivos Excel para comenzar el análisis",
                        c="dimmed",
                        size="sm",
                    ),

                    dmc.Accordion(
                        [upload_bar(uid, label, desc) for uid, label, desc in UPLOAD_TABLES],
                        chevronPosition="left",
                        multiple=True,
                        variant="contained",
                    ),

                    html.Div(id="upload-status", style={"marginTop": "10px"}),
                ], gap="sm", style={"padding": "20px"}),
            ], shadow="xs", radius="md", style={"marginBottom": "20px", "width": "80%"}),
        ]),
    ])
