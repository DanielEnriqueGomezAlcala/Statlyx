import pandas as pd

def clean_data_t1t2(tabla_1, tabla_2):
    # Limpiar tabla_1
    tabla_1 = tabla_1[['Ass Codnum', 'Tipologia', 'Curso']]
    tabla_1 = tabla_1.rename(columns={'Ass Codnum': 'Codigo'})
    tabla_1 = tabla_1.drop_duplicates()

    # Limpiar tabla_2
    tabla_2 = tabla_2[['Curso Aca', 'Cod Asig', 'Nummat', 'Asignatura', 'Tasa Rend', 'Tasa Exito']]
    tabla_2 = tabla_2.rename(columns=
    {'Curso Aca':'Anio', 
    'Cod Asig': 'Codigo', 
    'Nummat': 'Matriculados',
    'Tasa Rend': 'Tasa_Rendimiento',
    'Tasa Exito': 'Tasa_Exito',
    })
    tabla_2 = tabla_2.drop_duplicates()
    
    # Join Tabla_1 y Tabla_2
    df = pd.merge(tabla_1, tabla_2, on='Codigo', how='left')
    
    return df