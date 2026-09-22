"""
Función para exportar figuras Plotly a PNG y recortar espacios en blanco
"""

import io
import os
from PIL import Image, ImageChops, ImageOps

from utils.logger import get_logger

logger = get_logger(__name__)


def save_chart_image(fig, img_path, width=1200, scale=2, border=0, border_color=(180, 180, 180)):
    """
    Exporta una figura Plotly a PNG, recorta el espacio blanco inferior y opcionalmente añade un borde.

    Args:
        fig: Figura Plotly a exportar.
        img_path: Ruta de destino del archivo PNG.
        width: Anchura en píxeles de la imagen generada.
        scale: Factor de escala aplicado al exportar.
        border: Grosor del borde en píxeles. 0 para no añadir borde.
        border_color: Color RGB del borde como tupla (R, G, B).

    Returns:
        Ruta del archivo PNG.
    """
    if os.path.exists(img_path):
        logger.info("Chart cache hit: %s", os.path.basename(img_path))
        return img_path

    # Genera la imagen en formato PNG
    img_bytes = fig.to_image(format="png", width=width, scale=scale)
    img = Image.open(io.BytesIO(img_bytes)).convert("RGB")

    # Recorta el espacio blanco inferior
    white = Image.new("RGB", img.size, (255, 255, 255))
    bbox = ImageChops.difference(img, white).getbbox()
    if bbox:
        img = img.crop((0, 0, img.width, bbox[3] + 15))

    # Agregamos borde
    if border > 0:
        img = ImageOps.expand(img, border=border, fill=border_color)

    # Guardamos la imagen en la ruta especificada
    img.save(img_path)
