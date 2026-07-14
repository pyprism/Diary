import datetime

import pytest
from django.contrib.auth import get_user_model

from diary.models import Diary, DiaryAnalysis
from diary.serializers import DiaryAnalysisSerializer
from utils.enums import AnalysisStatus


User = get_user_model()


@pytest.fixture
def user():
    return User.objects.create_user(
        email="analysis-status@example.com",
        password="password",
    )


@pytest.fixture
def diary(user):
    return Diary.objects.create(
        title="Analysis status",
        content={"version": 1, "blocks": [{"type": "paragraph", "text": "Hello"}]},
        user=user,
        date=datetime.date(2024, 1, 1),
    )


@pytest.mark.django_db
def test_diary_analysis_serializer_marks_retryable_failures_for_auto_retry(
    diary, settings
):
    settings.FAILED_ANALYSIS_RETRY_INTERVAL_SECONDS = 3600
    analysis = DiaryAnalysis.objects.create(
        diary=diary,
        status=AnalysisStatus.FAILED,
        error=(
            "ConnectionError: HTTPSConnectionPool(host='openrouter.ai', port=443): "
            "Max retries exceeded with url: /api/v1/chat/completions "
            "(Caused by NewConnectionError(\"HTTPSConnection(host='openrouter.ai', "
            "port=443): Failed to establish a new connection: [Errno 101] "
            'Network is unreachable"))'
        ),
    )

    data = DiaryAnalysisSerializer(analysis).data

    assert data["will_retry_automatically"] is True
    assert data["retry_after_seconds"] == 3600


@pytest.mark.django_db
def test_diary_analysis_serializer_does_not_retry_non_retryable_failures(diary):
    analysis = DiaryAnalysis.objects.create(
        diary=diary,
        status=AnalysisStatus.FAILED,
        error="Failed to parse LLM response: invalid json",
    )

    data = DiaryAnalysisSerializer(analysis).data

    assert data["will_retry_automatically"] is False
    assert data["retry_after_seconds"] is None
