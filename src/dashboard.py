import dash
from dash import Input, Output, State, dcc, ALL, ctx
import dash_mantine_components as dmc
import base64
import io
import os
import tempfile
import pandas as pd
import plotly.graph_objects as go

# Componentes
from components.header import header
from components.upload import upload
from components.filter import filter
from components.preview import preview
from components.report import report
# Funciones
from functions.clean_data.clean_data_t1t2 import clean_data_t1t2
from functions.clean_data.clean_data_t4 import clean_data_t4
from charts.dinamic.table_t1_t2 import dinamic_table_t1_t2
from charts.dinamic.table_t4 import dinamic_table_t4
from functions.write_word.write_word import write_word

app = dash.Dash(__name__)


app.layout = dmc.MantineProvider(
    theme={"colorScheme": "light", "primaryColor": "violet"},
    children=[
        # Componentes
        header(),
        upload(),
        filter(),
        preview(),
        report(),

        # Store para guardar los datos
        dcc.Store(id='stored-t1-t2'),
        dcc.Store(id='stored-t4'),
        dcc.Store(id='filtered-t1-t2'),
        dcc.Store(id='filtered-t4'),

        # Descargar informe
        dcc.Download(id="download-report-word"),
    ]
)

######################################## Callbacks ########################################

######################################## Header ###########################################

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
    Output('navigation-tabs', 'value'),
    Input('navigation-tabs', 'value'),
)

######################################## Upload ###########################################

@app.callback(
    Output('stored-t1-t2', 'data'),
    Output('stored-t4', 'data'),
    Output('upload-status-tabla1', 'children'),
    Output('upload-status-tabla2', 'children'),
    Output('upload-status-tabla4', 'children'),
    Output('upload-status', 'children'),
    Output('year-picker', 'minDate'),
    Output('year-picker', 'maxDate'),
    Output('tipo-multi-select', 'data'),
    Output('curso-multi-select', 'data'),
    [Input('upload-tabla1', 'contents'),
     Input('upload-tabla2', 'contents'),
     Input('upload-tabla4', 'contents')],
    [State('upload-tabla1', 'filename'),
     State('upload-tabla2', 'filename'),
     State('upload-tabla4', 'filename')]
)
def handle_upload(contents_t1, contents_t2, contents_t4, filename_t1, filename_t2, filename_t4):
    from datetime import datetime as dt

    def file_badge(filename, contents):
        if contents is not None:
            return dmc.Badge(f"✓ {filename}", color="green", variant="light", size="sm")
        return dmc.Badge("Pendiente", color="gray", variant="light", size="sm")

    badge_t1 = file_badge(filename_t1, contents_t1)
    badge_t2 = file_badge(filename_t2, contents_t2)
    badge_t4 = file_badge(filename_t4, contents_t4)

    empty = [None, None, badge_t1, badge_t2, badge_t4,
             dmc.Alert("Sube los tres archivos Excel para continuar", color="gray", title="Esperando archivos"),
             None, None, [], []]

    if not all([contents_t1, contents_t2, contents_t4]):
        return empty

    try:
        def decode_excel(contents, header):
            _, content_string = contents.split(',')
            decoded = base64.b64decode(content_string)
            return pd.read_excel(io.BytesIO(decoded), header=header)

        tabla_1 = decode_excel(contents_t1, header=4)
        tabla_2 = decode_excel(contents_t2, header=4)
        tabla_4 = decode_excel(contents_t4, header=5)

        df_t1t2 = clean_data_t1t2(tabla_1, tabla_2)
        df_t4 = clean_data_t4(tabla_4)

        start_years = df_t1t2['Anio'].dropna().str.extract(r'(\d+)')[0].astype(int)
        min_year = dt(int(start_years.min()), 1, 1)
        max_year = dt(int(start_years.max()), 12, 31)

        tipos = [{'value': v, 'label': v} for v in sorted(df_t1t2['Tipologia'].dropna().unique())]
        cursos = [{'value': str(v), 'label': str(v)} for v in sorted(df_t1t2['Curso'].dropna().unique())]

        msg = dmc.Alert(
            f"Datos procesados correctamente ({len(df_t1t2)} filas)",
            color="green", title="Éxito"
        )

        return [
            df_t1t2.to_json(date_format='iso', orient='split'),
            df_t4.to_json(date_format='iso', orient='split'),
            badge_t1, badge_t2, badge_t4, msg,
            min_year, max_year, tipos, cursos
        ]

    except Exception as e:
        error = dmc.Alert(f"Error al procesar los archivos: {str(e)}", color="red", title="Error")
        return [None, None, badge_t1, badge_t2, badge_t4, error, None, None, [], []]

######################################## Filters ###########################################

