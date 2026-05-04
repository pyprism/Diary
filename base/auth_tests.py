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
