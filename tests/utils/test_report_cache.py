import os
from unittest.mock import patch

import pytest

import utils.report_cache as cache_module


@pytest.fixture(autouse=True)
def reset_cache():
    cache_module.image_dir = None
    yield
    cache_module.image_dir = None


def test_get_image_dir_creates_directory():
    path = cache_module.get_image_dir()
    assert os.path.isdir(path)


def test_get_image_dir_returns_same_dir():
    first = cache_module.get_image_dir()
    second = cache_module.get_image_dir()
    assert first == second


def test_clear_cache_invalidates_dir():
    first = cache_module.get_image_dir()
    with patch("utils.report_cache.clear_llm_cache"):
        cache_module.clear_cache()
    second = cache_module.get_image_dir()
    assert first != second
