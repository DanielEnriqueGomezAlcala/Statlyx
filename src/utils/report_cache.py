import os
import tempfile

from utils.logger import get_logger
from functions.llm import clear_llm_cache

logger = get_logger(__name__)

image_dir: str | None = None


def get_image_dir() -> str:
    """
    Obtiene o crea el directorio temporal persistente donde se guardan las imágenes del informe.

    Returns:
        Ruta absoluta al directorio de imágenes.
    """
    global image_dir
    if image_dir is None or not os.path.isdir(image_dir):
        image_dir = tempfile.mkdtemp(prefix="tfg_report_")
        logger.info("Directorio de imágenes creado: %s", image_dir)
    return image_dir


def clear_cache() -> None:
    """
    Invalida el directorio de imágenes y limpia el caché de LLM.
    """
    global image_dir
    image_dir = None

    clear_llm_cache()

    logger.info("Cache limpiado")
