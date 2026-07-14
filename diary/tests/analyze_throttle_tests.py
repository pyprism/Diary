import datetime

import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient, APIRequestFactory

from diary.models import Diary
from diary.views import AnalyzeThrottle

User = get_user_model()

VALID_CONTENT = {"version": 1, "blocks": [{"type": "paragraph", "text": "Hello."}]}


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_client(api_client):
    user = User.objects.create_user(email="poller@example.com", password="password")
    api_client.force_authenticate(user=user)
    return api_client, user


@pytest.fixture
def diary_entry(authenticated_client):
    _, user = authenticated_client
    return Diary.objects.create(
        user=user,
        title="Entry",
        content=VALID_CONTENT,
        date=datetime.date(2024, 4, 28),
    )


@pytest.mark.django_db
def test_analyze_get_polling_is_not_throttled(authenticated_client, diary_entry):
    client, _ = authenticated_client
    url = f"/api/v1/diaries/{diary_entry.pk}/analyze/"

    # Well past the default "user" throttle scope's 40/minute — GET must never trip it.
    for _ in range(50):
        response = client.get(url)
        assert response.status_code != status.HTTP_429_TOO_MANY_REQUESTS


@pytest.mark.django_db
def test_analyze_post_is_still_rate_limited_by_the_analyze_scope(diary_entry):
    """AnalyzeThrottle only bypasses GET; POST goes through the normal
    SimpleRateThrottle history check under the "analyze" scope."""
    user = diary_entry.user
    throttle = AnalyzeThrottle()
    throttle.THROTTLE_RATES = {"analyze": "1/minute"}
    throttle.rate = throttle.get_rate()
    throttle.num_requests, throttle.duration = throttle.parse_rate(throttle.rate)

    factory = APIRequestFactory()
    request = factory.post(f"/api/v1/diaries/{diary_entry.pk}/analyze/")
    request.user = user

    assert throttle.allow_request(request, view=None) is True
    assert throttle.allow_request(request, view=None) is False


def test_analyze_get_never_touches_the_throttle_history():
    throttle = AnalyzeThrottle()
    factory = APIRequestFactory()
    request = factory.get("/api/v1/diaries/1/analyze/")

    assert throttle.allow_request(request, view=None) is True
