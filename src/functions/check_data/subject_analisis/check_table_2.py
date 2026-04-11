import pandas as pd


REQUIRED_COLUMNS = ["Curso Aca", "Cod Asig", "Nummat", "Asignatura", "Tasa Rend", "Tasa Exito"]


def check_table_2(df: pd.DataFrame) -> bool:
    """Valida que la tabla 2 contenga las columnas requeridas.

    Args:
        df: DataFrame con los datos de la tabla 2.

    Returns:
        ``True`` si la tabla es válida.

    Raises:
        ValueError: Si el DataFrame está vacío o le faltan columnas requeridas.
    """
    if df.empty:
        raise ValueError("La tabla 2 está vacía.")

    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"La tabla 2 no tiene las columnas requeridas: {missing}")

    return True
