import pandas as pd
import pytest

from functions.clean_data.clean_data_call import clean_data_call
from functions.clean_data.clean_data_t1t2 import clean_data_t1t2
from functions.clean_data.clean_data_t4 import clean_data_t4


@pytest.fixture
def tabla_1():
    return pd.DataFrame(
        {
            "Ass Codnum": [139261011, 139261012, 139261013],
            "Tipologia": ["FORMACIÓN BÁSICA", "FORMACIÓN BÁSICA", "OBLIGATORIA"],
            "Curso": [1, 1, 2],
        }
    )


@pytest.fixture
def tabla_2():
    return pd.DataFrame(
        {
            "Curso Aca": ["2022-23", "2023-24", "2024-25"],
            "Cod Asig": [139261011, 139261012, 139261013],
            "Nummat": [340, 429, 478],
            "Asignatura": ["INFORMÁTICA BÁSICA", "ÁLGEBRA", "CÁLCULO"],
            "Tasa Rend": [72.4, 68.1, 75.3],
            "Tasa Exito": [89.2, 82.5, 91.0],
        }
    )


@pytest.fixture
def tabla_aux():
    return pd.DataFrame(
        {
            "Código": [139261011, 139261012, 139261013],
            "Cuatrimestre": [1, 1, 2],
            "Mención": ["No aplica", "No aplica", "No aplica"],
            "Curso": [1, 1, 2],
        }
    )


@pytest.fixture
def tabla_4():
    rows = [
        "18   -Tasa de éxito del título",
        "15   -Tasa de abandono del título - (IA)",
        "17   -Tasa de rendimiento del título - (IA)",
        "16   -Tasa de eficiencia de los graduados - (IA)",
        "14   -Tasa de graduación del título - (IA)",
    ]
    return pd.DataFrame(
        {
            "Unnamed: 0": rows,
            "2020-21": [90.0, 21.7, 65.4, 81.2, 35.5],
            "2021-22": [88.7, 17.7, 65.8, 83.4, None],
            "2022-23": [89.1, 16.6, 67.2, 81.4, None],
        }
    )


@pytest.fixture
def tabla_call():
    return pd.DataFrame(
        {
            "Curso": ["2022-2023", "2022-2023", "2022-2023"],
            "Convocatoria": ["ENE", "MAY", "JUL"],
            "Asignatura": ["INFORMÁTICA BÁSICA", "ÁLGEBRA", "CÁLCULO"],
            "Grupo": [1, 1, 1],
            "Cod": [139261011, 139261012, 139261013],
            "Eficiencia": [0.724, 0.681, 0.753],
            "Exito": [0.892, 0.825, 0.910],
        }
    )


@pytest.fixture
def df_subjects(tabla_1, tabla_2, tabla_aux):
    return clean_data_t1t2(tabla_1, tabla_2, tabla_aux)


@pytest.fixture
def df_degrees(tabla_4):
    return clean_data_t4(tabla_4)


@pytest.fixture
def df_call(tabla_call, tabla_aux):
    return clean_data_call(tabla_call, tabla_aux)
