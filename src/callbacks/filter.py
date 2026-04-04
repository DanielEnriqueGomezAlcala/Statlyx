import io

import pandas as pd
from dash import Input, Output


def _filter_by_year(df, start_year, end_year):
    df = df.dropna(subset=['Anio']).copy()
    df["start_year"] = df["Anio"].str.extract(r'(\d{4})')[0].astype(int)
    return df[(df["start_year"] >= start_year) & (df["start_year"] <= end_year)]


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
            df_t1t2 = _filter_by_year(df_t1t2, start_year, end_year)
            df_t4   = _filter_by_year(df_t4,   start_year, end_year)
            df_conv = _filter_by_year(df_conv,  start_year, end_year)

        return (
            df_t1t2.to_json(date_format='iso', orient='split'),
            df_t4.to_json(date_format='iso', orient='split'),
            df_conv.to_json(date_format='iso', orient='split'),
        )
