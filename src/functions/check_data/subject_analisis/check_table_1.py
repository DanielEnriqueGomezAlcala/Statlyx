import pandas as pd


REQUIRED_COLUMNS = ["Ass Codnum", "Tipologia", "Curso"]


def check_table_1(df: pd.DataFrame) -> bool:
    if df.empty:
        raise ValueError("La tabla 1 está vacía.")

    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"La tabla 1 no tiene las columnas requeridas: {missing}")

    return True
