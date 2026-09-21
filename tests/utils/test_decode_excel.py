import base64
import io

import pandas as pd

from utils.decode_excel import decode_excel


def _excel_b64(rows, header=False) -> str:
    buf = io.BytesIO()
    pd.DataFrame(rows).to_excel(buf, index=False, header=header)
    encoded = base64.b64encode(buf.getvalue()).decode()
    mime = (
        "data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,"
    )
    return mime + encoded


def test_decodes_as_dataframe():
    contents = _excel_b64([{"A": 1, "B": 2}, {"A": 3, "B": 4}], header=True)
    result = decode_excel(contents, header=0)
    assert list(result.columns) == ["A", "B"]
    assert list(result["A"]) == [1, 3]


def test_header_selects_correct_row():
    buf = io.BytesIO()
    raw = pd.DataFrame([["ignorar", "ignorar"], ["Nombre", "Valor"], ["Ana", 10]])
    raw.to_excel(buf, index=False, header=False)
    encoded = base64.b64encode(buf.getvalue()).decode()
    mime = (
        "data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,"
    )
    contents = mime + encoded
    result = decode_excel(contents, header=1)
    assert list(result.columns) == ["Nombre", "Valor"]
