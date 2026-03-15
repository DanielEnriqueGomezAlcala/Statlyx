import pandas as pd

def clean_data_t4(tabla_4):
    df = tabla_4.rename(columns={'Unnamed: 0': 'Indicador'})
    mapeo_columnas = {
        "18   -Tasa de éxito del título": "Tasa éxito",
        "15   -Tasa de abandono del título - (IA)": "Tasa abandono",
        "17   -Tasa de rendimiento del título - (IA)": "Tasa rendimiento",
        "16   -Tasa de eficiencia de los graduados - (IA)": "Tasa eficiencia",
        "14   -Tasa de graduación del título - (IA)": "Tasa graduación"
    }
    df_filtrado = df[df['Indicador'].isin(mapeo_columnas.keys())].copy()
    df_filtrado['Indicador'] = df_filtrado['Indicador'].map(mapeo_columnas)
    df_filtrado.set_index('Indicador', inplace=True)
    df_transpuesto = df_filtrado.transpose()
    df_transpuesto.reset_index(inplace=True)
    df_transpuesto.rename(
        columns=
        {'index': 'Anio', 
        'Tasa éxito': 'Tasa_Exito', 
        'Tasa abandono': 'Tasa_Abandono', 
        'Tasa rendimiento': 'Tasa_Rendimiento', 
        'Tasa eficiencia': 'Tasa_Eficiencia', 
        'Tasa graduación': 'Tasa_Graduacion'
        }, inplace=True)
    df_transpuesto.columns.name = None 
    return df_transpuesto