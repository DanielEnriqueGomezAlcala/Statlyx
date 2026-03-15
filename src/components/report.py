from dash import html
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
                    dmc.Divider(label="Previsualización de gráficos", labelPosition="center", mt="md"),
                    
                    dmc.Tabs([
                        dmc.TabsList([
                            dmc.TabsTab("Desglose asignaturas", value="preview-cuatrimestre-curso"),
                            dmc.TabsTab("Desglose itinerarios", value="preview-itineraries"),
                            dmc.TabsTab("Desglose tipologías", value="preview-typologies"),
                        ], grow=True),
                        
                        # Primer gráfico de ejemplo
                        dmc.TabsPanel(
                            dmc.Stack([
                                dmc.SimpleGrid(
                                    cols={"base": 1, "sm": 2}, 
                                    spacing="md",
                                    verticalSpacing="md",
                                    children=[
                                        dmc.Card([
                                            dmc.CardSection(
                                                html.Img(
                                                    src="./assets/ejemplo_grafica_1.png",
                                                    style={"width": "100%", "height": "auto", "borderRadius": "8px"}
                                                )
                                            ),
                                            dmc.Text("Grafica de lineas", size="xs", ta="center", mt="sm")
                                        ], withBorder=True, shadow="sm", radius="md"),

                                        dmc.Card([
                                            dmc.CardSection(
                                                html.Img(
                                                    src="./assets/ejemplo_resumen_1.png",
                                                    style={"width": "100%", "height": "auto", "borderRadius": "8px"}
                                                )
                                            ),
                                            dmc.Text("Gráfico de barras resumen", size="xs", ta="center", mt="sm")
                                        ], withBorder=True, shadow="sm", radius="md"),
                                    ],
                                ),
                            ], gap="md", p="md"),
                            value="preview-cuatrimestre-curso"
                        ),

                        # Segundo gráfico de ejemplo
                        dmc.TabsPanel(
                            dmc.Stack([
                                dmc.Text("Ejemplos de visualización por Itinerario", size="sm", c="dimmed", ta="center", mt="md"),
                                
                                dmc.SimpleGrid(
                                    cols={"base": 1, "sm": 2}, 
                                    spacing="md",
                                    verticalSpacing="md",
                                    children=[
                                        dmc.Card([
                                            dmc.CardSection(
                                                html.Img(
                                                    src="./assets/ejemplo_grafica_2.png",
                                                    style={"width": "100%", "height": "auto", "borderRadius": "8px"}
                                                )
                                            ),
                                            dmc.Text("Grafica de lineas", size="xs", ta="center", mt="sm")
                                        ], withBorder=True, shadow="sm", radius="md"),

                                        dmc.Card([
                                            dmc.CardSection(
                                                html.Img(
                                                    src="./assets/ejemplo_resumen_2.png",
                                                    style={"width": "100%", "height": "auto", "borderRadius": "8px"}
                                                )
                                            ),
                                            dmc.Text("Gráfico de barras resumen", size="xs", ta="center", mt="sm")
                                        ], withBorder=True, shadow="sm", radius="md"),
                                    ],
                                ),
                            ], gap="md", p="md"),
                            value="preview-itineraries"
                        ),

                        # Tercer gráfico de ejemplo
                        dmc.TabsPanel(
                            dmc.Stack([
                                dmc.Text("Ejemplos de visualización por Tipología", size="sm", c="dimmed", ta="center", mt="md"),
                                
                                dmc.SimpleGrid(
                                    cols={"base": 1, "sm": 2}, 
                                    spacing="md",
                                    verticalSpacing="md",
                                    children=[
                                        dmc.Card([
                                            dmc.CardSection(
                                                html.Img(
                                                    src="./assets/ejemplo_grafica_3.png",
                                                    style={"width": "100%", "height": "auto", "borderRadius": "8px"}
                                                )
                                            ),
                                            dmc.Text("Grafica de lineas", size="xs", ta="center", mt="sm")
                                        ], withBorder=True, shadow="sm", radius="md"),

                                        dmc.Card([
                                            dmc.CardSection(
                                                html.Img(
                                                    src="./assets/ejemplo_resumen_3.png",
                                                    style={"width": "100%", "height": "auto", "borderRadius": "8px"}
                                                )
                                            ),
                                            dmc.Text("Gráfico de barras resumen", size="xs", ta="center", mt="sm")
                                        ], withBorder=True, shadow="sm", radius="md"),
                                    ],
                                ),
                            ], gap="md", p="md"),
                            value="preview-typologies"
                        ),
                        
                    ], value="preview-cuatrimestre-curso", color="violet", style={"marginTop": "10px", "marginBottom": "20px"}),

                    # Selector de gráficos a incluir en el informe
                    dmc.MultiSelect(
                        label="Selecciona los gráficos a incluir en el informe",
                        description="Los gráficos seleccionados se insertarán en la plantilla de Word.",
                        id="chart-selector",
                        data=[
                            {"value": "cuatrimestre-curso", "label": "Gráfico de asignaturas por cuatrimestre y curso"},
                            {"value": "itinerario", "label": "Comparativa por itinerario"},
                            {"value": "tipologia", "label": "Comparativa por tipología"}
                        ],
                        value=[],
                        clearable=True,
                        searchable=True,
                        leftSection=DashIconify(icon="mdi:chart-multiple"),
                    ),

                    dmc.Divider(style={"marginTop": "10px", "marginBottom": "10px"}),

                    # Inputs de texto para el nombre de la institución y la titulación
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