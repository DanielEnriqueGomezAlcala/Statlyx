import dash
from dash import dcc, html, Input, Output, State
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import plotly.graph_objects as go
import pandas as pd
import tempfile
import base64
import io
import os
from datetime import datetime


from graphs.dinamic.table import crear_tabla_datos
from graphs.dinamic.line import crear_grafica_lineas


from functions.write_word import rellenar_plantilla

# Inicializar la app
app = dash.Dash(__name__)

# Colores personalizados
COLORS = {
    'primary': '#5C068C',
    'secondary': '#7D3C98',
    'light': '#D5D8DC',
    'background': '#f8f9fa'
}

# Layout del dashboard
app.layout = dmc.MantineProvider(
    theme={"colorScheme": "light", "primaryColor": "violet"},
    children=[
        dmc.Container([
            # Header
            dmc.Paper([
                dmc.Group([
                    dmc.Group([
                        html.Img(src='/assets/logo.jpeg', height='40px'),
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
            
            # Subir archivo

            dmc.Center([
                dmc.Paper([
                    html.Div(id="upload-section"),
                    dmc.Stack([
                        dmc.Title("Subir archivo", order=4),
                        dmc.Text("Sube un archivo CSV", c="dimmed", size="sm"),
                        dcc.Upload(
                            id='upload-data',
                            children=dmc.Stack([
                                DashIconify(icon="material-symbols:upload", width=50, color=COLORS['primary']),
                                dmc.Button(
                                    "Subir archivo",
                                    leftSection=DashIconify(icon="material-symbols:upload"),
                                    color=COLORS['primary'],
                                    variant="filled"
                                ),
                                dmc.Text("Arrastra y suelta el archivo aquí o haz clic", size="xs", c="dimmed")
                            ], align="center", gap="xs"),
                            style={
                                'width': '100%',
                                'height': '180px',
                                'borderWidth': '2px',
                                'borderStyle': 'dashed',
                                'borderRadius': '10px',
                                'borderColor': COLORS['light'],
                                'textAlign': 'center',
                                'display': 'flex',
                                'alignItems': 'center',
                                'justifyContent': 'center',
                                'cursor': 'pointer'
                            },
                            multiple=False
                        ),
                        html.Div(id='upload-status', style={'marginTop': '10px'})
                    ], gap="sm", style={'padding': '20px'})
                ], shadow="xs", radius="md", style={'marginBottom': '20px', 'width': '80%'})
            ]),

            # Filtros

            dmc.Center([
                dmc.Paper([
                    html.Div(id="filters-section"),
                    dmc.Stack([
                        dmc.Title("Filtros", order=4),
                        dmc.Text("Configura los filtros para el análisis de datos", c="dimmed", size="sm"),

                        dmc.Stack([
                            dmc.YearPickerInput(
                                id="year-picker",
                                minDate=None,
                                maxDate=None,
                                leftSection=DashIconify(icon="fa:calendar"),
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
                                leftSection=DashIconify(icon="mdi:filter"),
                            ),

                            dmc.MultiSelect(
                                label="Selecciona asignaturas",
                                placeholder="Selecciona las asignaturas",
                                id="asignatura-multi-select",
                                value=[],
                                data=[],
                                clearable=True,
                                searchable=True,
                                leftSection=DashIconify(icon="mdi:book-open-variant"),
                            ),

                            dmc.MultiSelect(
                                label="Selecciona cursos",
                                placeholder="Selecciona los cursos",
                                id="curso-multi-select",
                                value=[],
                                data=[],
                                clearable=True,
                                searchable=True,
                                leftSection=DashIconify(icon="mdi:school"),
                            ),
                        ]),
                        
                        html.Div(id='filter-status', style={'marginTop': '10px'})
                    ], gap="sm", style={'padding': '20px'})
                ], shadow="xs", radius="md", style={'marginBottom': '20px', 'width': '80%'})
            ]),
            
            # Metricas y visualizaciones
            dmc.Center([
                dmc.Paper([
                    html.Div(id="metrics-section"),
                    dmc.Stack([
                        dmc.Title("Metricas", order=4),
                        dmc.Tabs([
                                dmc.TabsList(
                                    [
                                        dmc.TabsTab("Tabla de datos", value="table"),
                                        dmc.TabsTab("Gráfico de lineas", value="general"),
                                    ]
                                ),
                                dmc.TabsPanel(
                                    dcc.Graph(id='data-table-graph'), value="table"
                                ),
                                dmc.TabsPanel(
                                    dmc.Stack([
                                        dmc.Select(
                                            label="Selecciona eje X para el gráfico",
                                            placeholder="Selecciona el eje X",
                                            id="eje-x-select",
                                            value="Anio",
                                            data=[
                                                {'value': 'Anio', 'label': 'Año'},
                                                {'value': 'Curso', 'label': 'Curso'},
                                                {'value': 'Cuatrimestre', 'label': 'Cuatrimestre'},
                                                {'value': 'Asignatura', 'label': 'Asignatura'},
                                            ],
                                            clearable=False,
                                            searchable=False,
                                            leftSection=DashIconify(icon="mdi:chart-line"),
                                            style={'width': '300px'}
                                        ),
                                        dcc.Graph(id='data-line-graph')
                                    ], gap="md")
                                    , value="general"
                                ),
                            ],
                            color=COLORS['primary'],
                            orientation="horizontal", 
                            variant="pills",
                            value="table"
                        )
                        
                    ], gap="sm", style={'padding': '20px'})
                ], shadow="xs", radius="md", style={'marginBottom': '20px', 'width': '80%'})
            ]),

            # Generar informe
            dmc.Center([
                dmc.Paper([
                    html.Div(id="report-section"),
                    dmc.Stack([
                        dmc.Title("Generar informe", order=4),
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
            

            # Download component para descargar datos
            dcc.Download(id="download-report-word"),
            
            
            # Store para guardar los datos
            dcc.Store(id='stored-data'),
            dcc.Store(id='filtered-data'),
            dcc.Store(id='scroll-trigger')
            
        ], fluid=True, style={'backgroundColor': COLORS['background'], 'padding': '20px', 'minHeight': '100vh'}),
    ]
)

######################################## Callbacks ########################################

# Clientside callback para hacer scroll a la sección seleccionada
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
    Input('navigation-tabs', 'value')
)

# Callback para manejar la carga de archivos
@app.callback(
    [Output('stored-data', 'data'),
     Output('upload-status', 'children'),
     Output('year-picker', 'minDate'),
     Output('year-picker', 'maxDate'),
     Output('tipo-multi-select', 'data'),
     Output('asignatura-multi-select', 'data'),
     Output('curso-multi-select', 'data')],
    Input('upload-data', 'contents'),
    State('upload-data', 'filename')
)
def handle_upload(contents, filename):
    if contents is None:
        # No hay archivo subido
        return None, dmc.Alert(
            "Por favor, sube un archivo CSV para comenzar", 
            color="gray", 
            title="Sin archivo"
        ), None, None, [], [], []
    
    # Procesar archivo subido
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        
        # Extraer años del dataframe si existe la columna 'Anio'
        min_year = None
        max_year = None
        
        if 'Anio' in df.columns:
            df[["start_year", "end_year"]] = df["Anio"].str.split("-", expand=True).astype(int)
            min_year_int = int(df["start_year"].min())
            max_year_int = int(df["end_year"].max())
            
            # El year picker espera objetos datetime
            min_year = datetime(min_year_int, 1, 1)
            max_year = datetime(max_year_int, 12, 31)
        
        # Extraer tipos únicos si existe la columna 'Tipo'
        tipos_data = []
        if 'Tipo' in df.columns:
            tipos_unicos = sorted(df['Tipo'].dropna().unique())
            tipos_data = [{'value': tipo, 'label': tipo} for tipo in tipos_unicos]
        
        # Extraer asignaturas únicas si existe la columna 'Asignatura'
        asignaturas_data = []
        if 'Asignatura' in df.columns:
            asignaturas_unicas = sorted(df['Asignatura'].dropna().unique())
            asignaturas_data = [{'value': asig, 'label': asig} for asig in asignaturas_unicas]
        
        # Extraer cursos únicos si existe la columna 'Curso'
        cursos_data = []
        if 'Curso' in df.columns:
            cursos_unicos = sorted(df['Curso'].dropna().unique())
            cursos_data = [{'value': curso, 'label': curso} for curso in cursos_unicos]
        
        status = dmc.Alert(
            f"Archivo '{filename}' cargado exitosamente ({len(df)} filas)", 
            color="green", 
            title="Éxito"
        )
    except Exception as e:
        return None, dmc.Alert(f"Error al cargar el archivo: {str(e)}", color="red", title="Error"), None, None, [], [], []
    
    return df.to_json(date_format='iso', orient='split'), status, min_year, max_year, tipos_data, asignaturas_data, cursos_data

# Callback para aplicar filtros a los datos
@app.callback(
    Output('filtered-data', 'data'),
    [Input('stored-data', 'data'),
     Input('year-picker', 'value'),
     Input('tipo-multi-select', 'value'),
     Input('asignatura-multi-select', 'value'),
     Input('curso-multi-select', 'value')]
)
def update_filter(stored_data, year_range, tipos, asignaturas, cursos):
    if stored_data is None:
        return None
    
    df = pd.read_json(io.StringIO(stored_data), orient='split')
    
    # Aplicar filtros si existen
    df_filtered = df.copy()
    
    # Validar que year_range sea una lista válida con dos elementos
    if year_range and isinstance(year_range, list) and len(year_range) == 2 and year_range[0] and year_range[1]:
        df_filtered[["start_year", "end_year"]] = df_filtered["Anio"].str.split("-", expand=True).astype(int)
        # Parsear las fechas del YearPickerInput
        start_year = pd.to_datetime(year_range[0]).year
        end_year = pd.to_datetime(year_range[1]).year
        df_filtered = df_filtered[
            (df_filtered["start_year"] >= start_year) & 
            (df_filtered["end_year"] <= end_year)
        ]
    
    if tipos and len(tipos) > 0:
        df_filtered = df_filtered[df_filtered['Tipo'].isin(tipos)]
    
    if asignaturas and len(asignaturas) > 0:
        df_filtered = df_filtered[df_filtered['Asignatura'].isin(asignaturas)]
    
    if cursos and len(cursos) > 0:
        df_filtered = df_filtered[df_filtered['Curso'].isin(cursos)]
    
    return df_filtered.to_json(date_format='iso', orient='split')

@app.callback(
    Output('data-table-graph', 'figure'),
    Input('filtered-data', 'data')
)
def update_table(filtered_data):
    if filtered_data is None:
        return go.Figure()
    
    df_filtered = pd.read_json(io.StringIO(filtered_data), orient='split')
    df_filtered = df_filtered.head(100)  # Limitar a 100 filas para la tabla

    # Crear la tabla con los datos filtrados
    return crear_tabla_datos(df_filtered)

@app.callback(
    Output('data-line-graph', 'figure'),
    [Input('filtered-data', 'data'),
     Input('eje-x-select', 'value')]
)
def update_line_chart(filtered_data, eje_x):
    if filtered_data is None:
        return go.Figure()
    
    df_filtered = pd.read_json(io.StringIO(filtered_data), orient='split')
    
    # Crear el gráfico de líneas con el eje X seleccionado
    return crear_grafica_lineas(df_filtered, eje_x)

# Callback para habilitar/deshabilitar botones según los inputs
@app.callback(
    [Output('generate-report-word-button', 'disabled')],
    [Input('institution-input', 'value'),
     Input('degree-input', 'value'),
     Input('filtered-data', 'data')]
)
def toggle_report_buttons(institucion, titulacion, filtered_data):
    # Deshabilitar si falta institución, titulación o no hay datos
    disabled = not (institucion and titulacion and filtered_data)
    return [disabled]

@app.callback(
    Output("download-report-word", "data"),
    Input("generate-report-word-button", "n_clicks"),
    [State('filtered-data', 'data'),
     State('institution-input', 'value'),
     State('degree-input', 'value')],
    prevent_initial_call=True
)
def generate_report(n_clicks, filtered_data, institucion, titulacion):
    if not filtered_data or not institucion or not titulacion:
        return dash.no_update
    
    df = pd.read_json(io.StringIO(filtered_data), orient='split')
    ruta_plantilla = os.path.join(os.path.dirname(__file__), '..', 'templates', 'InformePrueba.docx')

    with tempfile.TemporaryDirectory() as tmpdir:
        
    
    # Generar el documento Word
    buffer = rellenar_plantilla(df, ruta_plantilla, institucion=institucion, titulacion=titulacion)
    
    # Retornar el documento Word para descarga
    return dcc.send_bytes(buffer.getvalue(), f"informe_{institucion or 'dashboard'}_{datetime.now().strftime('%Y%m%d')}.docx")

if __name__ == '__main__':
    app.run(debug=True, port=8050)