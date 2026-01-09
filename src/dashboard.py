import dash
from dash import dcc, html, Input, Output, State, ctx
import pandas as pd
from pathlib import Path
import plotly.graph_objects as go
from datetime import datetime

# Importar funciones de gráficos interactivos
from functions.charts.interactive import (
    crear_lineas_rendimiento,
    crear_comparacion_media,
    crear_tabla_resumen,
    crear_brecha_genero
)

# Inicializar la aplicación Dash
app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "Dashboard Rendimiento Académico"


def obtener_universidades_disponibles():
    """Obtiene la lista de universidades disponibles"""
    base_path = Path(__file__).parent.parent / "data" / "clean-data"
    universidades = []
    
    excluir = {
        '???', 'Fuente:_Sistema_Integrado_de_Información_Universitaria_(SIIU).',
        'Notas:', 'Todas_las_universidades', 
        'Universidades_Privadas', 'Universidades_Públicas',
        'Universidades_Privadas_No_Presenciales', 
        'Universidades_Privadas_Presenciales',
        'Universidades_Públicas_No_Presenciales',
        'Universidades_Públicas_Presenciales',
        '.DS_Store'
    }
    
    for item in base_path.iterdir():
        if item.is_dir() and not item.name.startswith('.') and not item.name.startswith('~'):
            if item.name not in excluir:
                csv_file = item / "Tabla.csv"
                if csv_file.exists():
                    nombre_legible = item.name.replace('_', ' ')
                    universidades.append({'label': nombre_legible, 'value': item.name})
    
    return sorted(universidades, key=lambda x: x['label'])


def cargar_datos_universidad(universidad_folder):
    """Carga los datos de una universidad"""
    base_path = Path(__file__).parent.parent / "data" / "clean-data" / universidad_folder / "Tabla.csv"
    
    try:
        df = pd.read_csv(base_path, sep=';', encoding='utf-8')
        df['Valor'] = pd.to_numeric(df['Valor'].replace('???', pd.NA), errors='coerce')
        return df
    except Exception as e:
        print(f"Error al cargar datos: {e}")
        return pd.DataFrame()


def obtener_carreras_de_universidad(universidad_folder):
    """Obtiene las carreras disponibles de una universidad"""
    df = cargar_datos_universidad(universidad_folder)
    if df.empty:
        return []
    
    carreras = df['Carrera'].unique()
    carreras_filtradas = []
    
    for c in carreras:
        if (c != universidad_folder.replace('_', ' ') and 
            c != 'Todos los ámbitos' and 
            not c.startswith('Total') and
            c != '???'):
            carreras_filtradas.append({'label': c, 'value': c})
    
    return sorted(carreras_filtradas, key=lambda x: x['label'])


