import pandas as pd

CONVOCATORIAS = {'ENE': 'Enero', 'MAR': 'Marzo', 'MAY': 'Mayo', 'JUL': 'Julio'}

def clean_data_call(df_call, df_aux):
    """Limpia y combina los datos de convocatorias con la tabla auxiliar.

    Convierte las tasas a porcentaje, normaliza nombres de columnas, mapea
    los códigos de convocatoria a nombres completos y añade el curso de la
    tabla auxiliar.

    Args:
        df_call: DataFrame con los datos de la tabla de convocatorias.
        df_aux: DataFrame auxiliar con el curso por código de asignatura.

    Returns:
        DataFrame combinado con columnas normalizadas listo para el análisis.
    """
    df_call[['Eficiencia', 'Exito']] = df_call[['Eficiencia', 'Exito']] * 100
    df_call[['Eficiencia', 'Exito']] = df_call[['Eficiencia', 'Exito']].round(2)
    df_call = df_call[['Curso', 'Convocatoria', 'Asignatura', 'Grupo', 'Cod', 'Eficiencia', 'Exito']]
    df_call = df_call.rename(columns={
        'Curso': 'Anio',
        'Convocatoria': 'Convocatoria',
        'Grupo': 'Grupo',
        'Cod': 'Codigo',
        'Eficiencia': 'Tasa_Eficiencia',
        'Exito': 'Tasa_Exito',
    })
    df_call['Convocatoria'] = df_call['Convocatoria'].map(CONVOCATORIAS)
    df_call = df_call.drop_duplicates()

    df_aux = df_aux[['Código', 'Curso']]
    df_aux = df_aux.rename(columns=
    {
        'Código': 'Codigo',
        'Curso': 'Curso',
    })

    df = pd.merge(df_call, df_aux, on='Codigo', how='left')
    return df
