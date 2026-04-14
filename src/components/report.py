"""
Componente de la sección de generación de informes
"""

from dash import html
import dash_mantine_components as dmc
from colors.colors import COLORS
from dash_iconify import DashIconify

INDENT_STYLE = {"marginLeft": "28px"}

SUBITEMS = [
    (
        0,
        "Desglose por curso-cuatrimestre",
        "Agrupa los resultados por curso y cuatrimestre.",
    ),
    (
        1,
        "Desglose por tipología",
        "Clasifica los resultados según el tipo de asignatura.",
    ),
    (
        2,
        "Desglose por menciones/itinerarios",
        "Clasifica los resultados según la mención o itinerario de la asignatura.",
    ),
    (
        3,
        "Desglose por convocatoria",
        "Compara resultados entre convocatoria ordinaria y extraordinaria.",
    ),
]


def checkbox_item(idx, label, description, mb="6px"):
    """
    Item de checkbox para el desglose por asignatura.

    Args:
        idx: Índice del item.
        label: Label del item.
        description: Descripción del item.
        mb: Margen bottom del item.

    Returns:
        html.Div: Div con el contenido del item de checkbox.
    """
    return html.Div(
        [
            dmc.Checkbox(
                id={"type": "check-asignatura-item", "index": idx},
                label=label,
                checked=False,
                disabled=True,
                color=COLORS["primary"],
            ),
            dmc.Text(description, size="xs", c="dimmed", style=INDENT_STYLE),
        ],
        style={"marginBottom": mb},
    )