# Layout de la aplicación
app.layout = html.Div([
    # Header
    html.Div([
        html.H1("Dashboard de Rendimiento Académico", 
               style={'margin': '0', 'color': 'white'}),
        html.P("Análisis de Rendimiento Universitario",
              style={'margin': '10px 0 0 0', 'color': '#e0e0e0'})
    ], style={'padding': '30px', 'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
             'borderRadius': '10px', 'marginBottom': '30px', 'textAlign': 'center'}),
    
    # Controles
    html.Div([
        html.Div([
            html.Label("Universidad:", style={'fontWeight': 'bold', 'marginBottom': '8px', 'display': 'block'}),
            dcc.Dropdown(
                id='dropdown-universidad',
                options=obtener_universidades_disponibles(),
                placeholder="Seleccione una universidad..."
            )
        ], style={'flex': '1', 'marginRight': '15px'}),
        
        html.Div([
            html.Label("Carrera:", style={'fontWeight': 'bold', 'marginBottom': '8px', 'display': 'block'}),
            dcc.Dropdown(
                id='dropdown-carrera',
                placeholder="Primero seleccione una universidad..."
            )
        ], style={'flex': '1'})
    ], style={'display': 'flex', 'marginBottom': '30px', 'padding': '20px', 
             'background': 'white', 'borderRadius': '10px', 'boxShadow': '0 2px 8px rgba(0,0,0,0.1)'}),
    
    # Mensaje inicial
    html.Div(id='mensaje-inicial', children=[
        html.Div("Seleccione una universidad y carrera para visualizar los gráficos", 
                style={'fontSize': '1.2em', 'color': '#666', 'textAlign': 'center', 'padding': '40px'})
    ]),
    
    # Gráficos
    html.Div(id='graficos-container', style={'display': 'none'}, children=[
        # Gráfico 1: Evolución del Rendimiento
        html.Div([
            html.H3("Evolución del Rendimiento por Género", 
                   style={'color': '#667eea', 'borderBottom': '3px solid #667eea', 'paddingBottom': '10px'}),
            dcc.Graph(id='graph-rendimiento')
        ], style={'background': 'white', 'padding': '20px', 'borderRadius': '10px', 
                 'boxShadow': '0 2px 8px rgba(0,0,0,0.1)', 'marginBottom': '20px'}),
        
        # Gráfico 2: Comparación con Media
        html.Div([
            html.H3("Comparación con Media Universitaria", 
                   style={'color': '#667eea', 'borderBottom': '3px solid #667eea', 'paddingBottom': '10px'}),
            dcc.Graph(id='graph-comparacion')
        ], style={'background': 'white', 'padding': '20px', 'borderRadius': '10px', 
                 'boxShadow': '0 2px 8px rgba(0,0,0,0.1)', 'marginBottom': '20px'}),
        
        # Gráfico 3: Tabla Resumen
        html.Div([
            html.H3("Resumen de Indicadores", 
                   style={'color': '#667eea', 'borderBottom': '3px solid #667eea', 'paddingBottom': '10px'}),
            dcc.Graph(id='graph-tabla')
        ], style={'background': 'white', 'padding': '20px', 'borderRadius': '10px', 
                 'boxShadow': '0 2px 8px rgba(0,0,0,0.1)', 'marginBottom': '20px'}),
        
        # Gráfico 4: Brecha de Género
        html.Div([
            html.H3("Brecha de Género", 
                   style={'color': '#667eea', 'borderBottom': '3px solid #667eea', 'paddingBottom': '10px'}),
            dcc.Graph(id='graph-brecha')
        ], style={'background': 'white', 'padding': '20px', 'borderRadius': '10px', 
                 'boxShadow': '0 2px 8px rgba(0,0,0,0.1)', 'marginBottom': '30px'}),
        
        # Botones de generar documentos
        html.Div([
            html.Div([
                html.Button(
                    "Generar Informe PDF",
                    id='btn-generar-informe',
                    n_clicks=0,
                    style={
                        'fontSize': '1.1em',
                        'padding': '15px 40px',
                        'background': '#667eea',
                        'color': 'white',
                        'border': 'none',
                        'borderRadius': '8px',
                        'cursor': 'pointer',
                        'fontWeight': 'bold',
                        'marginRight': '15px'
                    }
                ),
                html.Button(
                    "Generar Presentación PDF",
                    id='btn-generar-presentacion',
                    n_clicks=0,
                    style={
                        'fontSize': '1.1em',
                        'padding': '15px 40px',
                        'background': '#764ba2',
                        'color': 'white',
                        'border': 'none',
                        'borderRadius': '8px',
                        'cursor': 'pointer',
                        'fontWeight': 'bold'
                    }
                )
            ], style={'display': 'flex', 'justifyContent': 'center', 'gap': '15px'}),
            html.Div(id='output-informe', style={'marginTop': '15px', 'textAlign': 'center'}),
            html.Div(id='output-presentacion', style={'marginTop': '15px', 'textAlign': 'center'})
        ], style={'textAlign': 'center', 'marginTop': '20px'})
    ]),
    
    # Footer
    html.Div([
        html.P("Sistema de Análisis de Rendimiento Académico - Versión 1.0",
              style={'margin': '0', 'color': '#999', 'fontSize': '0.9em'})
    ], style={'textAlign': 'center', 'marginTop': '50px', 'padding': '20px', 
             'borderTop': '1px solid #ddd'})
    
], style={'maxWidth': '1200px', 'margin': '0 auto', 'padding': '30px', 
         'fontFamily': 'Arial, sans-serif', 'background': '#f5f5f5'})


# Callback para actualizar carreras
@app.callback(
    Output('dropdown-carrera', 'options'),
    Output('dropdown-carrera', 'value'),
    Input('dropdown-universidad', 'value')
)
def actualizar_carreras(universidad):
    if not universidad:
        return [], None
    
    carreras = obtener_carreras_de_universidad(universidad)
    return carreras, None


