import hashlib
from unittest.mock import MagicMock, patch

import pytest

import functions.llm.llm as llm_module


@pytest.fixture(autouse=True)
def reset_llm_state():
    original_mode = llm_module.llm_mode
    llm_module.llm_cache.clear()
    yield
    llm_module.llm_mode = original_mode
    llm_module.llm_cache.clear()


def test_generate_text_mode_no_returns_empty():
    llm_module.llm_mode = "no"
    assert llm_module.generate_text("cualquier prompt") == ""


def test_generate_text_cache_hit_skips_api():
    llm_module.llm_mode = "sin-razonamiento"
    prompt = "prompt de prueba"
    key = hashlib.md5((prompt + "sin-razonamiento").encode()).hexdigest()
    llm_module.llm_cache[key] = "texto cacheado"

    with patch.object(llm_module, "_client") as mock_client:
        result = llm_module.generate_text(prompt)
        mock_client.chat.completions.create.assert_not_called()

    assert result == "texto cacheado"


def test_generate_text_cache_miss_calls_api_and_stores_result():
    llm_module.llm_mode = "sin-razonamiento"
    prompt = "nuevo prompt"

    mock_response = MagicMock()
    mock_response.choices[0].message.content = "respuesta generada"
    mock_response.usage.prompt_tokens = 10
    mock_response.usage.completion_tokens = 20

    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = mock_response

    with patch.object(llm_module, "_client", mock_client):
        result = llm_module.generate_text(prompt)

    assert result == "respuesta generada"
    key = hashlib.md5((prompt + "sin-razonamiento").encode()).hexdigest()
    assert llm_module.llm_cache[key] == "respuesta generada"
    mock_client.chat.completions.create.assert_called_once()


def test_generate_text_api_error_returns_error_string():
    llm_module.llm_mode = "sin-razonamiento"

    mock_client = MagicMock()
    mock_client.chat.completions.create.side_effect = Exception("conexión fallida")

    with patch.object(llm_module, "_client", mock_client):
        result = llm_module.generate_text("prompt")

    assert "Ha ocurrido un error" in result
    assert "conexión fallida" in result


def test_set_llm_mode_valid_updates_mode():
    llm_module.llm_mode = "no"
    llm_module.set_llm_mode("sin-razonamiento")
    assert llm_module.llm_mode == "sin-razonamiento"


def test_set_llm_mode_change_clears_cache():
    llm_module.llm_mode = "sin-razonamiento"
    llm_module.llm_cache["clave"] = "valor"
    llm_module.set_llm_mode("con-razonamiento")
    assert llm_module.llm_cache == {}


def test_set_llm_mode_invalid_does_not_change_state():
    llm_module.llm_mode = "sin-razonamiento"
    llm_module.llm_cache["clave"] = "valor"
    llm_module.set_llm_mode("modo-inexistente")
    assert llm_module.llm_mode == "sin-razonamiento"
    assert llm_module.llm_cache == {"clave": "valor"}


def test_clear_llm_cache_empties_dict():
    llm_module.llm_cache["a"] = "1"
    llm_module.llm_cache["b"] = "2"
    llm_module.clear_llm_cache()
    assert llm_module.llm_cache == {}
