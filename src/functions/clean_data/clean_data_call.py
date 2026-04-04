import pandas as pd

CONVOCATORIAS = {'ENE': 'Enero', 'MAR': 'Marzo', 'MAY': 'Mayo', 'JUL': 'Julio'}

def clean_data_call(df_call, df_aux):
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
