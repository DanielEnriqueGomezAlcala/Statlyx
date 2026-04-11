# Dashboard de Análisis de Calidad Académica

Aplicación web interactiva para el análisis de indicadores de calidad académica universitaria. Permite cargar datos de rendimiento, filtrarlos, visualizarlos y generar informes automáticos en formato Word y PowerPoint con análisis de texto generado por IA.

---

## Características principales

- **Carga y validación** de tablas de datos académicos (asignaturas, titulación, convocatorias)
- **Filtrado dinámico** por rango de años, tipología de asignatura y curso
- **Previsualización tabular** de los datos cargados
- **Generación de informes Word** con gráficas y análisis de texto vía LLM
- **Generación de presentaciones PowerPoint** con el mismo contenido
- **Tres modos de IA**: sin texto, análisis rápido (gpt-4.1-nano) o análisis con razonamiento (gpt-5-nano)
- **Caché de imágenes y respuestas LLM** para acelerar regeneraciones

---

## Requisitos previos

- Python 3.11 o superior
- Clave de API de OpenAI (para la generación de texto con IA)

---

## Instalación

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd TFG
```

### 2. Crear y activar el entorno virtual

```bash
python -m venv .venv
source .venv/bin/activate        # macOS / Linux
.venv\Scripts\activate           # Windows
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Copia el archivo de ejemplo y rellena tus credenciales:

```bash
cp .env.example .env
```

| Variable | Descripción | Requerida |
|----------|-------------|-----------|
| `OPENAI_API_KEY` | Clave de API de OpenAI | Sí |
| `OPENROUTER_API_KEY` | Clave de API de OpenRouter (alternativa) | No |
| `PROVIDER` | Proveedor activo: `openai` o `openrouter` | No (default: `openai`) |
| `GENERATE_TEXT` | Activar generación de texto con IA | No (default: `true`) |
| `MODEL_NAME` | Modelo LLM a usar | No (default: `gpt-4.1-nano`) |

---

## Ejecución

```bash
cd src
python dashboard.py
```

La aplicación estará disponible en [http://localhost:8050](http://localhost:8050).

---

## Archivos de datos requeridos

La aplicación espera cinco archivos Excel con el siguiente contenido:

| Archivo | Descripción | Fila de cabecera |
|---------|-------------|-----------------|
| **Tabla 1** | Tipología y curso por asignatura (`Ass Codnum`, `Tipologia`, `Curso`) | 4 |
| **Tabla 2** | Tasas de rendimiento y éxito por asignatura y año | 4 |
| **Tabla 4** | Indicadores de titulación por año (tasas de éxito, abandono, eficiencia, graduación) | 5 |
| **Convocatorias** | Tasas por convocatoria, grupo y asignatura | 0 |
| **Tabla auxiliar** | Cuatrimestre y mención por asignatura (`Código`, `Cuatrimestre`, `Mención`) | 0 |

---

## Estructura del proyecto

```
TFG/
├── .env                        # Variables de entorno (no commitear)
├── requirements.txt
├── templates/
│   ├── InformePlantilla.docx   # Plantilla Word para los informes
│   └── PresentacionPlantilla.pptx  # Plantilla PowerPoint
└── src/
    ├── dashboard.py            # Punto de entrada de la aplicación
    ├── constants.py            # Constantes globales (cursos, tasas, tipologías)
    ├── assets/                 # Archivos estáticos (CSS, imágenes)
    ├── callbacks/              # Lógica de interacción Dash
    │   ├── upload.py           # Carga y validación de archivos
    │   ├── filter.py           # Aplicación de filtros
    │   ├── preview.py          # Previsualización de tablas
    │   ├── report.py           # Generación de informes
    │   └── header.py
    ├── components/             # Componentes visuales de la UI
    │   ├── upload.py
    │   ├── filter.py
    │   ├── preview.py
    │   ├── report.py
    │   └── header.py
    ├── charts/
    │   ├── dinamic/            # Tablas interactivas Plotly
    │   └── static/             # Gráficas estáticas para los informes
    │       ├── shared/         # Gráficas de líneas y tabla (nivel asignatura)
    │       ├── degree_breakdown/   # Gráficas de titulación
    │       ├── subject_breakdown/  # Resumen por curso
    │       ├── tipology_breakdown/ # Resumen por tipología
    │       ├── mention_breakdown/  # Resumen por mención
    │       └── call_breakdown/     # Resumen por convocatoria
    ├── colors/
    │   └── colors.py           # Paleta de colores corporativa
    ├── functions/
    │   ├── check_data/         # Validación de estructura de tablas
    │   ├── clean_data/         # Limpieza y normalización de datos
    │   ├── generate_information/   # Generación de gráficas y análisis por sección
    │   │   ├── subject_analisis/   # Desglose por curso, tipología, mención, convocatoria
    │   │   └── degree_analisis/    # Análisis de indicadores de titulación
    │   ├── llm/
    │   │   ├── llm.py          # Cliente OpenAI con caché y modos de razonamiento
    │   │   └── prompts/        # Prompts estructurados por tipo de análisis
    │   ├── write_word/         # Generación del informe Word (docxtpl)
    │   └── write_presentation/ # Generación de la presentación PowerPoint (python-pptx)
    └── utils/
        ├── decode_excel.py     # Decodificación de archivos Excel en base64
        ├── filter_by_year.py   # Filtrado de DataFrames por rango de años
        ├── image.py            # Exportación y recorte de gráficas a PNG
        ├── logger.py           # Configuración del logger
        └── report_cache.py     # Gestión del directorio temporal de imágenes
```

---

## Flujo de uso

```
1. Subir archivos  →  2. Ajustar filtros  →  3. Previsualizar datos
        ↓
4. Configurar informe (secciones, tipo de gráfica, IA)
        ↓
5. Generar Word / PowerPoint  →  Descarga automática
```

---

## Secciones del informe

| Sección | Descripción |
|---------|-------------|
| Análisis por titulación | Evolución temporal de los indicadores de titulación |
| Desglose por curso | Tasas de éxito y rendimiento por curso y cuatrimestre |
| Desglose por tipología | Comparativa entre tipos de asignatura |
| Desglose por mención | Análisis por mención (excluye "No aplica") |
| Desglose por convocatoria | Tasas por convocatoria (Enero, Marzo, Mayo, Julio) y grupo |

---

## Modos de generación de texto con IA

| Modo | Modelo | Descripción |
|------|--------|-------------|
| Sin IA | — | Solo gráficas, sin análisis de texto |
| Sin razonamiento | gpt-4.1-nano | Rápido y económico |
| Con razonamiento | gpt-5-nano | Mayor precisión, más lento |

---

## Dependencias principales

| Paquete | Versión | Uso |
|---------|---------|-----|
| dash | 3.0.4 | Framework web |
| dash-mantine-components | 2.5.1 | Componentes UI |
| dash-iconify | 0.1.2 | Iconos |
| plotly | 5.18.0 | Visualizaciones interactivas |
| pandas | 2.2.3 | Manipulación de datos |
| docxtpl | 0.16.7 | Generación de Word con plantilla |
| python-pptx | 1.0.2 | Generación de PowerPoint |
| openai | 2.21.0 | Generación de texto con IA |
| Pillow | 10.4.0 | Procesamiento de imágenes |
| kaleido | 0.2.1 | Exportación de gráficas Plotly a PNG |
| python-dotenv | 1.2.1 | Carga de variables de entorno |
| pydantic | 2.12.5 | Validación de modelos de prompts |
