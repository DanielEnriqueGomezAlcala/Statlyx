"""
Callbacks para el header de la aplicación.
"""

from dash import Input, Output


def register_callbacks(app):
    """
    Registra los callbacks para el header de la aplicación.

    Args:
        app: Instancia de la aplicación Dash.
    """
    app.clientside_callback(
        """
        function(tab_value) {
            if (tab_value) {
                const sectionId = tab_value + '-section';
                const element = document.getElementById(sectionId);
                if (element) {
                    element.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            }
            return tab_value;
        }
        """,
        Output("scroll-trigger", "data"),
        Input("navigation-tabs", "value"),
    )
