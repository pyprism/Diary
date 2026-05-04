import datetime

import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone
from freezegun import freeze_time
from rest_framework import status
from rest_framework.test import APIClient

from diary.models import Diary, ShareLink

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
    def _authenticated_client(email="owner@example.com", password="password"):
        user = create_user(email=email, password=password)
        api_client.force_authenticate(user=user)
        return api_client, user

    return _authenticated_client


@pytest.fixture
def diary_entry(db):
    def _make(user):
        return Diary.objects.create(
            user=user,
            title="My Entry",
            content=VALID_CONTENT,
            date=datetime.date(2024, 4, 28),
        )

    return _make


# ── Create share link ─────────────────────────────────────────────────────────


@pytest.mark.django_db
def test_create_full_share_link(authenticated_client, diary_entry):
    client, user = authenticated_client()
    diary = diary_entry(user)

    response = client.post(
        f"/api/v1/diaries/{diary.pk}/shares/",
        {"share_type": "FULL"},
        format="json",
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["share_type"] == "FULL"
    assert "token" in response.data
    assert "public_url" in response.data
    assert "expires_at" in response.data


@pytest.mark.django_db
def test_create_excerpt_share_link(authenticated_client, diary_entry):
    client, user = authenticated_client()
    diary = diary_entry(user)

    response = client.post(
        f"/api/v1/diaries/{diary.pk}/shares/",
        {"share_type": "EXCERPT", "excerpt": "Hello."},
        format="json",
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["excerpt"] == "Hello."


@pytest.mark.django_db
def test_excerpt_share_requires_excerpt_text(authenticated_client, diary_entry):
    client, user = authenticated_client()
    diary = diary_entry(user)

    response = client.post(
        f"/api/v1/diaries/{diary.pk}/shares/",
        {"share_type": "EXCERPT"},
        format="json",
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_excerpt_share_must_come_from_diary(authenticated_client, diary_entry):
    client, user = authenticated_client()
    diary = diary_entry(user)

    response = client.post(
        f"/api/v1/diaries/{diary.pk}/shares/",
        {"share_type": "EXCERPT", "excerpt": "Not in this diary."},
        format="json",
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_create_share_with_custom_expiry(authenticated_client, diary_entry):
    client, user = authenticated_client()
    diary = diary_entry(user)

    response = client.post(
        f"/api/v1/diaries/{diary.pk}/shares/",
        {"share_type": "FULL", "expiry_seconds": 3600},
        format="json",
    )
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_cannot_share_another_users_diary(
    authenticated_client, create_user, diary_entry
):
    client, _ = authenticated_client()
    other_user = create_user(email="other@example.com", password="password")
    diary = diary_entry(other_user)

    response = client.post(
        f"/api/v1/diaries/{diary.pk}/shares/",
        {"share_type": "FULL"},
        format="json",
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


# ── List / delete share links ─────────────────────────────────────────────────


@pytest.mark.django_db
def test_list_shares_for_diary(authenticated_client, diary_entry, settings):
    client, user = authenticated_client()
    diary = diary_entry(user)
    ShareLink.objects.create_share(diary, user, expiry_seconds=3600)
    ShareLink.objects.create_share(diary, user, expiry_seconds=3600)

    response = client.get(f"/api/v1/diaries/{diary.pk}/shares/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2


@pytest.mark.django_db
def test_list_all_current_user_share_links(
    authenticated_client, create_user, diary_entry
):
    client, user = authenticated_client()
    own_diary = diary_entry(user)
    other_user = create_user(email="other@example.com", password="password")
    other_diary = diary_entry(other_user)
    own_share = ShareLink.objects.create_share(own_diary, user, expiry_seconds=3600)
    ShareLink.objects.create_share(other_diary, other_user, expiry_seconds=3600)

    response = client.get("/api/v1/shares/")

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["token"] == own_share.token
    assert response.data[0]["diary_id"] == own_diary.id
    assert response.data[0]["diary_title"] == "My Entry"
    assert "public_url" in response.data[0]


@pytest.mark.django_db
def test_delete_share_link(authenticated_client, diary_entry):
    client, user = authenticated_client()
    diary = diary_entry(user)
    share = ShareLink.objects.create_share(diary, user, expiry_seconds=3600)

    response = client.delete(f"/api/v1/diaries/{diary.pk}/shares/{share.token}/")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not ShareLink.objects.filter(token=share.token).exists()


# ── Public share view ─────────────────────────────────────────────────────────


@pytest.mark.django_db
def test_public_share_view_returns_content(api_client, create_user, diary_entry):
    user = create_user(email="owner@example.com", password="password")
    diary = diary_entry(user)
    share = ShareLink.objects.create_share(diary, user, expiry_seconds=3600)

    response = api_client.get(f"/api/v1/share/{share.token}")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["diary_title"] == "My Entry"
    assert response.data["content"] == VALID_CONTENT


@pytest.mark.django_db
def test_public_share_view_returns_excerpt_only(api_client, create_user, diary_entry):
    user = create_user(email="owner@example.com", password="password")
    diary = diary_entry(user)
    share = ShareLink.objects.create_share(
        diary, user, expiry_seconds=3600, share_type="EXCERPT", excerpt="Hello."
    )

    response = api_client.get(f"/api/v1/share/{share.token}")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["content"] == "Hello."


@pytest.mark.django_db
def test_expired_share_link_returns_404(api_client, create_user, diary_entry):
    user = create_user(email="owner@example.com", password="password")
    diary = diary_entry(user)

    with freeze_time("2024-01-01"):
        share = ShareLink.objects.create_share(diary, user, expiry_seconds=60)

    # Now it's expired
    response = api_client.get(f"/api/v1/share/{share.token}")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_invalid_token_returns_404(api_client):
    response = api_client.get("/api/v1/share/nonexistent-token-xyz")
    assert response.status_code == status.HTTP_404_NOT_FOUND
