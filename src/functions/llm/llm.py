from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
_generate = os.getenv("GENERATE_TEXT", "true").lower() != "false"

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
    "Genera conclusiones técnicas, directas y en tono académico, "
    "siguiendo estrictamente el número de líneas y el formato indicados en cada solicitud."
)


def generate_text(prompt: str) -> str:
    if not _generate:
        return _LOREM
    try:
        response = _client.chat.completions.create(
            model="gpt-4.1-nano",
            messages=[
                {"role": "system", "content": _SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            max_tokens=600,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Ha ocurrido un error: {e}"