def report():
    """
    Sección de generación de informe.

    Returns:
        html.Div: Div con el contenido de la sección de generación de informe.
    """
    return html.Div(
        [
            dmc.Center(
                [
                    dmc.Paper(
                        [
                            html.Div(id="report-section"),
                            dmc.Stack(
                                [
                                    dmc.Title("Generar informe", order=4),
                                    dmc.Divider(
                                        label="Generación de texto con IA",
                                        labelPosition="center",
                                        mt="md",
                                    ),
                                    dmc.Text(
                                        "Selecciona si deseas incluir análisis de texto generado por IA en el informe.",
                                        size="xs",
                                        c="dimmed",
                                        ta="center",
                                        mb="sm",
                                    ),
                                    dmc.Center(
                                        dmc.SegmentedControl(
                                            id="llm-mode-selector",
                                            value="sin-razonamiento",
                                            color=COLORS["primary"],
                                            data=[
                                                {"value": "no", "label": "No"},
                                                {
                                                    "value": "sin-razonamiento",
                                                    "label": "Sin razonamiento",
                                                },
                                                {
                                                    "value": "con-razonamiento",
                                                    "label": "Con razonamiento",
                                                },
                                            ],
                                        ),
                                    ),
                                    dmc.Center(
                                        dmc.Text(
                                            id="llm-mode-description",
                                            size="xs",
                                            c="dimmed",
                                            mt=4,
                                        )
                                    ),
                                    dmc.Divider(
                                        label="Contenido del informe",
                                        labelPosition="center",
                                        mt="md",
                                    ),
                                    dmc.Text(
                                        "Selecciona las secciones que deseas incluir en el informe.",
                                        size="xs",
                                        c="dimmed",
                                        ta="center",
                                        mb="sm",
                                    ),
                                    html.Div(
                                        [
                                            # Análisis por titulación
                                            html.Div(
                                                [
                                                    dmc.Checkbox(
                                                        id="check-titulacion",
                                                        label="Análisis por titulación",
                                                        checked=False,
                                                        disabled=True,
                                                        color=COLORS["primary"],
                                                    ),
                                                    dmc.Text(
                                                        "Evolución de las tasas de rendimiento y éxito a nivel global de la titulación.",
                                                        size="xs",
                                                        c="dimmed",
                                                        style={
                                                            **INDENT_STYLE,
                                                            "marginTop": "2px",
                                                        },
                                                    ),
                                                ],
                                                style={"marginBottom": "12px"},
                                            ),
                                            # Análisis por asignatura
                                            html.Div(
                                                [
                                                    dmc.Checkbox(
                                                        id="check-asignatura",
                                                        label="Análisis por asignatura",
                                                        checked=False,
                                                        indeterminate=False,
                                                        disabled=True,
                                                        color=COLORS["primary"],
                                                    ),
                                                    dmc.Text(
                                                        "Rendimiento detallado por asignatura con distintos niveles de desglose.",
                                                        size="xs",
                                                        c="dimmed",
                                                        style={
                                                            **INDENT_STYLE,
                                                            "marginTop": "2px",
                                                            "marginBottom": "6px",
                                                        },
                                                    ),
                                                    html.Div(
                                                        [
                                                            checkbox_item(
                                                                idx, label, desc
                                                            )
                                                            for idx, label, desc in SUBITEMS
                                                        ],
                                                        style=INDENT_STYLE,
                                                    ),
                                                ]
                                            ),
                                        ]
                                    ),
                                    dmc.Divider(
                                        label="Tipo de visualización",
                                        labelPosition="center",
                                        mt="md",
                                    ),
                                    dmc.Text(
                                        "Elige uno o ambos formatos para incluir en el informe.",
                                        size="xs",
                                        c="dimmed",
                                        ta="center",
                                        mb="sm",
                                    ),
                                    dmc.CheckboxGroup(
                                        id="chart-type-selector",
                                        value=["graficas-lineas", "graficas-tablas"],
                                        children=dmc.SimpleGrid(
                                            cols=2,
                                            spacing="md",
                                            children=[
                                                dmc.Card(
                                                    [
                                                        dmc.Checkbox(
                                                            value="graficas-lineas",
                                                            label="Gráficas de líneas",
                                                            color=COLORS["primary"],
                                                        ),
                                                        dmc.Text(
                                                            "Evolución temporal de indicadores clave.",
                                                            size="xs",
                                                            c="dimmed",
                                                            mt=2,
                                                        ),
                                                        dmc.Image(
                                                            src="assets/line_chart_example.png",
                                                            alt="Gráfica de líneas",
                                                            w="80%",
                                                        ),
                                                    ],
                                                    withBorder=True,
                                                    shadow="sm",
                                                    radius="md",
                                                    p="sm",
                                                ),
                                                dmc.Card(
                                                    [
                                                        dmc.Checkbox(
                                                            value="graficas-tablas",
                                                            label="Gráficas de tablas",
                                                            color=COLORS["primary"],
                                                        ),
                                                        dmc.Text(
                                                            "Tabla estructurada de resultados por asignatura.",
                                                            size="xs",
                                                            c="dimmed",
                                                            mt=2,
                                                        ),
                                                        dmc.Center(
                                                            dmc.Image(
                                                                src="assets/table_chart_example.png",
                                                                alt="Gráfica de tabla",
                                                            ),
                                                        ),
                                                    ],
                                                    withBorder=True,
                                                    shadow="sm",
                                                    radius="md",
                                                    p="sm",
                                                ),
                                            ],
                                        ),
                                    ),
                                    dmc.Divider(
                                        label="Parámetros opcionales",
                                        labelPosition="center",
                                        mt="md",
                                    ),
                                    dmc.Text(
                                        "Para análisis por asignatura. Si se indican, aparecerán como líneas de referencia en las gráficas.",
                                        size="xs",
                                        c="dimmed",
                                        ta="center",
                                        mb="sm",
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
                                                min=0,
                                                max=100,
                                                suffix="%",
                                                size="sm",
                                            ),
                                            dmc.NumberInput(
                                                id="limit-value-input",
                                                label="Valor límite",
                                                description="Tasa mínima aceptable (%)",
                                                placeholder="Ej: 50",
                                                min=0,
                                                max=100,
                                                suffix="%",
                                                size="sm",
                                            ),
                                        ],
                                    ),
                                    dmc.Divider(mt="md", mb="sm"),
                                    dmc.TextInput(
                                        id="institution-input",
                                        label="Nombre de la institución",
                                        placeholder="Universidad de La Laguna",
                                        description="Aparecerá en el encabezado del informe generado.",
                                        size="sm",
                                        radius="sm",
                                        variant="default",
                                        required=True,
                                    ),
                                    dmc.TextInput(
                                        id="degree-input",
                                        label="Nombre de la titulación",
                                        placeholder="Ingeniería Informática",
                                        description="Aparecerá en el encabezado del informe generado.",
                                        size="sm",
                                        radius="sm",
                                        variant="default",
                                        required=True,
                                    ),
                                    dmc.Center(
                                        style={"margin": "10px"},
                                        children=dmc.Group(
                                            [
                                                dmc.Button(
                                                    "Generar informe Word",
                                                    id="generate-report-word-button",
                                                    leftSection=DashIconify(
                                                        icon="mdi:download"
                                                    ),
                                                    color=COLORS["primary"],
                                                    variant="filled",
                                                    disabled=True,
                                                ),
                                                dmc.Button(
                                                    "Generar presentación PowerPoint",
                                                    id="generate-report-pptx-button",
                                                    leftSection=DashIconify(
                                                        icon="mdi:presentation"
                                                    ),
                                                    color=COLORS["primary"],
                                                    variant="filled",
                                                    disabled=True,
                                                ),
                                            ]
                                        ),
                                    ),
                                    html.Div(
                                        id="report-generation-status",
                                        style={"marginTop": "8px"},
                                    ),
                                ],
                                gap="sm",
                                style={"padding": "20px"},
                            ),
                        ],
                        shadow="xs",
                        radius="md",
                        style={"marginBottom": "20px", "width": "80%"},
                    ),
                ]
            ),
        ]
    )
