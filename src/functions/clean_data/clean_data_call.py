"""
Limpieza y fusión de la tabla de convocatorias con la tabla auxiliar
"""

import pandas as pd

CONVOCATORIAS = {"ENE": "Enero", "MAR": "Marzo", "MAY": "Mayo", "JUL": "Julio"}


def clean_data_call(df_call, df_aux):
    """Limpia y combina los datos de convocatorias con la tabla auxiliar.

    Args:
        df_call: DF con los datos de la tabla de convocatorias.
        df_aux: DF auxiliar con datos extras de las asignaturas de una titulación.

    Returns:
        DF combinado con columnas normalizadas.
    """
    df_call[["Eficiencia", "Exito"]] = df_call[["Eficiencia", "Exito"]] * 100
    df_call[["Eficiencia", "Exito"]] = df_call[["Eficiencia", "Exito"]].round(2)
    # Se seleccionan las columnas necesarias de la tabla de convocatorias
    df_call = df_call[["Curso", "Convocatoria", "Asignatura", "Grupo", "Cod", "Eficiencia", "Exito"]]
    # Se renombran las columnas de la tabla de convocatorias
    df_call = df_call.rename(
        columns={
            "Curso": "Anio",
            "Convocatoria": "Convocatoria",
            "Grupo": "Grupo",
            "Cod": "Codigo",
            "Eficiencia": "Tasa_Eficiencia",
            "Exito": "Tasa_Exito",
        }
    )
    df_call["Convocatoria"] = df_call["Convocatoria"].map(CONVOCATORIAS)  # Se mapean las convocatorias a nombres completos
    df_call = df_call.drop_duplicates()  # Se eliminan duplicados

    df_aux = df_aux[["Código", "Curso"]]  # Se seleccionan las columnas necesarias de la tabla auxiliar
    # Se renombran las columnas de la tabla auxiliar
    df_aux = df_aux.rename(
        columns={
            "Código": "Codigo",
            "Curso": "Curso",
        }
    )

    df = pd.merge(df_call, df_aux, on="Codigo", how="left")  # Se unen las tablas de convocatorias y auxiliar por el codigo de asignatura
    return df
