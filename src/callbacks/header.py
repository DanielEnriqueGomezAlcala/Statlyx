from dash import Input, Output


def register_callbacks(app):
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
        Output('scroll-trigger', 'data'),
        Input('navigation-tabs', 'value'),
    )
