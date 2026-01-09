import pandas as pd
from jinja2 import Template
from datetime import datetime
import os
from pathlib import Path


def ruta_a_uri(ruta_relativa):
    return Path(ruta_relativa).resolve().as_uri()

def generate_html_report(universidad, carrera, plantilla):
    fecha_hoy = datetime.now().strftime("%d/%m/%Y")

    datos_informe = {
        "universidad": universidad,
        "carrera": carrera,
        "fecha": fecha_hoy,
        "tasa_tipo": "Rendimiento / Éxito / Evaluación",
        "tendencia_g1": "estable con ligero crecimiento en el último bienio",
        "path_g1": ruta_a_uri(f"../output/graph/G1_Resumen_{carrera}.png"),
        "path_g2": ruta_a_uri(f"../output/graph/G2_Brecha_{carrera}.png"),
        "path_g3": ruta_a_uri(f"../output/graph/G3_Velocimetro_{carrera}.png"),
        "path_g4": ruta_a_uri(f"../output/graph/G4_CompMedia_{carrera}.png"),
    }

    with open(f"../templates/{plantilla}.html", "r", encoding="utf-8") as f:
        plantilla_html = f.read()

    template = Template(plantilla_html)
    html_final = template.render(datos_informe)

    # 5. Guardar el HTML resultante (para revisar o convertir)
    with open(f"../output/informe_html/informe_{carrera}.html", "w", encoding="utf-8") as f:
        f.write(html_final)

    print(f"HTML generado para {carrera}. Ahora puedes convertirlo a PDF.")