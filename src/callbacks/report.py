import io
import os
import tempfile

import pandas as pd
from dash import ALL, Input, Output, State, ctx, dcc

from functions.write_word.write_word import write_word
from functions.write_presentation.write_presentation import write_presentation

_TEMPLATE_WORD_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'templates', 'InformePruebaV7.docx')
_TEMPLATE_PPTX_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'templates', 'PresentacionPlantilla.pptx')
_SUBITEM_VALUES = ["desglose-curso", "desglose-tipologia", "desglose-menciones", "desglose-convocatoria"]


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
        if ctx.triggered_id == "check-asignatura":
            checked_states = [all_checked if not d else False for d in disabled_states]
        active = [c for c, d in zip(checked_states, disabled_states) if not d]
        all_checked_state = bool(active) and all(active)
        indeterminate = any(active) and not all_checked_state
        return all_checked_state, indeterminate, checked_states

    @app.callback(
        Output("chart-selector", "data"),
        Input("check-titulacion", "checked"),
        Input({"type": "check-asignatura-item", "index": ALL}, "checked"),
    )
    def update_chart_selector(titulacion_checked, asignatura_items_checked):
        selected = []
        if titulacion_checked:
            selected.append("analisis-titulacion")
        for value, checked in zip(_SUBITEM_VALUES, asignatura_items_checked):
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
        disabled = not (institucion and titulacion and filtered_t1_t2 and filtered_t4 and filtered_conv)
        return disabled, disabled

    @app.callback(
        Output('download-report-word', 'data'),
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
        prevent_initial_call=True,
    )
    def generate_report_word(
        _n_clicks,
        filtered_t1_t2, filtered_t4, filtered_conv,
        institucion, titulacion,
        chart_selector, chart_types,
        target_value, limit_value,
    ):
        df      = pd.read_json(io.StringIO(filtered_t1_t2), orient='split')
        df_t4   = pd.read_json(io.StringIO(filtered_t4),    orient='split')
        df_conv = pd.read_json(io.StringIO(filtered_conv),  orient='split')

        with tempfile.TemporaryDirectory() as directorio:
            ruta_guardado = write_word(
                df, df_t4, df_conv,
                _TEMPLATE_WORD_PATH, directorio,
                chart_selector, chart_types,
                institucion, titulacion,
                target_value, limit_value,
            )
            return dcc.send_file(ruta_guardado)

    @app.callback(
        Output('download-report-pptx', 'data'),
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
        prevent_initial_call=True,
    )
    def generate_report_pptx(
        _n_clicks,
        filtered_t1_t2, filtered_t4, filtered_conv,
        institucion, titulacion,
        chart_selector, chart_types,
        target_value, limit_value,
    ):
        df      = pd.read_json(io.StringIO(filtered_t1_t2), orient='split')
        df_t4   = pd.read_json(io.StringIO(filtered_t4),    orient='split')
        df_conv = pd.read_json(io.StringIO(filtered_conv),  orient='split')

        with tempfile.TemporaryDirectory() as directorio:
            ruta_guardado = write_presentation(
                df, df_t4, df_conv,
                _TEMPLATE_PPTX_PATH, directorio,
                chart_selector, chart_types,
                institucion, titulacion,
                target_value, limit_value,
            )
            return dcc.send_file(ruta_guardado)
