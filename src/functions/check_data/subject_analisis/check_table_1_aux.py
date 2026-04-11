import pandas as pd


REQUIRED_COLUMNS = ["Código", "Cuatrimestre", "Mención"]


def check_table_1_aux(df: pd.DataFrame) -> bool:
    """Valida que la tabla auxiliar contenga las columnas requeridas.

    Args:
        df: DF con los datos de la tabla auxiliar.

    Returns:
        True si la tabla es válida.

    Raises:
        ValueError: Si el DF está vacío o le faltan columnas requeridas.
    """
    if df.empty:
        raise ValueError(
            "La tabla 1 aux está vacía."
        )  # Se lanza un error si la tabla está vacía

    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(
            f"La tabla 1 aux no tiene las columnas requeridas: {missing}"
        )  # Se lanza un error si la tabla no tiene las columnas requeridas

    return True
