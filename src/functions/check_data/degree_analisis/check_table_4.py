import pandas as pd


REQUIRED_ROWS = [
    "18   -Tasa de éxito del título",
    "15   -Tasa de abandono del título - (IA)",
    "17   -Tasa de rendimiento del título - (IA)",
    "16   -Tasa de eficiencia de los graduados - (IA)",
    "14   -Tasa de graduación del título - (IA)",
]


def check_table_4(df: pd.DataFrame) -> bool:
    """Valida que la tabla 4 contenga las filas de indicadores requeridas.

    Args:
        df: DataFrame con los datos de la tabla 4.

    Returns:
        ``True`` si la tabla es válida.

    Raises:
        ValueError: Si el DataFrame está vacío o le faltan filas de indicadores requeridas.
    """
    if df.empty:
        raise ValueError("La tabla 4 está vacía.")

    all_values = df.astype(str).values.flatten()
    missing = [row for row in REQUIRED_ROWS if not any(row in val for val in all_values)]
    if missing:
        raise ValueError(f"La tabla 4 no contiene las filas requeridas: {missing}")

    return True
