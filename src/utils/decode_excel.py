import base64
import io

import pandas as pd

def decode_excel(contents, header) -> pd.DataFrame:
    """Decodifica un archivo Excel en base64 y lo carga como DataFrame.

    Args:
        contents: Contenido del archivo en formato base64 (data URI de Dash).
        header: Índice de la fila que contiene las cabeceras.

    Returns:
        DataFrame con el contenido del archivo Excel.
    """
    _, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    return pd.read_excel(io.BytesIO(decoded), header=header)