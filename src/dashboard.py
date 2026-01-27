import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
from datetime import datetime
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Inches
import tempfile
import io
import sys
sys.path.append(str(Path(__file__).parent))
from functions.generate_docx import escribir_informe

from charts.interactive.line_chart import grafico_lineas_interactivo as line_chart
from functions.generate_docx import escribir_informe

st.set_page_config(page_title="Dashboard de Análisis Académico", layout="wide")

st.title("Dashboard de Análisis de Rendimiento Académico")

# Subir archivo CSV en la pestaña principal
st.header("Cargar Datos")
uploaded_file = st.file_uploader("Subir archivo CSV", type=['csv'], help="Sube tu archivo CSV con los datos académicos")

if uploaded_file is not None:
    # Leer CSV
    dataset = pd.read_csv(uploaded_file, sep=",")
    
    # Validar columnas requeridas
    columnas_requeridas = ['Tasa', 'Curso', 'Asignatura', 'Valor', 'Convocatoria', 'Tipo']
    columnas_faltantes = [col for col in columnas_requeridas if col not in dataset.columns]
    
    if columnas_faltantes:
        st.error(f"Error: El archivo CSV no contiene las siguientes columnas obligatorias: {', '.join(columnas_faltantes)}")
        st.warning("Por favor, asegúrate de que tu archivo CSV contenga todas las columnas requeridas:")
        st.write("- **Tasa**: Tipo de tasa (Éxito, Rendimiento, etc.)")
        st.write("- **Curso**: Curso de la titulación (Primero, Segundo, etc.)")
        st.write("- **Asignatura**: Nombre de la asignatura")
        st.write("- **Valor**: Valor numérico de la métrica")
        st.write("- **Convocatoria**: Convocatoria (Enero, Junio, Julio)")
        st.write("- **Tipo**: Tipología de la asignatura (Obligatorias, Optativas, etc.)")
        st.stop()
    
    dataset = dataset[dataset['Valor'] != '???']
    
    st.success("Archivo cargado exitosamente")
    
    # Filtros en el sidebar
    st.sidebar.header("Filtros")
    
    # Filtro por convocatoria
    convocatorias_disponibles = ['Curso completo']
    if 'Convocatoria' in dataset.columns:
        convocatorias_disponibles = ['Curso completo'] + list(dataset['Convocatoria'].unique())
    convocatoria = st.sidebar.selectbox(
        "Convocatoria",
        options=convocatorias_disponibles
    )
    
    # Filtro por asignatura
    asignaturas_disponibles = ['Todas']
    if 'Asignatura' in dataset.columns:
        asignaturas_disponibles = ['Todas'] + sorted(list(dataset['Asignatura'].unique()))
    asignatura = st.sidebar.selectbox(
        "Asignatura",
        options=asignaturas_disponibles
    )
    
    # Filtro por curso/cuatrimestre
    cursos_disponibles = ['Todos']
    if 'Curso' in dataset.columns:
        cursos_disponibles = ['Todos', 'Primero', 'Segundo', 'Tercero', 'Cuarto']
    curso = st.sidebar.selectbox(
        "Curso de la titulación",
        options=cursos_disponibles
    )

    # Filtro por tipología
    tipologias_disponibles = ['Todas']
    if 'Tipo' in dataset.columns:
        tipologias_disponibles = ['Todas'] + sorted(list(dataset['Tipo'].unique()))
    tipologia = st.sidebar.selectbox(
        "Tipología de la asignatura",
        options=tipologias_disponibles
    )  

    # Filtro por Itinerario
    itinerarios_disponibles = ['Todos']
    if 'Itinerario' in dataset.columns:
        itinerarios_disponibles = ['Todos'] + sorted(list(dataset['Itinerario'].unique()))
    itinerario = st.sidebar.selectbox(
        "Itinerario",
        options=itinerarios_disponibles
    )  
    
    # Filtro por rango de años
    st.sidebar.subheader("Rango de Años")
    if 'Anio' in dataset.columns:
        # Obtener años académicos únicos y ordenarlos
        anios_academicos = sorted(dataset['Anio'].unique())
        
        # Multiselect para seleccionar años académicos
        anios_seleccionados = st.sidebar.multiselect(
            "Seleccionar años académicos",
            options=anios_academicos,
            default=anios_academicos,
            help="Selecciona uno o más años académicos para filtrar"
        )
    else:
        anios_seleccionados = None
    
    # Aplicar filtros
    df_filtered = dataset.copy()
    
    if convocatoria != 'Curso completo' and 'Convocatoria' in dataset.columns:
        df_filtered = df_filtered[df_filtered['Convocatoria'] == convocatoria]
    
    if asignatura != 'Todas' and 'Asignatura' in dataset.columns:
        df_filtered = df_filtered[df_filtered['Asignatura'] == asignatura]
    
    if curso != 'Todos' and 'Curso' in dataset.columns:
        df_filtered = df_filtered[df_filtered['Curso'] == curso]
    
    if itinerario != 'Todos' and 'Itinerario' in dataset.columns:
        df_filtered = df_filtered[df_filtered['Itinerario'] == itinerario]
    
    if anios_seleccionados is not None and len(anios_seleccionados) > 0 and 'Anio' in df_filtered.columns:
        df_filtered = df_filtered[df_filtered['Anio'].isin(anios_seleccionados)]
    
    # Mostrar métricas
    st.header("Métricas Generales")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if 'Valor' in df_filtered.columns:
            df_filtered['Valor'] = pd.to_numeric(df_filtered['Valor'], errors='coerce')
            promedio = df_filtered['Valor'].mean()
            st.metric("Promedio", f"{promedio:.2f}%")
        else:
            st.metric("Promedio", "N/A")
    
    with col2:
        if 'Valor' in df_filtered.columns:
            maximo = df_filtered['Valor'].max()
            st.metric("Máximo", f"{maximo:.2f}%")
        else:
            st.metric("Máximo", "N/A")
    
    with col3:
        if 'Valor' in df_filtered.columns:
            minimo = df_filtered['Valor'].min()
            st.metric("Mínimo", f"{minimo:.2f}%")
        else:
            st.metric("Mínimo", "N/A")
    
    with col4:
        st.metric("Registros", len(df_filtered))
    
    # Tabs para diferentes visualizaciones
    tab1, tab2 = st.tabs(["Gráficos", "Tabla de Datos"])
    
    with tab1:
        st.subheader("Evolución Temporal")
        
        if 'Anio' in df_filtered.columns and 'Valor' in df_filtered.columns:
            # Preparar datos para gráfico
            if 'Tasa' in df_filtered.columns:
                tasa_seleccionada = st.selectbox("Seleccionar Tasa", options=df_filtered['Tasa'].unique())
                df_grafico = df_filtered[df_filtered['Tasa'] == tasa_seleccionada].copy()
            else:
                df_grafico = df_filtered.copy()
            
            df_grafico['Valor'] = pd.to_numeric(df_grafico['Valor'], errors='coerce')
            
            # Agrupar por año
            df_agrupado = df_grafico.groupby('Anio')['Valor'].mean().reset_index()
            
            # Crear gráfico
            fig = line_chart(df_agrupado)
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No hay datos suficientes para mostrar el gráfico de evolución temporal")
    
    with tab2:
        st.subheader("Datos Filtrados")
        st.dataframe(df_filtered, use_container_width=True, height=400)
    
    # Sección de generación de informes
    st.header("Generación de Informes")
    
    col_inf1, col_inf2 = st.columns(2)
    
    with col_inf1:
        formato_informe = st.selectbox("Formato del informe", ["DOCX", "PDF"])
    
    with col_inf2:
        nombre_informe = st.text_input("Nombre del informe", value="informe_academico")
    
    # Campo obligatorio para el nombre de la universidad
    nombre_universidad = st.text_input(
        "Nombre de la Universidad *", 
        placeholder="Ej: Universidad de La Laguna",
        help="Este campo es obligatorio para generar el informe"
    )
    
    # Campo obligatorio para el nombre de la titulación
    nombre_titulacion = st.text_input(
        "Nombre de la Titulación *",
        placeholder="Ej: Grado en Ingeniería Informática",
        help="Este campo es obligatorio para generar el informe"
    )
    
    # Validar que los campos obligatorios no estén vacíos
    if st.button("Generar y Descargar Informe", type="primary"):
        if not nombre_universidad or nombre_universidad.strip() == "":
            st.error("Por favor, ingresa el nombre de la Universidad antes de generar el informe.")
        elif not nombre_titulacion or nombre_titulacion.strip() == "":
            st.error("Por favor, ingresa el nombre de la Titulación antes de generar el informe.")
        else:
            with st.spinner("Generando informe..."):
                try:
                    # Preparar datos para el informe
                    # Filtros para incluir en el documento
                    anios_str = ', '.join(anios_seleccionados) if anios_seleccionados and len(anios_seleccionados) > 0 else 'Todos'
                    filtros_aplicados = {
                        'convocatoria': convocatoria,
                        'asignatura': asignatura,
                        'curso': curso,
                        'tipologia': tipologia,
                        'itinerario': itinerario if itinerario != 'Todos' else 'N/A',
                        'anios_academicos': anios_str,
                    }
                    
                    # Llamar a la función escribir_informe
                    exito, mensaje, docx_buffer, filename = escribir_informe(
                        carrera=nombre_titulacion,
                        universidad=nombre_universidad,
                        df=df_filtered,
                        nombre_informe=nombre_informe,
                        filtros_aplicados=filtros_aplicados
                    )
                    
                    if exito:
                        st.success("✅ Informe generado exitosamente")
                        
                        st.download_button(
                            label="⬇️ Descargar Informe DOCX",
                            data=docx_buffer,
                            file_name=filename,
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                        )
                    else:
                        st.error(f"❌ Error al generar el informe: {mensaje}")
                    
                except Exception as e:
                    st.error(f"❌ Error al generar el informe: {str(e)}")
                    import traceback
                    st.error(traceback.format_exc())
                    
else:
    st.info("👆 Por favor, sube un archivo CSV para comenzar el análisis")
    
    # Mostrar ejemplo de estructura esperada
    st.subheader("📝 Estructura esperada del CSV")
    st.markdown("""
    El archivo CSV debe contener al menos las siguientes columnas:
    - **Anio**: Año de la cohorte
    - **Valor**: Valor de la métrica
    - **Tasa**: Tipo de tasa
    - **Convocatoria**: Enero, Mayo, Junio/Julio
    - **Asignatura**: Nombre de la asignatura
    - **Curso**: Primero, Segundo, Tercero, Cuarto
    - **Tipologia**: Obligatorias, Optativas, Itinerario
    """)

# Footer
st.markdown("---")
st.markdown("*Dashboard desarrollado para análisis de rendimiento académico*")