@app.callback(
    [Output('filtered-t1-t2', 'data'),
     Output('filtered-t4', 'data')],
    [Input('stored-t1-t2', 'data'),
     Input('stored-t4', 'data'),
     Input('year-picker', 'value'),
     Input('tipo-multi-select', 'value'),
     Input('curso-multi-select', 'value')],
)
def update_filter(stored_t1_t2, stored_t4, year_range, tipo_multi_select, curso_multi_select):
    if stored_t1_t2 is None or stored_t4 is None:
        return None, None
    
    df_filtered_t1t2 = pd.read_json(io.StringIO(stored_t1_t2), orient='split')
    df_filtered_t4 = pd.read_json(io.StringIO(stored_t4), orient='split')

    # Filtramos tipologia
    if tipo_multi_select:
        df_filtered_t1t2 = df_filtered_t1t2[df_filtered_t1t2['Tipologia'].isin(tipo_multi_select)]

    # Filtramos cursos (Curso es int en el df, pero el MultiSelect envía strings)
    if curso_multi_select:
        df_filtered_t1t2 = df_filtered_t1t2[df_filtered_t1t2['Curso'].astype(str).isin(curso_multi_select)]

    # Filtramos años
    if year_range and isinstance(year_range, list) and len(year_range) == 2 and year_range[0] and year_range[1]:
        start_year = pd.to_datetime(year_range[0]).year
        end_year = pd.to_datetime(year_range[1]).year

        df_filtered_t1t2 = df_filtered_t1t2.dropna(subset=['Anio'])
        df_filtered_t1t2["start_year"] = df_filtered_t1t2["Anio"].str.extract(r'(\d{4})')[0].astype(int)
        df_filtered_t1t2 = df_filtered_t1t2[
            (df_filtered_t1t2["start_year"] >= start_year) &
            (df_filtered_t1t2["start_year"] <= end_year)
        ]

        df_filtered_t4 = df_filtered_t4.dropna(subset=['Anio'])
        df_filtered_t4["start_year"] = df_filtered_t4["Anio"].str.extract(r'(\d{4})')[0].astype(int)
        df_filtered_t4 = df_filtered_t4[
            (df_filtered_t4["start_year"] >= start_year) &
            (df_filtered_t4["start_year"] <= end_year)
        ]
    
    return [
        df_filtered_t1t2.to_json(date_format='iso', orient='split'),
        df_filtered_t4.to_json(date_format='iso', orient='split'),
    ]

######################################## Preview ###########################################

@app.callback(
    Output('data-table-t1t2', 'figure'),
    Output('data-table-t4', 'figure'),
    Input('filtered-t1-t2', 'data'),
    Input('filtered-t4', 'data')
)
def update_table(filtered_t1_t2, filtered_t4):
    if filtered_t1_t2 is None or filtered_t4 is None:
        return go.Figure(), go.Figure()
    
    df_filtered_t1t2 = pd.read_json(io.StringIO(filtered_t1_t2), orient='split')
    df_filtered_t4 = pd.read_json(io.StringIO(filtered_t4), orient='split')
    
    df_filtered_t1t2 = df_filtered_t1t2.head(100)
    df_filtered_t4 = df_filtered_t4.head(100)
    return dinamic_table_t1_t2(df_filtered_t1t2), dinamic_table_t4(df_filtered_t4)

@app.callback(
    Output('data-table-t1t2-container', 'style'),
    Output('data-table-t4-container', 'style'),
    Input('table-selector', 'value')
)
def toggle_table(selected):
    if selected == 't4':
        return {"display": "none"}, {}
    return {}, {"display": "none"}

######################################## Report ###########################################

@app.callback(
    Output("check-asignatura", "checked"),
    Output("check-asignatura", "indeterminate"),
    Output({"type": "check-asignatura-item", "index": ALL}, "checked"),
    Input("check-asignatura", "checked"),
    Input({"type": "check-asignatura-item", "index": ALL}, "checked"),
    prevent_initial_call=True
)
def update_asignatura_checkbox(all_checked, checked_states):
    if ctx.triggered_id == "check-asignatura":
        checked_states = [all_checked] * len(checked_states)
    all_checked_states = all(checked_states)
    indeterminate = any(checked_states) and not all_checked_states
    return all_checked_states, indeterminate, checked_states

@app.callback(
    Output("chart-selector", "data"),
    Input("check-titulacion", "checked"),
    Input({"type": "check-asignatura-item", "index": ALL}, "checked"),
)
def update_chart_selector(titulacion_checked, asignatura_items_checked):
    sub_item_values = ["desglose-curso", "desglose-tipologia", "desglose-convocatoria"]
    selected = []
    if titulacion_checked:
        selected.append("analisis-titulacion")
    for i, checked in enumerate(asignatura_items_checked):
        if checked:
            selected.append(sub_item_values[i])
    return selected

# Callback para habilitar/deshabilitar botones según los inputs

@app.callback(
    [Output('generate-report-word-button', 'disabled')],
    [Input('institution-input', 'value'),
     Input('degree-input', 'value'),
     Input('filtered-t1-t2', 'data'),
     Input('filtered-t4', 'data')]
)
def toggle_report_buttons(institucion, titulacion, filtered_t1_t2, filtered_t4):
    disabled = not (institucion and titulacion and filtered_t1_t2 and filtered_t4)
    return [disabled]

@app.callback(
    Output('download-report-word', 'data'),
    Input('generate-report-word-button', 'n_clicks'),
    [State('filtered-t1-t2', 'data'),
     State('filtered-t4', 'data'),
     State('institution-input', 'value'),
     State('degree-input', 'value'),
     State('chart-selector', 'data'),
     State('chart-type-selector', 'value'),
     State('target-value-input', 'value'),
     State('limit-value-input', 'value')],
    prevent_initial_call=True
)
def generate_report_word(_n_clicks, filtered_t1_t2, filtered_t4, institucion, titulacion, chart_selector, chart_types, target_value, limit_value):
    df = pd.read_json(io.StringIO(filtered_t1_t2), orient='split')
    df_t4 = pd.read_json(io.StringIO(filtered_t4), orient='split')
    df.to_csv('df.csv', sep=';', index=False)

    ruta_plantilla = os.path.join(os.path.dirname(__file__), '..', 'templates', 'InformePruebaV6.docx')

    with tempfile.TemporaryDirectory() as directorio:
        ruta_guardado = write_word(df, df_t4, ruta_plantilla, directorio, chart_selector, chart_types, institucion, titulacion, target_value, limit_value)
        return dcc.send_file(ruta_guardado)

if __name__ == '__main__':
    app.run(debug=True, port=8050)