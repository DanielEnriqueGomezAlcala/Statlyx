from dash import html
import dash_mantine_components as dmc
from dash_iconify import DashIconify


def filter_section():
    """
    Sección de filtros.

    Returns:
        html.Div: Div con el contenido de la sección de filtros.
    """
    return html.Div(
        [
            dmc.Center(
                [
                    dmc.Paper(
                        [
                            html.Div(id="filters-section"),
                            dmc.Stack(
                                [
                                    dmc.Title("Filtros", order=4),
                                    dmc.Text(
                                        "Configura los filtros para el análisis de datos",
                                        c="dimmed",
                                        size="sm",
                                    ),
                                    dmc.Stack(
                                        [
                                            dmc.YearPickerInput(
                                                id="year-picker",
                                                minDate=None,
                                                maxDate=None,
                                                leftSection=DashIconify(
                                                    icon="fa:calendar"
                                                ),
                                                type="range",
                                                label="Selecciona rango de años",
                                                placeholder="Selecciona años",
                                            ),
                                            dmc.MultiSelect(
                                                label="Selecciona tipos de asignatura",
                                                placeholder="Selecciona los tipos",
                                                id="tipo-multi-select",
                                                value=[],
                                                data=[],
                                                clearable=True,
                                                searchable=True,
                                                leftSection=DashIconify(
                                                    icon="mdi:filter"
                                                ),
                                            ),
                                            dmc.MultiSelect(
                                                label="Selecciona cursos",
                                                placeholder="Selecciona los cursos",
                                                id="curso-multi-select",
                                                value=[],
                                                data=[],
                                                clearable=True,
                                                searchable=True,
                                                leftSection=DashIconify(
                                                    icon="mdi:school"
                                                ),
                                            ),
                                        ]
                                    ),
                                    html.Div(
                                        id="filter-status", style={"marginTop": "10px"}
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
