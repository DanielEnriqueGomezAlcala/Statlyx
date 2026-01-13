import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.graph_objects as go

# Importar funciones de gráficos interactivos
from functions.charts.interactive import (
    crear_lineas_rendimiento,
    crear_comparacion_media,
    crear_tabla_resumen,
    crear_brecha_genero
)

# Importar funciones de generación de documentos
from functions.generar_informe import generar_informe_docx
from functions.generar_presentacion import generar_presentacion_pptx

# Configuración de la página
st.set_page_config(
    page_title="Dashboard Rendimiento Académico",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados
st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
    }
    .stButton>button {
        width: 100%;
        background-color: #667eea;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        border: none;
    }
    .stButton>button:hover {
        background-color: #5568d3;
    }
    h1 {
        color: #667eea;
    }
    h2 {
        color: #667eea;
        border-bottom: 3px solid #667eea;
        padding-bottom: 10px;
    }
    h3 {
        color: #667eea;
    }
    </style>
""", unsafe_allow_html=True)


@st.cache_data
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


@st.cache_data
def cargar_datos_universidad(universidad_folder):
    """Carga los datos de una universidad"""
    base_path = Path(__file__).parent.parent / "data" / "clean-data" / universidad_folder / "Tabla.csv"
    
    try:
        df = pd.read_csv(base_path, sep=';', encoding='utf-8')
        df['Valor'] = pd.to_numeric(df['Valor'].replace('???', pd.NA), errors='coerce')
        return df
    except Exception as e:
        st.error(f"Error al cargar datos: {e}")
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
            carreras_filtradas.append(c)
    
    return sorted(carreras_filtradas)


# Header
st.markdown("""
    <div style='padding: 30px; background: #667eea; 
         border-radius: 10px; margin-bottom: 30px; text-align: center;'>
        <h1 style='margin: 0; color: white;'>Dashboard de Rendimiento Académico</h1>
        <p style='margin: 10px 0 0 0; color: #e0e0e0; font-size: 1.1em;'>
            Análisis de Rendimiento Universitario
        </p>
    </div>
""", unsafe_allow_html=True)

# Sidebar para controles
with st.sidebar:
    st.header("Selección de Datos")
    
    # Obtener universidades
    universidades = obtener_universidades_disponibles()
    universidades_dict = {u['label']: u['value'] for u in universidades}
    
    # Selector de universidad
    universidad_label = st.selectbox(
        "Universidad",
        options=["Seleccione una universidad..."] + list(universidades_dict.keys()),
        key="universidad"
    )
    
    # Selector de carrera
    if universidad_label and universidad_label != "Seleccione una universidad...":
        universidad_value = universidades_dict[universidad_label]
        carreras = obtener_carreras_de_universidad(universidad_value)
        
        carrera = st.selectbox(
            "Carrera",
            options=["Seleccione una carrera..."] + carreras,
            key="carrera"
        )
    else:
        carrera = st.selectbox(
            "Carrera",
            options=["Primero seleccione una universidad..."],
            disabled=True
        )
    
    st.markdown("---")

# Contenido principal
if universidad_label == "Seleccione una universidad..." or carrera == "Seleccione una carrera...":
    st.info("Por favor, seleccione una universidad y una carrera en el panel lateral para visualizar los gráficos.")

else:
    universidad_value = universidades_dict[universidad_label]
    
    try:
        # Cargar datos
        df = cargar_datos_universidad(universidad_value)
        df_filtrado = df[df['Carrera'].isin([carrera, 'Todos los ámbitos'])].copy()
        
        if df_filtrado.empty:
            st.error("No hay datos disponibles para la selección actual.")
        else:
            # Mostrar información de la selección
            st.success(f"**Universidad:** {universidad_label} | **Carrera:** {carrera}")
            
            # Crear tabs para organizar mejor el contenido
            tab1, tab2, tab3, tab4 = st.tabs([
                "Evolución del Rendimiento",
                "Comparación con Media",
                "Resumen de Indicadores",
                "Brecha de Género"
            ])
            
            with tab1:
                st.subheader("Evolución del Rendimiento por Género")
                fig1 = crear_lineas_rendimiento(df_filtrado, carrera)
                st.plotly_chart(fig1, use_container_width=True)
            
            with tab2:
                st.subheader("Comparación con Media Universitaria")
                fig2 = crear_comparacion_media(df_filtrado, carrera)
                st.plotly_chart(fig2, use_container_width=True)
            
            with tab3:
                st.subheader("Resumen de Indicadores")
                fig3 = crear_tabla_resumen(df_filtrado, carrera)
                st.plotly_chart(fig3, use_container_width=True)
            
            with tab4:
                st.subheader("Brecha de Género")
                fig4 = crear_brecha_genero(df_filtrado, carrera)
                st.plotly_chart(fig4, use_container_width=True)
            
            # Sección de generación de documentos
            st.markdown("---")
            st.subheader("Generación de Documentos")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("Generar Informe DOCX", use_container_width=True):
                    with st.spinner("Generando informe..."):
                        success, message, docx_path = generar_informe_docx(
                            carrera, universidad_value, df_filtrado
                        )
                        
                        if success:
                            st.success("Informe DOCX generado exitosamente")
                            st.info(f"Guardado en: {docx_path}")
                        else:
                            st.error(f"Error: {message}")
            
            with col2:
                if st.button("Generar Presentación PPTX", use_container_width=True):
                    with st.spinner("Generando presentación..."):
                        success, message, pptx_path = generar_presentacion_pptx(
                            carrera, universidad_value, df_filtrado
                        )
                        
                        if success:
                            st.success("Presentación PPTX generada exitosamente")
                            st.info(f"Guardado en: {pptx_path}")
                        else:
                            st.error(f"Error: {message}")
    
    except Exception as e:
        st.error(f"Error al procesar los datos: {str(e)}")

# Footer
st.markdown("---")
