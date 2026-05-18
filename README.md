<p align="center">
  <img src="src/assets/logo.jpeg" alt="Statlyx logo" width="180" />
</p>

<h1 align="center">Statlyx</h1>

<p align="center">
  Dashboard interactivo para automatizar la generación de informes de rendimiento en el ámbito académico
</p>

<p align="center">
  <a href="https://github.com/DanielEnriqueGomezAlcala/Statlyx/actions/workflows/ci.yml"><img src="https://github.com/DanielEnriqueGomezAlcala/Statlyx/actions/workflows/ci.yml/badge.svg" alt="CI" /></a>
  <a href="https://github.com/DanielEnriqueGomezAlcala/Statlyx/actions/workflows/tests.yml"><img src="https://github.com/DanielEnriqueGomezAlcala/Statlyx/actions/workflows/tests.yml/badge.svg" alt="Tests" /></a>
  <img src="https://img.shields.io/badge/python-3.13-blue" alt="Python 3.13" />
  <img src="https://img.shields.io/badge/license-MIT-purple" alt="MIT License" />
  <a href="https://danielenriquegomezalcala.github.io/Statlyx/"><img src="https://img.shields.io/badge/Docs-v1.0.0-blue?style=flat-square" alt="MIT License" /></a>
</p>

---

## Acceder a la documentación del código