# Callback para actualizar gráficos
@app.callback(
    Output('graficos-container', 'style'),
    Output('mensaje-inicial', 'style'),
    Output('graph-rendimiento', 'figure'),
    Output('graph-comparacion', 'figure'),
    Output('graph-tabla', 'figure'),
    Output('graph-brecha', 'figure'),
    Input('dropdown-carrera', 'value'),
    State('dropdown-universidad', 'value')
)
def actualizar_graficos(carrera, universidad):
    # Figura vacía por defecto
    fig_vacia = go.Figure()
    fig_vacia.update_layout(height=400)
    
    if not universidad or not carrera:
        return (
            {'display': 'none'}, 
            {'display': 'block'},
            fig_vacia, fig_vacia, fig_vacia, fig_vacia
        )
    
    try:
        # Cargar datos
        df = cargar_datos_universidad(universidad)
        df_filtrado = df[df['Carrera'].isin([carrera, 'Todos los ámbitos'])].copy()
        
        if df_filtrado.empty:
            raise ValueError("No hay datos disponibles")
        
        # Crear gráficos
        fig1 = crear_lineas_rendimiento(df_filtrado, carrera)
        fig2 = crear_comparacion_media(df_filtrado, carrera)
        fig3 = crear_tabla_resumen(df_filtrado, carrera)
        fig4 = crear_brecha_genero(df_filtrado, carrera)
        
        return (
            {'display': 'block'}, 
            {'display': 'none'},
            fig1, fig2, fig3, fig4
        )
        
    except Exception as e:
        print(f"Error: {e}")
        return (
            {'display': 'none'}, 
            {'display': 'block'},
            fig_vacia, fig_vacia, fig_vacia, fig_vacia
        )


# Callback para generar informe PDF
@app.callback(
    Output('output-informe', 'children'),
    Input('btn-generar-informe', 'n_clicks'),
    State('dropdown-carrera', 'value'),
    State('dropdown-universidad', 'value'),
    prevent_initial_call=True
)
def generar_informe(n_clicks, carrera, universidad):
    if not universidad or not carrera:
        return html.Div("Seleccione una universidad y carrera", 
                       style={'color': '#f59e0b', 'padding': '10px'})
    
    try:
        # Cargar datos
        df = cargar_datos_universidad(universidad)
        df_filtrado = df[df['Carrera'].isin([carrera, 'Todos los ámbitos'])].copy()
        
        # Crear directorios de salida
        output_dir_graph = Path(__file__).parent.parent / "output" / "graph"
        output_dir_graph.mkdir(parents=True, exist_ok=True)
        
        # Crear y guardar gráficos como imágenes
        fig1 = crear_lineas_rendimiento(df_filtrado, carrera)
        fig2 = crear_comparacion_media(df_filtrado, carrera)
        fig3 = crear_tabla_resumen(df_filtrado, carrera)
        fig4 = crear_brecha_genero(df_filtrado, carrera)
        
        # Guardar como imágenes PNG
        carrera_file = carrera.replace(' ', '_').replace('/', '_')
        img1_path = output_dir_graph / f"rendimiento_{carrera_file}.png"
        img2_path = output_dir_graph / f"comparacion_{carrera_file}.png"
        img3_path = output_dir_graph / f"tabla_{carrera_file}.png"
        img4_path = output_dir_graph / f"brecha_{carrera_file}.png"
        
        fig1.write_image(str(img1_path), width=1200, height=600)
        fig2.write_image(str(img2_path), width=1200, height=600)
        fig3.write_image(str(img3_path), width=1200, height=400)
        fig4.write_image(str(img4_path), width=1200, height=600)
        
        # Generar HTML con imágenes en base64
        import base64
        
        def img_to_base64(img_path):
            with open(img_path, 'rb') as f:
                return base64.b64encode(f.read()).decode()
        
        img1_base64 = img_to_base64(img1_path)
        img2_base64 = img_to_base64(img2_path)
        img3_base64 = img_to_base64(img3_path)
        img4_base64 = img_to_base64(img4_path)
        
        # Cargar y renderizar plantilla
        from jinja2 import Template
        
        template_path = Path(__file__).parent.parent / "templates" / "informe_prueba.html"
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        template = Template(template_content)
        
        html_content = template.render(
            carrera=carrera,
            universidad=universidad.replace('_', ' '),
            fecha=datetime.now().strftime('%d/%m/%Y'),
            periodo=f"{df_filtrado['Anio'].min()} - {df_filtrado['Anio'].max()}",
            graph1_img=img1_base64,
            graph2_img=img2_base64,
            graph3_img=img3_base64,
            graph4_img=img4_base64
        )
        
        # Guardar HTML
        output_dir_html = Path(__file__).parent.parent / "output" / "informe_html"
        output_dir_html.mkdir(parents=True, exist_ok=True)
        
        html_path = output_dir_html / f"informe_{carrera_file}.html"
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Generar PDF
        from weasyprint import HTML
        output_dir_pdf = Path(__file__).parent.parent / "output" / "informe_pdf"
        output_dir_pdf.mkdir(parents=True, exist_ok=True)
        
        pdf_path = output_dir_pdf / f"Informe_{carrera_file}.pdf"
        HTML(string=html_content).write_pdf(str(pdf_path))
        
        return html.Div([
            html.Div("Informe PDF generado exitosamente", 
                    style={'fontSize': '1.1em', 'fontWeight': 'bold', 'color': '#10b981', 'marginBottom': '10px'}),
            html.P(f"Guardado en: {pdf_path}", 
                  style={'fontSize': '0.85em', 'color': '#666', 'marginTop': '5px'})
        ], style={'background': '#d1fae5', 'padding': '15px', 'borderRadius': '8px'})
        
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        print(f"Error detallado: {error_detail}")
        return html.Div(f"Error: {str(e)}", 
                       style={'color': '#ef4444', 'background': '#fee2e2', 
                             'padding': '15px', 'borderRadius': '8px'})


