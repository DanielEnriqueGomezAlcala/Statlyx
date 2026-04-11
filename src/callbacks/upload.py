import base64
import io
from datetime import datetime as dt

import pandas as pd
from dash import Input, Output, State
import dash_mantine_components as dmc

from functions.clean_data.clean_data_t1t2 import clean_data_t1t2
from functions.clean_data.clean_data_t4 import clean_data_t4
from functions.clean_data.clean_data_call import clean_data_call
from functions.check_data.subject_analisis.check_table_1 import check_table_1
from functions.check_data.subject_analisis.check_table_2 import check_table_2
from functions.check_data.subject_analisis.check_table_1_aux import check_table_1_aux
from functions.check_data.degree_analisis.check_table_4 import check_table_4
from functions.check_data.subject_analisis.check_table_call import check_table_call
from utils.decode_excel import decode_excel


def validate_file(contents, filename, header, check_fn):
    """Decodifica y valida un archivo Excel subido desde la interfaz.

    Args:
        contents: Contenido del archivo en formato base64 (data URI de Dash).
        filename: Nombre del archivo mostrado en el badge.
        header: Índice de la fila que contiene las cabeceras.
        check_fn: Función de validación que recibe un DataFrame y lanza
            ``ValueError`` si no es válido.

    Returns:
        Tupla ``(df, badge, error)`` donde ``df`` es el DataFrame parseado
        (o ``None`` si falló), ``badge`` es el componente visual de estado
        y ``error`` es el mensaje de error (o ``None`` si fue exitoso).
    """
    if contents is None:
        return None, dmc.Badge("Pendiente", color="gray", variant="light", size="sm"), None
    try:
        df = decode_excel(contents, header)
        check_fn(df)
        return df, dmc.Badge(f"✓ {filename}", color="green", variant="light", size="sm"), None
    except ValueError as e:
        return None, dmc.Badge(f"✗ {filename}", color="red", variant="light", size="sm"), str(e)


def register_callbacks(app):
    @app.callback(
        Output('stored-t1-t2', 'data'),
        Output('stored-t4', 'data'),
        Output('stored-conv', 'data'),
        Output('stored-adicional', 'data'),
        Output('upload-status-tabla1', 'children'),
        Output('upload-status-tabla2', 'children'),
        Output('upload-status-tabla4', 'children'),
        Output('upload-status-conv', 'children'),
        Output('upload-status-adicional', 'children'),
        Output('upload-status', 'children'),
        Output('year-picker', 'minDate'),
        Output('year-picker', 'maxDate'),
        Output('tipo-multi-select', 'data'),
        Output('curso-multi-select', 'data'),
        Input('upload-tabla1', 'contents'),
        Input('upload-tabla2', 'contents'),
        Input('upload-tabla4', 'contents'),
        Input('upload-conv', 'contents'),
        Input('upload-adicional', 'contents'),
        State('upload-tabla1', 'filename'),
        State('upload-tabla2', 'filename'),
        State('upload-tabla4', 'filename'),
        State('upload-conv', 'filename'),
        State('upload-adicional', 'filename'),
    )
    def handle_upload(contents_t1, contents_t2, contents_t4, contents_conv, contents_adicional, filename_t1, filename_t2, filename_t4, filename_conv, filename_adicional):
        """Valida, limpia y almacena los archivos subidos por el usuario.

        Callback de Dash disparado cuando el usuario sube uno o más archivos.
        Valida cada archivo, los combina en DataFrames y actualiza el estado
        global de la aplicación junto con los controles de filtro.

        Args:
            contents_t1: Contenido base64 de la tabla 1 (tipología y curso).
            contents_t2: Contenido base64 de la tabla 2 (tasas por asignatura).
            contents_t4: Contenido base64 de la tabla 4 (indicadores de titulación).
            contents_conv: Contenido base64 de la tabla de convocatorias.
            contents_adicional: Contenido base64 de la tabla auxiliar (cuatrimestre y mención).
            filename_t1: Nombre del archivo de la tabla 1.
            filename_t2: Nombre del archivo de la tabla 2.
            filename_t4: Nombre del archivo de la tabla 4.
            filename_conv: Nombre del archivo de convocatorias.
            filename_adicional: Nombre del archivo auxiliar.
        """
        tabla_1,    badge_t1,        err_t1  = validate_file(contents_t1,        filename_t1,        4, check_table_1)
        tabla_2,    badge_t2,        err_t2  = validate_file(contents_t2,        filename_t2,        4, check_table_2)
        tabla_aux,  badge_adicional, err_aux = validate_file(contents_adicional, filename_adicional, 0, check_table_1_aux)
        tabla_4,    badge_t4,        err_t4  = validate_file(contents_t4,        filename_t4,        5, check_table_4)
        tabla_conv, badge_conv,      err_conv = validate_file(contents_conv,     filename_conv,      0, check_table_call)

        badges = [badge_t1, badge_t2, badge_t4, badge_conv, badge_adicional]

        def empty_return(msg):
            return [None, None, None, None, *badges, msg, None, None, [], []]

        errors = {k: v for k, v in [
            ("Tabla 1", err_t1), ("Tabla 2", err_t2), ("Tabla aux", err_aux),
            ("Tabla 4", err_t4), ("Tabla de convocatorias", err_conv),
        ] if v}
        if errors:
            msg = dmc.Alert(
                [dmc.Text(f"• {label}: {err}") for label, err in errors.items()],
                color="red", title="Archivos inválidos",
            )
            return empty_return(msg)

        pending = sum(1 for c in [contents_t1, contents_t2, contents_t4, contents_adicional, contents_conv] if c is None)
        if any(df is None for df in [tabla_1, tabla_2, tabla_4, tabla_aux, tabla_conv]):
            msg = dmc.Alert(
                f"Faltan {pending} archivo{'s' if pending != 1 else ''} por subir",
                color="gray", title="Esperando archivos",
            )
            return empty_return(msg)

        try:
            df_t1t2 = clean_data_t1t2(tabla_1, tabla_2, tabla_aux)
            df_t4   = clean_data_t4(tabla_4)
            df_conv = clean_data_call(tabla_conv, tabla_aux)

            start_years = df_t1t2['Anio'].dropna().str.extract(r'(\d+)')[0].astype(int)
            min_year = dt(int(start_years.min()), 1, 1)
            max_year = dt(int(start_years.max()), 12, 31)

            tipos  = [{'value': v, 'label': v} for v in sorted(df_t1t2['Tipologia'].dropna().unique())]
            cursos = [{'value': str(v), 'label': str(v)} for v in sorted(df_t1t2['Curso'].dropna().unique())]

            msg = dmc.Alert(
                f"Datos procesados correctamente ({len(df_t1t2)} filas)",
                color="green", title="Éxito",
            )
            return [
                df_t1t2.to_json(date_format='iso', orient='split'),
                df_t4.to_json(date_format='iso', orient='split'),
                df_conv.to_json(date_format='iso', orient='split'),
                contents_adicional,
                *badges,
                msg,
                min_year, max_year, tipos, cursos,
            ]

        except Exception as e:
            error = dmc.Alert(f"Error al procesar los archivos: {str(e)}", color="red", title="Error")
            return [None, None, None, None, *badges, error, None, None, [], []]
