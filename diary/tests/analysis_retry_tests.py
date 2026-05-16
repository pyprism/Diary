import datetime
from unittest.mock import patch

import pytest
from django.contrib.auth import get_user_model

from diary.models import Diary, DiaryAnalysis
from diary.tasks import _is_retryable_failure, retry_failed_diary_analyses_task
from utils.enums import AnalysisStatus


User = get_user_model()


@pytest.fixture
def user():
    return User.objects.create_user(
        email="retry@example.com",
        password="password",
    )


@pytest.fixture
def diary(user):
    return Diary.objects.create(
        title="Retry me",
        content={"version": 1, "blocks": [{"type": "paragraph", "text": "Hello"}]},
        user=user,
        date=datetime.date(2024, 1, 1),
    )


@pytest.mark.django_db
def test_retry_failed_diary_analyses_task_requeues_retryable_failures(diary):
    analysis = DiaryAnalysis.objects.create(
        diary=diary,
        status=AnalysisStatus.FAILED,
        task_id="old-task-id",
        error="OpenRouter HTTP 503: upstream unavailable",
    )

    with patch("diary.tasks.analyze_diary_task.apply_async") as mock_apply_async:
        retried = retry_failed_diary_analyses_task()

    analysis.refresh_from_db()

    assert retried == 1
    assert analysis.status == AnalysisStatus.PENDING
    assert analysis.error == ""
    assert analysis.task_id
    assert analysis.task_id != "old-task-id"
    mock_apply_async.assert_called_once_with(args=[diary.pk], task_id=analysis.task_id)


@pytest.mark.django_db
def test_retry_failed_diary_analyses_task_skips_non_retryable_failures(diary):
    analysis = DiaryAnalysis.objects.create(
        diary=diary,
        status=AnalysisStatus.FAILED,
        task_id="old-task-id",
        error="Failed to parse LLM response: invalid json",
    )

    with patch("diary.tasks.analyze_diary_task.apply_async") as mock_apply_async:
        retried = retry_failed_diary_analyses_task()

    analysis.refresh_from_db()

    assert retried == 0
    assert analysis.status == AnalysisStatus.FAILED
    assert analysis.error == "Failed to parse LLM response: invalid json"
    assert analysis.task_id == "old-task-id"
    mock_apply_async.assert_not_called()


@pytest.mark.django_db
def test_retry_failed_diary_analyses_task_keeps_failed_status_when_enqueue_fails(diary):
    analysis = DiaryAnalysis.objects.create(
        diary=diary,
        status=AnalysisStatus.FAILED,
        task_id="old-task-id",
        error="OpenRouter HTTP 429: rate limited",
    )

    with patch(
        "diary.tasks.analyze_diary_task.apply_async",
        side_effect=OSError("broker unavailable"),
    ):
        retried = retry_failed_diary_analyses_task()

    analysis.refresh_from_db()

    assert retried == 0
    assert analysis.status == AnalysisStatus.FAILED
    assert analysis.error == "Failed to dispatch analysis task: broker unavailable"


@pytest.mark.parametrize(
    ("error", "expected"),
    [
        ("OpenRouter HTTP 500: gateway failure", True),
        ("Read timed out while calling upstream", True),
        ("Connection error to upstream", True),
        ("Soft time limit exceeded", True),
        ("Failed to parse LLM response: invalid json", False),
        ("OPENROUTER_API_KEY is not set.", False),
    ],
)
def test_is_retryable_failure(error, expected):
    assert _is_retryable_failure(error) is expected
