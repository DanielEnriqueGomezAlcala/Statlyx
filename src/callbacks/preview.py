"""
Callbacks de previsualización de datos.
"""

import io

import pandas as pd
import plotly.graph_objects as go
from dash import Input, Output

from charts.dinamic.table_t1_t2 import dinamic_table_t1_t2
from charts.dinamic.table_t4 import dinamic_table_t4
from charts.dinamic.table_call import dinamic_table_call

NO_MOSTRAR = {"display": "none"}
MOSTRAR: dict[str, str] = {}


def register_callbacks(app):
    """Registra los callbacks de previsualización.

    Args:
        app: Instancia de la aplicación Dash.
    """

    @app.callback(
        Output("data-table-t1t2", "figure"),
        Output("data-table-t4", "figure"),
        Output("data-table-conv", "figure"),
        Input("filtered-t1-t2", "data"),
        Input("filtered-t4", "data"),
        Input("filtered-conv", "data"),
    )
    def update_table(filtered_t1_t2, filtered_t4, filtered_conv):
        """Genera las tablas de previsualización con los datos filtrados.

        Args:
            filtered_t1_t2: DF filtrado de asignaturas.
            filtered_t4: DF filtrado de indicadores de titulación.
            filtered_conv: DF filtrado de convocatorias.
        """
        if filtered_t1_t2 is None or filtered_t4 is None or filtered_conv is None:
            return go.Figure(), go.Figure(), go.Figure()

        df_t1t2 = pd.read_json(io.StringIO(filtered_t1_t2), orient="split").head(100)
        df_t4 = pd.read_json(io.StringIO(filtered_t4), orient="split").head(100)
        df_conv = pd.read_json(io.StringIO(filtered_conv), orient="split").head(100)

        return (
            dinamic_table_t1_t2(df_t1t2),
            dinamic_table_t4(df_t4),
            dinamic_table_call(df_conv),
        )

    @app.callback(
        Output("data-table-t1t2-container", "style"),
        Output("data-table-t4-container", "style"),
        Output("data-table-conv-container", "style"),
        Input("table-selector", "value"),
    )
    def toggle_table(selected):
        """Muestra la tabla seleccionada y oculta las demás.

        Args:
            selected: Identificador de la tabla activa (t1t2, t4, conv).
        """
        if selected == "t1t2":
            return MOSTRAR, NO_MOSTRAR, NO_MOSTRAR
        if selected == "t4":
            return NO_MOSTRAR, MOSTRAR, NO_MOSTRAR
        if selected == "conv":
            return NO_MOSTRAR, NO_MOSTRAR, MOSTRAR
        return NO_MOSTRAR, NO_MOSTRAR, NO_MOSTRAR
