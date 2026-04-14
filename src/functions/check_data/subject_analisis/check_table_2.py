"""
Validación de la tabla 2
"""

import pandas as pd


REQUIRED_COLUMNS = [
    "Curso Aca",
    "Cod Asig",
    "Nummat",
    "Asignatura",
    "Tasa Rend",
    "Tasa Exito",
]


def check_table_2(df: pd.DataFrame) -> bool:
    """Valida que la tabla 2 contenga las columnas requeridas.

    Args:
        df: DF con los datos de la tabla 2.

    Returns:
        True si la tabla es válida.

    Raises:
        ValueError: Si el DF está vacío o le faltan columnas requeridas.
    """
    if df.empty:
        raise ValueError(
            "La tabla 2 está vacía."
        )  # Se lanza un error si la tabla está vacía

    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(
            f"La tabla 2 no tiene las columnas requeridas: {missing}"
        )  # Se lanza un error si la tabla no tiene las columnas requeridas

    return True
