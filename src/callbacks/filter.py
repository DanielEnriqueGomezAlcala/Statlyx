import io

import pandas as pd
from dash import Input, Output

from utils.report_cache import clear_cache
from utils.logger import get_logger
from utils.filter_by_year import filter_by_year

logger = get_logger(__name__)

def register_callbacks(app):
    @app.callback(
        Output('filtered-t1-t2', 'data'),
        Output('filtered-t4', 'data'),
        Output('filtered-conv', 'data'),
        Input('stored-t1-t2', 'data'),
        Input('stored-t4', 'data'),
        Input('stored-conv', 'data'),
        Input('year-picker', 'value'),
        Input('tipo-multi-select', 'value'),
        Input('curso-multi-select', 'value'),
    )
    def update_filter(stored_t1_t2, stored_t4, stored_conv, year_range, tipo_multi_select, curso_multi_select):
        """Aplica los filtros activos a los DataFrames almacenados e invalida el caché.

        Callback de Dash disparado al cambiar cualquier filtro. Limpia el caché
        de imágenes y LLM para forzar la regeneración en el siguiente informe.

        Args:
            stored_t1_t2: JSON serializado del DataFrame de asignaturas.
            stored_t4: JSON serializado del DataFrame de indicadores de titulación.
            stored_conv: JSON serializado del DataFrame de convocatorias.
            year_range: Lista ``[fecha_inicio, fecha_fin]`` del selector de años.
            tipo_multi_select: Lista de tipologías seleccionadas para filtrar.
            curso_multi_select: Lista de cursos seleccionados para filtrar.
        """
        clear_cache()
        logger.info("Filtros actualizados — cache invalidado")

        if stored_t1_t2 is None or stored_t4 is None or stored_conv is None:
            return None, None, None

        df_t1t2 = pd.read_json(io.StringIO(stored_t1_t2), orient='split')
        df_t4   = pd.read_json(io.StringIO(stored_t4),    orient='split')
        df_conv = pd.read_json(io.StringIO(stored_conv),  orient='split')

        if tipo_multi_select:
            df_t1t2 = df_t1t2[df_t1t2['Tipologia'].isin(tipo_multi_select)]

        if curso_multi_select:
            df_t1t2 = df_t1t2[df_t1t2['Curso'].astype(str).isin(curso_multi_select)]
            df_conv = df_conv[df_conv['Curso'].astype(str).isin(curso_multi_select)]

        if year_range and isinstance(year_range, list) and len(year_range) == 2 and all(year_range):
            start_year = pd.to_datetime(year_range[0]).year
            end_year   = pd.to_datetime(year_range[1]).year
            df_t1t2 = filter_by_year(df_t1t2, start_year, end_year)
            df_t4   = filter_by_year(df_t4,   start_year, end_year)
            df_conv = filter_by_year(df_conv,  start_year, end_year)

        return (
            df_t1t2.to_json(date_format='iso', orient='split'),
            df_t4.to_json(date_format='iso', orient='split'),
            df_conv.to_json(date_format='iso', orient='split'),
        )
