import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.reverse import reverse

from diary.models import Tag

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_user():
    def _create_user(**kwargs):
        return User.objects.create_user(**kwargs)
    return _create_user


@pytest.mark.django_db
def test_create_tag(api_client, create_user):
    user = create_user(email='testuser@yo.com', password='testpass')
    api_client.force_authenticate(user=user)

    data = {
        'name': 'Test Tag'
    }

    response = api_client.post(reverse('tags-list'), data)

    assert response.status_code == status.HTTP_201_CREATED

    # Verify the tag is created and the user is correctly assigned
    tag = Tag.objects.get(name='Test Tag')
    assert tag.user == user


@pytest.mark.django_db
def test_update_tag(api_client, create_user):
    user = create_user(email='testuser@yo.com', password='<PASSWORD>')
    api_client.force_authenticate(user=user)

    data = {
        'name': 'Test Tag'
    }

    api_client.post(reverse('tags-list'), data)

    data = {
        'name': 'updated test Tag'
    }

    response = api_client.put(reverse('tags-detail', kwargs={'pk': 2}), data)

    assert response.status_code == status.HTTP_200_OK
    tag = Tag.objects.get(id=2)
    assert tag.name == 'updated test Tag'


