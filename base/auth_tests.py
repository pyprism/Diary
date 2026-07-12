import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.reverse import reverse

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_user():
    def _create_user(**kwargs):
        return User.objects.create_user(**kwargs)

    return _create_user


# Registration


@pytest.mark.django_db
def test_register_creates_user(api_client, settings):
    settings.REGISTRATION_OPEN = True
    data = {"email": "new@example.com", "password": "securepass1"}
    response = api_client.post(reverse("auth-register"), data)
    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.filter(email="new@example.com").exists()


@pytest.mark.django_db
def test_register_closed_returns_400(api_client, settings):
    settings.REGISTRATION_OPEN = False
    data = {"email": "new@example.com", "password": "securepass1"}
    response = api_client.post(reverse("auth-register"), data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_register_short_password_rejected(api_client, settings):
    settings.REGISTRATION_OPEN = True
    data = {"email": "new@example.com", "password": "short"}
    response = api_client.post(reverse("auth-register"), data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


# JWT Login


@pytest.mark.django_db
def test_login_returns_tokens(api_client, create_user):
    create_user(email="user@example.com", password="mypassword1")
    response = api_client.post(
        reverse("auth-login"), {"email": "user@example.com", "password": "mypassword1"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data
    assert "refresh" in response.data


@pytest.mark.django_db
def test_login_wrong_password_rejected(api_client, create_user):
    create_user(email="user@example.com", password="mypassword1")
    response = api_client.post(
        reverse("auth-login"), {"email": "user@example.com", "password": "wrong"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_me_returns_profile(api_client, create_user):
    user = create_user(email="user@example.com", password="mypassword1")
    api_client.force_authenticate(user=user)
    response = api_client.get(reverse("auth-me"))
    assert response.status_code == status.HTTP_200_OK
    assert response.data["email"] == "user@example.com"


@pytest.mark.django_db
def test_me_requires_auth(api_client):
    response = api_client.get(reverse("auth-me"))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_me_patch_sets_web_base_url(api_client, create_user):
    user = create_user(email="user@example.com", password="mypassword1")
    api_client.force_authenticate(user=user)

    response = api_client.patch(
        reverse("auth-me"),
        {"web_base_url": "https://diary.example.com/"},
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data["web_base_url"] == "https://diary.example.com"
    user.refresh_from_db()
    assert user.web_base_url == "https://diary.example.com"


@pytest.mark.django_db
def test_me_patch_ignores_read_only_fields(api_client, create_user):
    user = create_user(email="user@example.com", password="mypassword1")
    api_client.force_authenticate(user=user)

    response = api_client.patch(
        reverse("auth-me"),
        {"email": "someone-else@example.com"},
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK
    user.refresh_from_db()
    assert user.email == "user@example.com"


# Logout


@pytest.mark.django_db
def test_logout_blacklists_refresh_token(api_client, create_user):
    user = create_user(email="user@example.com", password="mypassword1")
    login_response = api_client.post(
        reverse("auth-login"), {"email": "user@example.com", "password": "mypassword1"}
    )
    refresh_token = login_response.data["refresh"]

    api_client.force_authenticate(user=user)
    logout_response = api_client.post(
        reverse("auth-logout"), {"refresh": refresh_token}, format="json"
    )
    assert logout_response.status_code == status.HTTP_205_RESET_CONTENT

    api_client.force_authenticate(user=None)
    refresh_response = api_client.post(
        reverse("auth-token-refresh"), {"refresh": refresh_token}, format="json"
    )
    assert refresh_response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_logout_requires_auth(api_client):
    response = api_client.post(reverse("auth-logout"), {"refresh": "x"}, format="json")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_logout_rejects_invalid_refresh_token(api_client, create_user):
    user = create_user(email="user@example.com", password="mypassword1")
    api_client.force_authenticate(user=user)
    response = api_client.post(
        reverse("auth-logout"), {"refresh": "not-a-real-token"}, format="json"
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
