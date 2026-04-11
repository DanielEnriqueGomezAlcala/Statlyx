import pandas as pd


REQUIRED_COLUMNS = ["Ass Codnum", "Tipologia", "Curso"]


def check_table_1(df: pd.DataFrame) -> bool:
    """Valida que la tabla 1 contenga las columnas requeridas.

    Args:
        df: DF con los datos de la tabla 1.

    Returns:
        True si la tabla es válida.

    Raises:
        ValueError: Si el DF está vacío o le faltan columnas requeridas.
    """
    if df.empty:
        raise ValueError(
            "La tabla 1 está vacía."
        )  # Se lanza un error si la tabla está vacía

    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(
            f"La tabla 1 no tiene las columnas requeridas: {missing}"
        )  # Se lanza un error si la tabla no tiene las columnas requeridas

    return True
