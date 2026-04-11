import io
import os

import pandas as pd
import dash_mantine_components as dmc
from dash import ALL, Input, Output, State, ctx, dcc

from functions.write_word.write_word import write_word
from functions.write_presentation.write_presentation import write_presentation
from functions.llm.llm import set_llm_mode
from utils.report_cache import get_image_dir
from utils.logger import get_logger

logger = get_logger(__name__)

RUTA_PLANTILLA_WORD = os.path.join(os.path.dirname(__file__), '..', '..', 'templates', 'InformePlantilla.docx')
RUTA_PLANTILLA_PPTX = os.path.join(os.path.dirname(__file__), '..', '..', 'templates', 'PresentacionPlantilla.pptx')
SUBITEMS = ["desglose-curso", "desglose-tipologia", "desglose-menciones", "desglose-convocatoria"]
OPCIONES_LLM = {
    "no":               "No se generará texto con IA. El informe solo incluirá gráficas.",
    "sin-razonamiento": f"Usa gpt-4.1-nano. Rápido y económico, sin razonamiento interno.",
    "con-razonamiento": f"Usa gpt-5-nano con razonamiento. Más preciso pero más lento.",
}


def register_callbacks(app):
    @app.callback(
        Output('check-titulacion', 'disabled'),
        Output({'type': 'check-asignatura-item', 'index': 0}, 'disabled'),
        Output({'type': 'check-asignatura-item', 'index': 1}, 'disabled'),
        Output({'type': 'check-asignatura-item', 'index': 2}, 'disabled'),
        Output({'type': 'check-asignatura-item', 'index': 3}, 'disabled'),
        Output('check-asignatura', 'disabled'),
        Input('stored-t1-t2', 'data'),
        Input('stored-conv', 'data'),
        Input('stored-t4', 'data'),
    )
    def update_report_options(stored_t1t2, stored_conv, stored_t4):
        """Activa o desactiva las opciones del informe según los datos disponibles.

        Args:
            stored_t1t2: JSON serializado del DataFrame de asignaturas (o ``None``).
            stored_conv: JSON serializado del DataFrame de convocatorias (o ``None``).
            stored_t4: JSON serializado del DataFrame de indicadores de titulación (o ``None``).
        """
        return (
            not stored_t4,
            not stored_t1t2,   # desglose-curso
            not stored_t1t2,   # desglose-tipologia
            not stored_t1t2,   # desglose-menciones
            not stored_conv,   # desglose-convocatoria
            not stored_t1t2,   # check padre analisis-asignatura
        )

    @app.callback(
        Output("check-asignatura", "checked"),
        Output("check-asignatura", "indeterminate"),
        Output({"type": "check-asignatura-item", "index": ALL}, "checked"),
        Input("check-asignatura", "checked"),
        Input({"type": "check-asignatura-item", "index": ALL}, "checked"),
        State({"type": "check-asignatura-item", "index": ALL}, "disabled"),
        prevent_initial_call=True,
    )
    def update_asignatura_checkbox(all_checked, checked_states, disabled_states):
        """Sincroniza el checkbox padre de análisis por asignatura con sus subitems.

        Gestiona los estados checked, indeterminate y disabled de forma coherente.

        Args:
            all_checked: Estado del checkbox padre (marcar/desmarcar todos).
            checked_states: Lista de estados de los checkboxes de cada subitem.
            disabled_states: Lista de estados disabled de cada subitem.
        """
        if ctx.triggered_id == "check-asignatura":
            checked_states = [all_checked if not d else False for d in disabled_states]
        active = [c for c, d in zip(checked_states, disabled_states) if not d]
        all_checked_state = bool(active) and all(active)
        indeterminate = any(active) and not all_checked_state
        return all_checked_state, indeterminate, checked_states



    @app.callback(
        Output("llm-mode-description", "children"),
        Input("llm-mode-selector", "value"),
    )
    def update_llm_mode_description(mode):
        """Devuelve la descripción textual del modo LLM seleccionado.

        Args:
            mode: Identificador del modo LLM seleccionado.
        """
        return OPCIONES_LLM.get(mode, "")

    @app.callback(
        Output("chart-selector", "data"),
        Input("check-titulacion", "checked"),
        Input({"type": "check-asignatura-item", "index": ALL}, "checked"),
    )
    def update_chart_selector(titulacion_checked, asignatura_items_checked):
        """Construye la lista de secciones seleccionadas para incluir en el informe.

        Args:
            titulacion_checked: ``True`` si el análisis por titulación está activado.
            asignatura_items_checked: Lista de estados de los checkboxes de los desgloses
                por asignatura (curso, tipología, menciones, convocatoria).
        """
        selected = []
        if titulacion_checked:
            selected.append("analisis-titulacion")
        for value, checked in zip(SUBITEMS, asignatura_items_checked):
            if checked:
                selected.append(value)
        return selected

    @app.callback(
        Output('generate-report-word-button', 'disabled'),
        Output('generate-report-pptx-button', 'disabled'),
        Input('institution-input', 'value'),
        Input('degree-input', 'value'),
        Input('filtered-t1-t2', 'data'),
        Input('filtered-t4', 'data'),
        Input('filtered-conv', 'data'),
    )
    def toggle_report_button(institucion, titulacion, filtered_t1_t2, filtered_t4, filtered_conv):
        """Desactiva los botones de generación si faltan datos obligatorios.

        Args:
            institucion: Nombre de la institución introducido por el usuario.
            titulacion: Nombre de la titulación introducido por el usuario.
            filtered_t1_t2: JSON del DataFrame filtrado de asignaturas (o ``None``).
            filtered_t4: JSON del DataFrame filtrado de indicadores (o ``None``).
            filtered_conv: JSON del DataFrame filtrado de convocatorias (o ``None``).
        """
        disabled = not (institucion and titulacion and filtered_t1_t2 and filtered_t4 and filtered_conv)
        return disabled, disabled

    @app.callback(
        Output('download-report-word', 'data'),
        Output('report-generation-status', 'children'),
        Input('generate-report-word-button', 'n_clicks'),
        State('filtered-t1-t2', 'data'),
        State('filtered-t4', 'data'),
        State('filtered-conv', 'data'),
        State('institution-input', 'value'),
        State('degree-input', 'value'),
        State('chart-selector', 'data'),
        State('chart-type-selector', 'value'),
        State('target-value-input', 'value'),
        State('limit-value-input', 'value'),
        State('llm-mode-selector', 'value'),
        running=[
            (Output('generate-report-word-button', 'loading'), True, False),
            (Output('generate-report-pptx-button', 'disabled'), True, False),
        ],
        prevent_initial_call=True,
    )
    def generate_report_word(_n_clicks, filtered_t1_t2, filtered_t4, filtered_conv, institucion, titulacion, chart_selector, chart_types, target_value, limit_value, llm_mode):
        """Genera el informe Word y lo envía al navegador para su descarga.

        Args:
            _n_clicks: Número de clics del botón (usado solo para disparar el callback).
            filtered_t1_t2: JSON del DataFrame filtrado de asignaturas.
            filtered_t4: JSON del DataFrame filtrado de indicadores de titulación.
            filtered_conv: JSON del DataFrame filtrado de convocatorias.
            institucion: Nombre de la institución.
            titulacion: Nombre de la titulación.
            chart_selector: Lista de secciones a incluir en el informe.
            chart_types: Lista de tipos de gráfica a generar.
            target_value: Valor de la tasa objetivo para las líneas de referencia.
            limit_value: Valor de la tasa límite para las líneas de referencia.
            llm_mode: Modo de generación de texto con IA.
        """
        set_llm_mode(llm_mode or "sin-razonamiento")
        logger.info("Generando informe Word — secciones: %s, modo LLM: %s", chart_selector, llm_mode)
        df      = pd.read_json(io.StringIO(filtered_t1_t2), orient='split')
        df_t4   = pd.read_json(io.StringIO(filtered_t4),    orient='split')
        df_conv = pd.read_json(io.StringIO(filtered_conv),  orient='split')

        directorio = get_image_dir()
        try:
            ruta_guardado = write_word(
                df, df_t4, df_conv,
                RUTA_PLANTILLA_WORD, directorio,
                chart_selector, chart_types,
                institucion, titulacion,
                target_value, limit_value,
            )
            logger.info("Informe Word generado: %s", os.path.basename(ruta_guardado))
            status = dmc.Alert("Informe Word generado correctamente.", color="green", variant="light")
            return dcc.send_file(ruta_guardado), status
        except Exception as e:
            logger.error("Error generando informe Word: %s", e)
            status = dmc.Alert(f"Error al generar el informe: {e}", color="red", variant="light")
            return None, status

    @app.callback(
        Output('download-report-pptx', 'data'),
        Output('report-generation-status', 'children', allow_duplicate=True),
        Input('generate-report-pptx-button', 'n_clicks'),
        State('filtered-t1-t2', 'data'),
        State('filtered-t4', 'data'),
        State('filtered-conv', 'data'),
        State('institution-input', 'value'),
        State('degree-input', 'value'),
        State('chart-selector', 'data'),
        State('chart-type-selector', 'value'),
        State('target-value-input', 'value'),
        State('limit-value-input', 'value'),
        State('llm-mode-selector', 'value'),
        running=[
            (Output('generate-report-pptx-button', 'loading'), True, False),
            (Output('generate-report-word-button', 'disabled'), True, False),
        ],
        prevent_initial_call=True,
    )
    def generate_report_pptx(_n_clicks, filtered_t1_t2, filtered_t4, filtered_conv, institucion, titulacion, chart_selector, chart_types, target_value, limit_value, llm_mode):
        """Genera la presentación PowerPoint y la envía al navegador para su descarga.

        Args:
            _n_clicks: Número de clics del botón (usado solo para disparar el callback).
            filtered_t1_t2: JSON del DataFrame filtrado de asignaturas.
            filtered_t4: JSON del DataFrame filtrado de indicadores de titulación.
            filtered_conv: JSON del DataFrame filtrado de convocatorias.
            institucion: Nombre de la institución.
            titulacion: Nombre de la titulación.
            chart_selector: Lista de secciones a incluir en la presentación.
            chart_types: Lista de tipos de gráfica a generar.
            target_value: Valor de la tasa objetivo para las líneas de referencia.
            limit_value: Valor de la tasa límite para las líneas de referencia.
            llm_mode: Modo de generación de texto con IA.
        """
        set_llm_mode(llm_mode or "sin-razonamiento")
        logger.info("Generando presentación PPTX — secciones: %s, modo LLM: %s", chart_selector, llm_mode)
        df      = pd.read_json(io.StringIO(filtered_t1_t2), orient='split')
        df_t4   = pd.read_json(io.StringIO(filtered_t4),    orient='split')
        df_conv = pd.read_json(io.StringIO(filtered_conv),  orient='split')

        directorio = get_image_dir()
        try:
            ruta_guardado = write_presentation(
                df, df_t4, df_conv,
                RUTA_PLANTILLA_PPTX, directorio,
                chart_selector, chart_types,
                institucion, titulacion,
                target_value, limit_value,
            )
            logger.info("Presentación PPTX generada: %s", os.path.basename(ruta_guardado))
            status = dmc.Alert("Presentación PowerPoint generada correctamente.", color="green", variant="light")
            return dcc.send_file(ruta_guardado), status
        except Exception as e:
            logger.error("Error generando presentación PPTX: %s", e)
            status = dmc.Alert(f"Error al generar la presentación: {e}", color="red", variant="light")
            return None, status
