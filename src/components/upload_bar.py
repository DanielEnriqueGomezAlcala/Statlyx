"""
Componente de barra de subida de archivos
"""

import dash_mantine_components as dmc
from dash import html, dcc
from dash_iconify import DashIconify
from colors.colors import COLORS


def upload_bar(upload_id, label, description=""):
    """
    Componente reutilizable de subida de archivos en formato barra horizontal desplegable.

    Args:
        upload_id: Sufijo del id.
        label: Título de la barra.
        description: Subtítulo opcional.

    Returns:
        dmc.AccordionItem: Item de la barra de subida de archivos.
    """
    label_stack = dmc.Stack(
        [
            dmc.Text(label, size="sm", fw=500),
            dmc.Text(description, size="xs", c="dimmed") if description else None,
        ],
        gap=0,
    )

    control_content = html.Div(
        [
            html.Div(
                [
                    DashIconify(
                        icon="material-symbols:upload-file-outline",
                        width=22,
                        color=COLORS["primary"],
                    ),
                    label_stack,
                ],
                style={
                    "display": "flex",
                    "alignItems": "center",
                    "gap": "12px",
                },
            ),
            html.Div(id=f"upload-status-{upload_id}"),
        ],
        style={
            "display": "flex",
            "justifyContent": "space-between",
            "alignItems": "center",
            "width": "100%",
            "paddingRight": "8px",
        },
    )

    drop_zone = dcc.Upload(
        id=f"upload-{upload_id}",
        children=html.Div(
            [
                DashIconify(
                    icon="material-symbols:cloud-upload-outline",
                    width=36,
                    color=COLORS["primary"],
                ),
                dmc.Text(
                    "Arrastra el archivo aquí o haz clic para seleccionar",
                    size="sm",
                    c="dimmed",
                    ta="center",
                ),
                dmc.Text(
                    "Formatos soportados: .xlsx, .xls",
                    size="xs",
                    c="dimmed",
                    ta="center",
                ),
            ],
            style={
                "display": "flex",
                "flexDirection": "column",
                "alignItems": "center",
                "gap": "6px",
                "padding": "20px",
            },
        ),
        style={
            "width": "100%",
            "borderWidth": "2px",
            "borderStyle": "dashed",
            "borderRadius": "8px",
            "borderColor": COLORS["light"],
            "cursor": "pointer",
            "backgroundColor": "#fafafa",
        },
        multiple=False,
    )

    return dmc.AccordionItem(
        [
            dmc.AccordionControl(control_content),
            dmc.AccordionPanel(drop_zone),
        ],
        value=upload_id,
    )
