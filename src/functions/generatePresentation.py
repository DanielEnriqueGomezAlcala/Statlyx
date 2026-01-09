from jinja2 import Template
from datetime import datetime
from pathlib import Path


def ruta_a_uri(ruta_relativa):
    return Path(ruta_relativa).resolve().as_uri()


def generate_presentation(carrera, universidad="Granada", plantilla="plantilla_presentacion"):
    """
    Genera una presentación HTML tipo diapositivas para convertir a PDF
    
    Args:
        carrera (str): Nombre de la carrera
        universidad (str): Nombre de la universidad
        plantilla (str): Nombre de la plantilla a usar (sin .html)
    """
    fecha_hoy = datetime.now().strftime("%d/%m/%Y")

    datos_presentacion = {
        "carrera": carrera,
        "universidad": universidad,
        "fecha": fecha_hoy,
        "tasa_tipo": "Rendimiento / Éxito / Evaluación",
        "tendencia_g1": "estable con ligero crecimiento en el último bienio",
        "path_g1": ruta_a_uri(f"../output/graph/G1_Resumen_{carrera}.png"),
        "path_g2": ruta_a_uri(f"../output/graph/G2_Brecha_{carrera}.png"),
        "path_g3": ruta_a_uri(f"../output/graph/G3_Velocimetro_{carrera}.png"),
        "path_g4": ruta_a_uri(f"../output/graph/G4_CompMedia_{carrera}.png"),
    }

    # Leer plantilla
    with open(f"../templates/{plantilla}.html", "r", encoding="utf-8") as f:
        plantilla_html = f.read()

    # Renderizar
    template = Template(plantilla_html)
    html_final = template.render(datos_presentacion)

    # Guardar HTML
    output_path = f"../output/informe_html/presentacion_{carrera}.html"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_final)

    print(f"✅ Presentación HTML generada: {output_path}")
    return output_path
