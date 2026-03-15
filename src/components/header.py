from dash import html
import dash_mantine_components as dmc

def header():
    return (
        html.Div([
            dmc.Paper([
                dmc.Group([
                    dmc.Group([
                        html.Img(src='../assets/logo.jpeg', height='40px'),
                    ], gap="xs"),
                    dmc.Group([
                        dmc.Tabs([
                            dmc.TabsList([
                                dmc.TabsTab("Subir archivo", value="upload"),
                                dmc.TabsTab("Filtros", value="filters"),
                                dmc.TabsTab("Métricas", value="metrics"),
                                dmc.TabsTab("Generar informe", value="report"),
                            ])
                        ], id="navigation-tabs", value="upload", color="violet")
                    ], style={'marginLeft': 'auto'})
                ], justify="space-between", style={'padding': '20px'})
            ], shadow="xs", radius="md", style={'marginBottom': '20px'}),
        ])
    )