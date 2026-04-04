import pandas as pd


REQUIRED_COLUMNS = ["Curso", "Convocatoria", "Grupo", "Cod", "Eficiencia", "Exito"]


def check_table_call(df: pd.DataFrame) -> bool:
    if df.empty:
        raise ValueError("La tabla de convocatorias está vacía.")

    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"La tabla de convocatorias no tiene las columnas requeridas: {missing}")

    return True