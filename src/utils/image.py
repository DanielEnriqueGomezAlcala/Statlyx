import io
from PIL import Image, ImageChops, ImageOps


def save_chart_image(fig, img_path, width=1200, scale=2, border=0, border_color=(180, 180, 180)):
    """Guarda una figura Plotly como PNG.
    - Recorta el espacio blanco inferior.
    - Si border > 0, añade un borde de color uniforme alrededor (solo para líneas).

    Args:
        border: grosor del borde en píxeles. 0 = sin borde (por defecto).
        border_color: color RGB del borde, por defecto gris claro.
    """
    img_bytes = fig.to_image(format="png", width=width, scale=scale)
    img = Image.open(io.BytesIO(img_bytes)).convert('RGB')

    # Recortar espacio blanco inferior
    white = Image.new('RGB', img.size, (255, 255, 255))
    bbox = ImageChops.difference(img, white).getbbox()
    if bbox:
        img = img.crop((0, 0, img.width, bbox[3] + 15))

    # Borde opcional
    if border > 0:
        img = ImageOps.expand(img, border=border, fill=border_color)

    img.save(img_path)
