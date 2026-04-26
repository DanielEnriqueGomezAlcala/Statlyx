"""
Definición de la llamada a la API de OpenAI.
"""

import hashlib
import os
import time

from dotenv import load_dotenv
from openai import OpenAI

from utils.logger import get_logger

load_dotenv()

logger = get_logger(__name__)

_api_key = os.getenv("OPENAI_API_KEY")
_client = OpenAI(api_key=_api_key) if _api_key else None

# Por defecto, se usa el modelo sin razonamiento si hay API key, si no "no"
llm_mode: str = "sin-razonamiento" if _api_key else "no"


def is_api_key_available() -> bool:
    """
    Devuelve True si la API key de OpenAI está configurada.
    Returns:
        bool: True si la API key está disponible, False en caso contrario.
    """
    return bool(_api_key)


MODEL_SIN_RAZONAMIENTO = "gpt-4.1-nano"
MODEL_CON_RAZONAMIENTO = "gpt-5-nano"

llm_cache: dict[str, str] = {}


def set_llm_mode(mode: str) -> None:
    """
    Cambia el modo de generación de texto y limpia el caché si el modo cambia.

    Args:
        mode: Modo de generación. Valores válidos: "no", "sin-razonamiento", "con-razonamiento".
    """
    global llm_mode
    if mode not in ("no", "sin-razonamiento", "con-razonamiento"):
        logger.warning("Modo LLM desconocido: %s — se mantiene el anterior", mode)
        return
    if mode != llm_mode:
        llm_cache.clear()
        logger.info("Modo LLM cambiado a: %s (cache limpiado)", mode)
    llm_mode = mode


SYSTEM_PROMPT = (
    "Eres un analista experto en calidad educativa universitaria. "
    "Genera conclusiones técnicas, directas y en tono académico. "
    "Responde SIEMPRE en un único párrafo continuo, sin saltos de línea, sin numeración, sin guiones."
)


def generate_text(prompt: str) -> str:
    """
    Genera un texto de análisis a partir de un prompt.

    Args:
        prompt: Texto del prompt a enviar al modelo.

    Returns:
        Texto generado por el modelo, o cadena vacía si el modo es "no".
    """
    if llm_mode == "no" or _client is None:
        return ""

    key = hashlib.md5(
        (prompt + llm_mode).encode()
    ).hexdigest()  # Se genera el hash del prompt y el modo
    if key in llm_cache:  # Si el hash está en la caché, se devuelve el texto generado
        logger.info("LLM cache hit (key=%s)", key[:8])
        return llm_cache[
            key
        ]  # Si el hash está en la caché, se devuelve el texto generado

    if llm_mode == "con-razonamiento":
        model = MODEL_CON_RAZONAMIENTO
        extra_kwargs = {"max_completion_tokens": 3000, "reasoning_effort": "low"}
    else:
        model = MODEL_SIN_RAZONAMIENTO
        extra_kwargs = {"max_tokens": 600, "temperature": 0.3}

    logger.info(
        "LLM llamada API (model=%s, modo=%s, prompt=%d chars)",
        model,
        llm_mode,
        len(prompt),
    )
    t0 = time.time()
    try:
        response = _client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            **extra_kwargs,
        )
        content = response.choices[0].message.content or ""
        content = " ".join(content.split())
        elapsed = time.time() - t0
        usage = response.usage
        logger.info(
            "LLM respuesta en %.1fs — tokens: prompt=%s, completion=%s",
            elapsed,
            usage.prompt_tokens if usage else "?",
            usage.completion_tokens if usage else "?",
        )
        if not content:
            logger.warning("LLM devolvió contenido vacío")
            return "No se pudo generar la respuesta"
        llm_cache[key] = content
        return content
    except Exception as e:
        logger.error("LLM error: %s", e)
        return f"Ha ocurrido un error: {e}"


def clear_llm_cache() -> None:
    """Vacía el caché de respuestas LLM."""
    llm_cache.clear()
    logger.info("Cache LLM limpiado")
