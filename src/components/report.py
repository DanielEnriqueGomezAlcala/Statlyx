from dash import html, dcc
import dash_mantine_components as dmc
from colors.colors import COLORS
from dash_iconify import DashIconify

def report():
    return html.Div([
        dmc.Center([
            dmc.Paper([
                html.Div(id="report-section"),
                dmc.Stack([
                    dmc.Title("Generar informe", order=4),

                    dmc.Divider(label="Contenido del informe", labelPosition="center", mt="md"),
                    dmc.Text(
                        "Selecciona las secciones que deseas incluir en el informe.",
                        size="xs", c="dimmed", ta="center", mb="sm"
                    ),

                    html.Div([
                        # Análisis por titulación
                        html.Div([
                            dmc.Checkbox(id="check-titulacion", label="Análisis por titulación", checked=False),
                            dmc.Text(
                                "Evolución de las tasas de rendimiento y éxito a nivel global de la titulación.",
                                size="xs", c="dimmed", style={"marginLeft": "28px", "marginTop": "2px"}
                            ),
                        ], style={"marginBottom": "12px"}),

                        # Análisis por asignatura
                        html.Div([
                            dmc.Checkbox(id="check-asignatura", label="Análisis por asignatura", checked=False, indeterminate=False),
                            dmc.Text(
                                "Rendimiento detallado por asignatura con distintos niveles de desglose.",
                                size="xs", c="dimmed", style={"marginLeft": "28px", "marginTop": "2px", "marginBottom": "6px"}
                            ),
                            html.Div([
                                html.Div([
                                    dmc.Checkbox(id={"type": "check-asignatura-item", "index": 0}, label="Desglose por curso-cuatrimestre", checked=False),
                                    dmc.Text("Agrupa los resultados por curso y cuatrimestre.", size="xs", c="dimmed", style={"marginLeft": "28px"}),
                                ], style={"marginBottom": "6px"}),
                                html.Div([
                                    dmc.Checkbox(id={"type": "check-asignatura-item", "index": 1}, label="Desglose por tipología/categoría", checked=False),
                                    dmc.Text("Clasifica los resultados según el tipo de asignatura.", size="xs", c="dimmed", style={"marginLeft": "28px"}),
                                ], style={"marginBottom": "6px"}),
                                html.Div([
                                    dmc.Checkbox(id={"type": "check-asignatura-item", "index": 2}, label="Desglose por convocatoria", checked=False),
                                    dmc.Text("Compara resultados entre convocatoria ordinaria y extraordinaria.", size="xs", c="dimmed", style={"marginLeft": "28px"}),
                                ]),
                            ], style={"marginLeft": "28px"}),
                        ]),

                        dcc.Store(id="chart-selector", data=[]),
                    ]),

                    dmc.Divider(label="Tipo de visualización", labelPosition="center", mt="md"),
                    dmc.Text(
                        "Elige uno o ambos formatos para incluir en el informe.",
                        size="xs", c="dimmed", ta="center", mb="sm"
                    ),

                    dmc.CheckboxGroup(
                        id="chart-type-selector",
                        value=["graficas-lineas"],
                        children=dmc.SimpleGrid(
                            cols=2,
                            spacing="md",
                            children=[
                                dmc.Card([
                                    dmc.Checkbox(value="graficas-lineas", label="Gráficas de líneas"),
                                    dmc.Text("Evolución temporal de indicadores clave.", size="xs", c="dimmed", mt=2),
                                ], withBorder=True, shadow="sm", radius="md", p="sm"),

                                dmc.Card([
                                    dmc.Checkbox(value="tablas", label="Tabla de datos"),
                                    dmc.Text("Tabla estructurada de resultados por asignatura.", size="xs", c="dimmed", mt=2),
                                ], withBorder=True, shadow="sm", radius="md", p="sm"),
                            ]
                        ),
                    ),

                    dmc.Divider(label="Parámetros opcionales", labelPosition="center", mt="md"),
                    dmc.Text(
                        "Para análisis por asignatura. Si se indican, aparecerán como líneas de referencia en las gráficas.",
                        size="xs", c="dimmed", ta="center", mb="sm"
                    ),

                    dmc.SimpleGrid(
                        cols=2,
                        spacing="md",
                        children=[
                            dmc.NumberInput(
                                id="target-value-input",
                                label="Valor objetivo",
                                description="Tasa de éxito objetivo (%)",
                                placeholder="Ej: 75",
                                min=0, max=100, suffix="%",
                                size="sm",
                            ),
                            dmc.NumberInput(
                                id="limit-value-input",
                                label="Valor límite",
                                description="Tasa mínima aceptable (%)",
                                placeholder="Ej: 50",
                                min=0, max=100, suffix="%",
                                size="sm",
                            ),
                        ]
                    ),

                    dmc.Divider(mt="md", mb="sm"),

                    dmc.TextInput(
                        placeholder="Universidad de La Laguna",
                        label="Nombre de la institución",
                        id="institution-input",
                        description="Escribe el nombre de la institución educativa para que aparezca en el informe generado.",
                        size="sm",
                        radius="sm",
                        variant="default",
                        required=True,
                    ),
                    dmc.TextInput(
                        placeholder="Ingeniería Informática",
                        label="Nombre de la titulación",
                        id="degree-input",
                        description="Escribe el nombre de la titulación para que aparezca en el informe generado.",
                        size="sm",
                        radius="sm",
                        variant="default",
                        required=True,
                    ),
                    dmc.Center(
                        style={'margin': '10px'},
                        children = [
                        dmc.Group([
                            dmc.Button(
                                "Generar informe Word",
                                leftSection=DashIconify(icon="mdi:download"),
                                color=COLORS['primary'],
                                variant="filled",
                                id="generate-report-word-button",
                                disabled=True
                            ),
                        ]),
                    ])
                ], gap="sm", style={'padding': '20px'})
            ], shadow="xs", radius="md", style={'marginBottom': '20px', 'width': '80%'})
        ]),
            
    ])