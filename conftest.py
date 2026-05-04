"""
Root pytest conftest.

- Forces Celery to run tasks synchronously (CELERY_TASK_ALWAYS_EAGER) so tests
  never need a live RabbitMQ broker.
- Patches the OpenRouter HTTP call so the analyze task completes without
  hitting the network.
"""

import json

import pytest
from django.test import override_settings
from unittest.mock import patch, MagicMock


# Celery eager mode for all tests


@pytest.fixture(autouse=True)
def celery_eager_mode(settings):
    """Make every Celery task execute synchronously & ignore failures."""
    settings.CELERY_TASK_ALWAYS_EAGER = True
    settings.CELERY_TASK_EAGER_PROPAGATES = False


# Mock OpenRouter for all tests

MOCK_LLM_RESPONSE = {
    "bangla_content": {
        "version": 1,
        "blocks": [
            {"type": "paragraph", "text": "আজকে ভালো ছিল।"},
        ],
    },
    "mood": "happy",
    "summary": "একটি সুন্দর দিনের কথা লেখা হয়েছে।",
}


def _mock_openrouter_post(*args, **kwargs):
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "choices": [
            {"message": {"content": json.dumps(MOCK_LLM_RESPONSE, ensure_ascii=False)}}
        ]
    }
    return mock_resp


@pytest.fixture(autouse=True)
def mock_openrouter(settings):
    """Patch requests.post inside diary.tasks so no real HTTP call is made."""
    settings.OPENROUTER_API_KEY = "test-key"
    with patch("diary.tasks.requests.post", side_effect=_mock_openrouter_post):
        yield
