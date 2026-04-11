import pandas as pd

def clean_data_t1t2(tabla_1, tabla_2, tabla_aux):
    """Limpia y combina las tablas 1, 2 y auxiliar en un único DataFrame de asignaturas.

    Normaliza los nombres de columnas, elimina duplicados y realiza los joins necesarios
    para obtener el DataFrame con tipología, cuatrimestre, mención y tasas por asignatura.

    Args:
        tabla_1: DataFrame con los datos de tipología y curso por asignatura.
        tabla_2: DataFrame con las tasas de rendimiento y éxito por asignatura y año.
        tabla_aux: DataFrame auxiliar con cuatrimestre y mención por asignatura.

    Returns:
        DataFrame combinado con columnas normalizadas listo para el análisis.
    """
    # Limpiar tabla_1
    tabla_1 = tabla_1[['Ass Codnum', 'Tipologia', 'Curso']]
    tabla_1 = tabla_1.rename(columns={'Ass Codnum': 'Codigo'})
    tabla_1 = tabla_1.drop_duplicates()

    # Limpiar tabla_2
    tabla_2 = tabla_2[['Curso Aca', 'Cod Asig', 'Nummat', 'Asignatura', 'Tasa Rend', 'Tasa Exito']]
    tabla_2 = tabla_2.rename(columns=
    {
        'Curso Aca':'Anio', 
        'Cod Asig': 'Codigo', 
        'Nummat': 'Matriculados',
        'Tasa Rend': 'Tasa_Rendimiento',
        'Tasa Exito': 'Tasa_Exito',
    })
    tabla_2 = tabla_2.drop_duplicates()

    # Limpiar tabla_aux
    tabla_aux = tabla_aux[['Código', 'Cuatrimestre', 'Mención']]
    tabla_aux = tabla_aux.rename(columns=
    {
        'Código': 'Codigo',
        'Cuatrimestre': 'Cuatrimestre',
        'Mención': 'Mencion'
    })

    # Join Tabla_1 y Tabla_2
    df = pd.merge(tabla_1, tabla_2, on='Codigo', how='left')

    # Join Tabla_1, Tabla_2 y Tabla_aux
    df = pd.merge(df, tabla_aux, on='Codigo', how='left')

    return df