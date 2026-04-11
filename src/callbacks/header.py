from dash import Input, Output


def register_callbacks(app):
    """
    Scrolls a la sección correspondiente cuando se selecciona un tab en el header.
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
