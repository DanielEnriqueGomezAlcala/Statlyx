import pandas as pd


REQUIRED_COLUMNS = ["Ass Codnum", "Tipologia", "Curso"]


def check_table_1(df: pd.DataFrame) -> bool:
    """Valida que la tabla 1 contenga las columnas requeridas.

    Args:
        df: DataFrame con los datos de la tabla 1.

    Returns:
        ``True`` si la tabla es válida.

    Raises:
        ValueError: Si el DataFrame está vacío o le faltan columnas requeridas.
    """
    if df.empty:
        raise ValueError("La tabla 1 está vacía.")

    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"La tabla 1 no tiene las columnas requeridas: {missing}")

    return True
