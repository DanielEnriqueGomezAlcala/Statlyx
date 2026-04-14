<p align="center">
  <img src="src/assets/logo.jpeg" alt="Statlyx logo" width="180" />
</p>

<h1 align="center">Statlyx</h1>

<p align="center">
  Interactive dashboard for university academic quality analysis — upload data, visualize trends, and generate AI-powered reports in Word and PowerPoint.
</p>

<p align="center">
  <a href="https://github.com/DanielEnriqueGomezAlcala/TFG/actions/workflows/ci.yml"><img src="https://github.com/DanielEnriqueGomezAlcala/TFG/actions/workflows/ci.yml/badge.svg" alt="CI" /></a>
  <img src="https://img.shields.io/badge/python-3.13-blue" alt="Python 3.13" />
  <img src="https://img.shields.io/badge/license-MIT-purple" alt="MIT License" />
</p>

---

## Overview

Statlyx is a [Dash](https://dash.plotly.com/)-based web application designed for university departments to analyze academic quality indicators. It guides you through a structured workflow: upload institutional Excel datasets, apply dynamic filters, preview results interactively, and export comprehensive reports — with optional AI-generated analysis powered by OpenAI models.

The tool was developed as a Bachelor's Thesis (TFG) project targeting Spanish university quality evaluation processes.

## Features

- **Upload & validate** five structured Excel tables covering subjects, degrees, and exam sessions
- **Dynamic filtering** by year range, subject typology, and course
- **Interactive data preview** with sortable, filterable Plotly tables
- **Word & PowerPoint report generation** from a single dataset, using `.docx`/`.pptx` templates
- **Three AI modes** — no text, fast analysis (`gpt-4.1-nano`), or deeper reasoning (`gpt-5-nano`)
- **LLM response caching** (MD5-based) to avoid redundant API calls on regeneration
- **Five configurable report sections** — toggle each breakdown independently
- **Static chart export** via Kaleido for embedding publication-ready PNG graphics in reports

## Workflow

```
1. Upload Excel files  →  2. Apply filters  →  3. Preview data
                                                        ↓
                          5. Download report  ←  4. Configure & generate
```

## Getting started

### Prerequisites

- [uv](https://docs.astral.sh/uv/) — Python package manager
- Python 3.13
- An OpenAI API key

### Installation

```bash
git clone https://github.com/DanielEnriqueGomezAlcala/TFG.git
cd TFG
uv sync
```

`uv sync` automatically creates a `.venv` and installs all dependencies from `pyproject.toml`.

### Configuration

Copy the environment template and fill in your credentials:

```bash
cp .env.example .env
```

| Variable | Description | Required | Default |
|---|---|---|---|
| `OPENAI_API_KEY` | OpenAI API key | Yes | — |

> [!NOTE]
> If `GENERATE_TEXT=false`, reports are generated with charts only — no API calls are made.

### Running the app

```bash
uv run python src/dashboard.py
```

The dashboard is available at **http://localhost:8050**.

## Data format

The application expects five Excel files. Upload them through the UI in any order.

| File | Content | Header row |
|---|---|---|
| **Tabla 1** | Subject typology and course (`Ass Codnum`, `Tipologia`, `Curso`) | 4 |
| **Tabla 2** | Subject success and performance rates by year | 4 |
| **Tabla 4** | Degree indicators by year (success, dropout, efficiency, graduation rates) | 5 |
| **Convocatorias** | Exam-session rates by subject and group | 0 |
| **Tabla auxiliar** | Subject semester and specialization (`Código`, `Cuatrimestre`, `Mención`) | 0 |

Sample datasets are available under `data/mock-clean-data/` and `data/mock-raw-data/`.

## Report sections

Each section can be toggled on or off before generating a report:

| Section | Description |
|---|---|
| Degree analysis | Time-series evolution of degree-level quality indicators |
| Course breakdown | Success and performance rates by course and semester |
| Typology breakdown | Comparison across subject types (basic, compulsory, optional, TFG, internships) |
| Specialization breakdown | Analysis by academic track/mention (excludes "No aplica") |
| Exam-session breakdown | Rates by session (January, March, May, July) and group |

## AI modes

| Mode | Model | Notes |
|---|---|---|
| No AI | — | Charts only; no API calls |
| Fast | `gpt-4.1-nano` | Low latency, economical |
| Reasoning | `gpt-5-nano` | Higher accuracy, slower |

Responses are cached locally by prompt hash — regenerating a report reuses cached text unless the underlying data changes.

## Project structure

```
TFG/
├── src/
│   ├── dashboard.py            # App entry point
│   ├── constants.py            # Global constants (courses, rates, typologies)
│   ├── assets/                 # Static files (logo, CSS, example images)
│   ├── callbacks/              # Dash event handlers (upload, filter, preview, report)
│   ├── components/             # UI components
│   ├── charts/
│   │   ├── dinamic/            # Interactive Plotly tables
│   │   └── static/             # PNG charts for reports (line, table, breakdown)
│   ├── colors/                 # Corporate color palette
│   ├── functions/
│   │   ├── check_data/         # Table structure validation
│   │   ├── clean_data/         # Data normalization
│   │   ├── generate_information/  # Per-section chart & analysis generation
│   │   ├── llm/                # OpenAI client, caching, structured prompts
│   │   ├── write_word/         # Word report generation (docxtpl)
│   │   └── write_presentation/ # PowerPoint generation (python-pptx)
│   └── utils/                  # Helpers (Excel decode, year filter, image export, logger)
├── templates/
│   ├── InformePlantilla.docx   # Word template
│   └── PresentacionPlantilla.pptx  # PowerPoint template
├── data/
│   ├── mock-clean-data/        # Sample cleaned datasets
│   └── mock-raw-data/          # Sample raw datasets
├── notebooks/                  # Jupyter notebooks for data exploration
├── knime/                      # KNIME workflows for raw data preprocessing
├── docs/                       # MkDocs API documentation source
└── pyproject.toml              # Dependencies and project metadata
```

## Documentation

API documentation is built with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/) and deployed automatically to GitHub Pages on every push to `main`.

```bash
# Serve docs locally
uv run mkdocs serve

# Deploy to GitHub Pages manually
uv run mkdocs gh-deploy --force
```

## Contributing

```bash
# Install dev dependencies and pre-commit hooks
uv sync
uv run pre-commit install
```

The CI pipeline runs Ruff linting and formatting checks on every pull request. All checks must pass before merging.