[Documentación del código](https://danielenriquegomezalcala.github.io/Statlyx/)

## Visión general

Statlyx es una aplicación web que usa [Dash](https://dash.plotly.com/). Está diseñada para automatizar la generación de los informes de rendimiento en el ámbito universitario.

La aplicación te guía de manera sencilla hasta lograr el resultado: carga de datos institucionales en formato Excel, se aplican validaciones y filtros, se previsualizan los datos y se rellena un formulario para generar los informes con la posibilidad de usar un modelo de OpenAI para el análisis.

## Características

- **Subida y validación de datos**: Se suben cinco ficheros Excel con una estructura específica y la aplicación valida si son válidos o no
- **Filtro**: Se pueden filtrar los Datasets generar el informe a medida
- **Previsualización**: Se pueden visualizar los datos que se usaran en el análisis de manera sencilla
- **Generación de documentos Word y PowerPoint**: Generar documentos completos, ya sean informes o presentaciones
- **LLM**: Se da la posibilidad de generar el informe con análisis por IA
- **Caché**: Se implementa un sistema de caché para evitar regenerar gráficos o llamadas al LLM
- **Selección de secciones**: Contenido del informe configurable

## Flujo de la aplicación

```
1. Se suben los ficheros en formato Excel  →  2. Se aplican Filtros
                                                        ↓
                                          3. Previsualización de los datos
                                                        ↓
                5. Descarga del reporte  ←  4. Configuración del documento
```

## Poner la aplicación a funcionar

### Sin usar docker

#### Requisitos

- Tener [uv](https://docs.astral.sh/uv/) descargado
- Python 3.13 o superior
- Poseer una API key de OpenAI

#### Instalación

```bash
mkdir Statlyx
cd Statlyx
git clone https://github.com/DanielEnriqueGomezAlcala/TFG.git .
cd TFG
uv sync
```

> [!NOTE]
> `uv sync` crea automáticamente un entorno virtual y descarga las dependencias del proyecto

#### Configuración

Copiamos el fichero .env.example y lo renombramos a .env. En él tendremos que escribir la API key de OpenAI sk...

```bash
cp .env.example .env
```

| Variable | Descripción | Requerida |
|---|---|---|
| `OPENAI_API_KEY` | OpenAI API key | Yes |

> [!NOTE]
> En el dashboard si se selecciona la generación sin IA, funcionará sin gastar Tokens

#### Poner la App a funcionar

```bash
uv run python src/dashboard.py
```

El dashboard se ejecutará en **http://localhost:8050**.

### Con docker (Se recomienda usar Docker Desktop)

Si usas docker es más sencillo, lo único que tendría que hacer es descargar la imagen usando el siguiente comando

```bash
docker pull ghcr.io/danielenriquegomezalcala/tfg:sha-8ffe584
```

Para hacerlo funcionar:

```bash
docker run -p 8050:8050 \
    -e OPENAI_API_KEY=sk-... \
    ghcr.io/danielenriquegomezalcala/tfg:sha-8ffe584
```

> [!WARNING]
> La API key de OpenAI es opcional ponerla, si no se pone la aplicación funcionará sin la feature de LLM

## Formato de los datos de subida

La aplicación necesita 5 ficheros Excel, cada uno con una estructura específica. En caso de no tenerla, la aplicación te notificará qué fichero está fallando y qué columna/fila se necesita.

### Tabla 1 - Datos de asignaturas
| Nombre de columna | Descripción | Ejemplo |
| :--- | :--- | :--- |
| `Ass Codnum` | Código numérico único asignado a la asignatura | `139261011` |
| `Tipologia` | Tipo de asignatura | `FORMACIÓN BÁSICA` |
| `Curso` | A que curso pertenece | `1, 2, 3, 4, 5, 6` |

### Tabla 2 - Datos de asignaturas - tasas
| Nombre de columna | Descripción | Ejemplo |
| :--- | :--- | :--- |
| `Curso Aca` | Periodo del curso académico | `2020-21` |
| `Cod Asig` | Código numérico único asignado a la asignatura | `139260901` |
| `Nummat` | Número de matriculados | `42` |
| `Asignatura` | Nombre de la asignatura | `ADMINISTRACIÓN Y DISEÑO DE BASE DE DATOS` |
| `Tasa Rend` | Valor de la tasa de rendimiento | `92,9` |
| `Tasa Exito` | Valor de la tasa de éxito | `93,9` |

### Tabla 4 - Datos de titulación

> [!WARNING]
> Esta tabla es distinta al resto: las columnas deben ser los años mientras que las filas son lo que se definen a continuación

| Nombre de fila | Descripción | Ejemplo |
| :--- | :--- | :--- |
| `18   -Tasa de éxito del título` | Tasa de éxito a nivel de titulación | `71,9` |
| `15   -Tasa de abandono del título - (IA)` | Tasa de abandono a nivel de titulación | `72,4` |
| `17   -Tasa de rendimiento del título - (IA)` | Tasa de rendimiento a nivel de titulación | `88,1` |
| `16   -Tasa de eficiencia de los graduados - (IA)` | Tasa de eficiencia a nivel de titulación | `71,3` |
| `14   -Tasa de graduación del título - (IA)` | Tasa de graduación a nivel de titulación | `91,3` |

### Tabla auxiliar 1 - Datos extra de las asignaturas
| Nombre de columna | Descripción | Ejemplo |
| :--- | :--- | :--- |
| `Código` | Código numérico único asignado a la asignatura | `139261011` |
| `Cuatrimestre` | Cuatrimestre al que pertenece la asignatura | `1, 2` |
| `Mención` | En caso de pertenecer a una mención | `Computación` |

> [!WARNING]
> En caso de no pertenecer a ninguna mención, poner **No aplica**

### Tabla auxiliar 2 - Datos de convocatoria
| Nombre de columna | Descripción | Ejemplo |
| :--- | :--- | :--- |
| `Curso` | Periodo del curso académico | `2024-2025` |
| `Convocatoria` | Convocatoria a la que pertenece | `MAY, ENE, JUL, MAR` |
| `Grupo` | Grupo de la asignatura | `1, 2` |
| `Cod` | Código numérico único asignado a la asignatura | `139263124` |
| `Eficiencia` | Valor de la tasa de eficiencia | `0,74` |
| `Exito` | Valor de la tasa de éxito | `0,9` |

## Secciones del reporte

Cada sección puede seleccionarse o deseleccionarse según las necesidades del informe

| Sección | Descripción |
|---|---|
| Análisis de titulación | Evolución de las tasas a nivel de titulación a lo largo del tiempo |
| Desglose por curso/cuatrimestre | Se hace un análisis de las asignaturas desglosadas en curso y cuatrimestre |
| Desglose por tipología | Análisis de las asignaturas según su tipo (Formación básica, Obligatorias, etc) |
| Desglose por mención | Análisis de las asignaturas separadas por mención (en caso de que existan) |
| Desglose por convocatoria | Análisis de las asignaturas desglosadas por curso y convocatoria |

## Modos de generación con LLM

| Mode | Model | Notes |
|---|---|---|
| Sin IA | — | Solo contendrá gráficas |
| Rápida | `gpt-4.1-nano` | Generará conclusiones de manera rápida |
| Razonamiento | `gpt-5-nano` | Tardará más en generar el informe pero será de mejor calidad |

> [!NOTE]
> Tanto las gráficas como las llamadas al LLM son cacheadas con el fin de evitar gastar recursos

## Estructura del proyecto

```
Statlyx/
├── src/
│   ├── dashboard.py            # Dashboard
│   ├── constants.py            # Constantes globales
│   ├── assets/                 # Imagenes que se usan en el dashboard
│   ├── callbacks/              # Logica del dashboard
│   ├── components/             # Componentes utilizados en el dashboard
│   ├── charts/
│   │   ├── dinamic/            # Funciones de graficos interactivos de Plotly
│   │   └── static/             # Funciones de graficos estáticos de Plotly
│   ├── colors/                 # Paleta de colores de la aplicación
│   ├── functions/
│   │   ├── check_data/         # Funciones de validación de las tablas subidas
│   │   ├── clean_data/         # Funciones de limpieza de las tablas
│   │   ├── generate_information/  # Funciones para generar la información que se inyectan en los reportes
│   │   ├── llm/                # Funciones para la integración del LLM
│   │   ├── write_word/         # Orquestador para generar los informes Word
│   │   └── write_presentation/ # Orquestador para generar las presentaciones PowerPoint
│   └── utils/                  # Funciones auxiliares
├── templates/
│   ├── InformePlantilla.docx   # Plantilla Word
│   └── PresentacionPlantilla.pptx  # Plantilla PowerPoint
├── docs/                       # Configuración de la documentación del código
└── pyproject.toml              # Dependencias del proyecto
```
