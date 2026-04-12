import pandas as pd


def filter_by_year(df, start_year, end_year) -> pd.DataFrame:
    """
    Filtra un DF por rango de años a partir de la columna Anio.

    Args:
        df: DF con los datos a filtrar.
        start_year: Año de inicio.
        end_year: Año de fin.

    Returns:
        DF filtrado con las filas cuyo año esté dentro del rango.
    """
    df = df.dropna(subset=["Anio"]).copy()
    df["start_year"] = df["Anio"].str.extract(r"(\d{4})")[0].astype(int)
    return df[(df["start_year"] >= start_year) & (df["start_year"] <= end_year)]
