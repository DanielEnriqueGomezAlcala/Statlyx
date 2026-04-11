import hashlib
import os
import time

from dotenv import load_dotenv
from openai import OpenAI

from utils.logger import get_logger

load_dotenv()

logger = get_logger(__name__)

_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Modo activo: "no" | "sin-razonamiento" | "con-razonamiento"
_llm_mode: str = "sin-razonamiento"

_MODEL_SIN_RAZONAMIENTO = "gpt-4.1-nano"
_MODEL_CON_RAZONAMIENTO = "gpt-5-nano"

_llm_cache: dict[str, str] = {}


def set_llm_mode(mode: str) -> None:
    """Cambia el modo de generación de texto y limpia el caché si el modo cambia.

    Args:
        mode: Modo de generación. Valores válidos: ``"no"``, ``"sin-razonamiento"``,
            ``"con-razonamiento"``.
    """
    global _llm_mode
    if mode not in ("no", "sin-razonamiento", "con-razonamiento"):
        logger.warning("Modo LLM desconocido: %s — se mantiene el anterior", mode)
        return
    if mode != _llm_mode:
        _llm_cache.clear()
        logger.info("Modo LLM cambiado a: %s (cache limpiado)", mode)
    _llm_mode = mode

_LOREM = (
    "Lorem ipsum dolor sit amet consectetur adipiscing elit velit eros suspendisse tempor, "
    "senectus consequat porttitor suscipit dictum maecenas mi ligula phasellus commodo justo laoreet, "
    "orci arcu scelerisque condimentum tincidunt mattis aliquam natoque nisl venenatis. "
    "Pretium dis ultrices fames nibh nostra cubilia integer, mi cum molestie commodo faucibus tortor, "
    "lobortis feugiat venenatis at vulputate ullamcorper. Suspendisse dictumst nibh phasellus ac conubia "
    "parturient turpis netus, metus justo dictum integer ligula duis rhoncus nisi, bibendum nostra "
    "elementum taciti laoreet quis tortor."
)

_SYSTEM_PROMPT = (
    "Eres un analista experto en calidad educativa universitaria. "
    "Genera conclusiones técnicas, directas y en tono académico. "
    "Responde SIEMPRE en un único párrafo continuo, sin saltos de línea, sin numeración, sin guiones."
)


def generate_text(prompt: str) -> str:
    """Genera un texto de análisis a partir de un prompt usando la API de OpenAI.

    Aplica caché en memoria basado en el hash del prompt y el modo activo.
    Si el modo es ``"no"`` devuelve un texto Lorem Ipsum sin realizar llamadas a la API.

    Args:
        prompt: Texto del prompt a enviar al modelo.

    Returns:
        Texto generado por el modelo, o Lorem Ipsum si el modo es ``"no"``.
    """
    if _llm_mode == "no":
        return _LOREM

    key = hashlib.md5((prompt + _llm_mode).encode()).hexdigest()
    if key in _llm_cache:
        logger.info("LLM cache hit (key=%s)", key[:8])
        return _llm_cache[key]

    if _llm_mode == "con-razonamiento":
        model = _MODEL_CON_RAZONAMIENTO
        extra_kwargs = {"max_completion_tokens": 3000, "reasoning_effort": "low"}
    else:
        model = _MODEL_SIN_RAZONAMIENTO
        extra_kwargs = {"max_tokens": 600, "temperature": 0.3}

    logger.info("LLM llamada API (model=%s, modo=%s, prompt=%d chars)", model, _llm_mode, len(prompt))
    t0 = time.time()
    try:
        response = _client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": _SYSTEM_PROMPT},
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
        _llm_cache[key] = content
        return content
    except Exception as e:
        logger.error("LLM error: %s", e)
        return f"Ha ocurrido un error: {e}"


def clear_llm_cache() -> None:
    """Vacía el caché de respuestas LLM."""
    _llm_cache.clear()
    logger.info("Cache LLM limpiado")
