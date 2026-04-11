import dash
from dash import dcc
import dash_mantine_components as dmc

# Componentes
from components.header import header
from components.upload import upload
from components.filter import filter_section
from components.preview import preview
from components.report import report

# Callbacks
import callbacks.header as header_callbacks
import callbacks.upload as upload_callbacks
import callbacks.filter as filter_callbacks
import callbacks.preview as preview_callbacks
import callbacks.report as report_callbacks

app = dash.Dash(__name__)

app.layout = dmc.MantineProvider(
    theme={"colorScheme": "light", "primaryColor": "violet"},
    children=[
        header(),
        upload(),
        filter_section(),
        preview(),
        report(),

        # Estado global de la aplicación
        dcc.Store(id='stored-t1-t2'),
        dcc.Store(id='stored-t4'),
        dcc.Store(id='stored-conv'),
        dcc.Store(id='stored-adicional'),
        dcc.Store(id='filtered-t1-t2'),
        dcc.Store(id='filtered-t4'),
        dcc.Store(id='filtered-conv'),
        dcc.Store(id='chart-selector', data=[]),
        dcc.Store(id='scroll-trigger'),

        # Descargas
        dcc.Download(id="download-report-word"),
        dcc.Download(id="download-report-pptx"),
    ]
)

header_callbacks.register_callbacks(app)
upload_callbacks.register_callbacks(app)
filter_callbacks.register_callbacks(app)
preview_callbacks.register_callbacks(app)
report_callbacks.register_callbacks(app)

if __name__ == '__main__':
    app.run(debug=True, port=8050)