# Callback para generar presentación PDF
@app.callback(
    Output('output-presentacion', 'children'),
    Input('btn-generar-presentacion', 'n_clicks'),
    State('dropdown-carrera', 'value'),
    State('dropdown-universidad', 'value'),
    prevent_initial_call=True
)
def generar_presentacion(n_clicks, carrera, universidad):
    if not universidad or not carrera:
        return html.Div("Seleccione una universidad y carrera", 
                       style={'color': '#f59e0b', 'padding': '10px'})
    
    try:
        # Cargar datos
        df = cargar_datos_universidad(universidad)
        df_filtrado = df[df['Carrera'].isin([carrera, 'Todos los ámbitos'])].copy()
        
        # Crear directorios de salida
        output_dir_graph = Path(__file__).parent.parent / "output" / "graph"
        output_dir_graph.mkdir(parents=True, exist_ok=True)
        
        # Crear y guardar gráficos como imágenes
        fig1 = crear_lineas_rendimiento(df_filtrado, carrera)
        fig2 = crear_comparacion_media(df_filtrado, carrera)
        fig4 = crear_brecha_genero(df_filtrado, carrera)
        
        # Guardar como imágenes PNG
        carrera_file = carrera.replace(' ', '_').replace('/', '_')
        img1_path = output_dir_graph / f"pres_rendimiento_{carrera_file}.png"
        img2_path = output_dir_graph / f"pres_comparacion_{carrera_file}.png"
        img4_path = output_dir_graph / f"pres_brecha_{carrera_file}.png"
        
        fig1.write_image(str(img1_path), width=1400, height=700)
        fig2.write_image(str(img2_path), width=1400, height=700)
        fig4.write_image(str(img4_path), width=1400, height=700)
        
        # Generar HTML con imágenes en base64
        import base64
        
        def img_to_base64(img_path):
            with open(img_path, 'rb') as f:
                return base64.b64encode(f.read()).decode()
        
        img1_base64 = img_to_base64(img1_path)
        img2_base64 = img_to_base64(img2_path)
        img4_base64 = img_to_base64(img4_path)
        
        # Cargar y renderizar plantilla
        from jinja2 import Template
        
        template_path = Path(__file__).parent.parent / "templates" / "plantilla_presentacion.html"
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        template = Template(template_content)
        
        html_content = template.render(
            carrera=carrera,
            universidad=universidad.replace('_', ' '),
            fecha=datetime.now().strftime('%d/%m/%Y'),
            graph1_img=img1_base64,
            graph2_img=img2_base64,
            graph4_img=img4_base64
        )
        
        # Guardar HTML
        output_dir_html = Path(__file__).parent.parent / "output" / "informe_html"
        output_dir_html.mkdir(parents=True, exist_ok=True)
        
        html_path = output_dir_html / f"presentacion_{carrera_file}.html"
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Generar PDF
        from weasyprint import HTML
        output_dir_pdf = Path(__file__).parent.parent / "output" / "informe_pdf"
        output_dir_pdf.mkdir(parents=True, exist_ok=True)
        
        pdf_path = output_dir_pdf / f"Presentacion_{carrera_file}.pdf"
        HTML(string=html_content).write_pdf(str(pdf_path))
        
        return html.Div([
            html.Div("Presentación PDF generada exitosamente", 
                    style={'fontSize': '1.1em', 'fontWeight': 'bold', 'color': '#764ba2', 'marginBottom': '10px'}),
            html.P(f"📁 Guardado en: {pdf_path}", 
                  style={'fontSize': '0.85em', 'color': '#666', 'marginTop': '5px'})
        ], style={'background': '#f3e8ff', 'padding': '15px', 'borderRadius': '8px'})
        
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        print(f"Error detallado: {error_detail}")
        return html.Div(f"Error: {str(e)}", 
                       style={'color': '#ef4444', 'background': '#fee2e2', 
                             'padding': '15px', 'borderRadius': '8px'})


# Ejecutar servidor
if __name__ == '__main__':    
    app.run(debug=True, host='127.0.0.1', port=8050)
