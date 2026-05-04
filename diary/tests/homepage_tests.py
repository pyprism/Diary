import datetime

import pytest
from django.contrib.auth import get_user_model
from django.test import override_settings
from freezegun import freeze_time
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.reverse import reverse

from diary.models import Diary


User = get_user_model()

VALID_CONTENT = {"version": 1, "blocks": [{"type": "paragraph", "text": "Hello."}]}


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_user():
    def _create_user(**kwargs):
        return User.objects.create_user(**kwargs)

    return _create_user


@pytest.fixture
def authenticated_client(api_client, create_user):
    def _authenticated_client(email="example@example.com", password="password"):
        user = create_user(email=email, password=password)
        api_client.force_authenticate(user=user)
        return api_client, user

    return _authenticated_client


@pytest.mark.django_db(transaction=True, reset_sequences=True)
@freeze_time("2025-04-28")
def test_homepage_returns_on_this_day_entries(authenticated_client):
    """Entries from a previous year on the same month/day should appear."""
    client, user = authenticated_client()

    # Entry from 2 years ago on the same month/day
    Diary.objects.create(
        user=user,
        title="Memory from 2023",
        date=datetime.date(2023, 4, 28),
        content=VALID_CONTENT,
    )

    response = client.get(reverse("homepage-list"))
    assert response.status_code == status.HTTP_200_OK
    assert response.data["is_exact_date"] is True
    assert response.data["matched_date"] == {"month": 4, "day": 28}
    assert len(response.data["entries"]) == 1
    assert response.data["entries"][0]["title"] == "Memory from 2023"


@pytest.mark.django_db(transaction=True, reset_sequences=True)
@freeze_time("2025-04-28")
def test_homepage_falls_back_to_next_available(authenticated_client):
    """When no entries exist for today's month/day in past years, return the next available."""
    client, user = authenticated_client()

    # No entry on April 28 in past years; entry exists on April 30
    Diary.objects.create(
        user=user,
        title="Memory from April 30",
        date=datetime.date(2023, 4, 30),
        content=VALID_CONTENT,
    )

    response = client.get(reverse("homepage-list"))
    assert response.status_code == status.HTTP_200_OK
    assert response.data["is_exact_date"] is False
    assert response.data["matched_date"] == {"month": 4, "day": 30}
    assert len(response.data["entries"]) == 1
    assert response.data["entries"][0]["title"] == "Memory from April 30"


@pytest.mark.django_db(transaction=True, reset_sequences=True)
@freeze_time("2025-04-28")
def test_homepage_wraps_around_to_start_of_year(authenticated_client):
    """When no entries exist after today's month/day, wrap around to earlier in the year."""
    client, user = authenticated_client()

    # Only entry is before April 28
    Diary.objects.create(
        user=user,
        title="Memory from January",
        date=datetime.date(2023, 1, 15),
        content=VALID_CONTENT,
    )

    response = client.get(reverse("homepage-list"))
    assert response.status_code == status.HTTP_200_OK
    assert response.data["is_exact_date"] is False
    assert response.data["matched_date"] == {"month": 1, "day": 15}


@pytest.mark.django_db(transaction=True, reset_sequences=True)
@freeze_time("2025-04-28")
def test_homepage_returns_empty_when_no_past_entries(authenticated_client):
    """When user has no entries in past years at all, return empty list."""
    client, user = authenticated_client()

    response = client.get(reverse("homepage-list"))
    assert response.status_code == status.HTTP_200_OK
    assert response.data["entries"] == []
    assert response.data["matched_date"] is None


@pytest.mark.django_db
def test_homepage_requires_auth(api_client):
    response = api_client.get(reverse("homepage-list"))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db(transaction=True, reset_sequences=True)
@override_settings(USE_TZ=False)
@freeze_time("2025-04-28")
def test_homepage_works_with_use_tz_disabled(authenticated_client):
    client, user = authenticated_client()
    Diary.objects.create(
        user=user,
        title="Memory from 2023",
        date=datetime.date(2023, 4, 28),
        content=VALID_CONTENT,
    )

    response = client.get(reverse("homepage-list"))
    assert response.status_code == status.HTTP_200_OK
    assert response.data["is_exact_date"] is True
    assert response.data["matched_date"] == {"month": 4, "day": 28}
