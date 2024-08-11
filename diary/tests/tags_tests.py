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


@pytest.fixture
def authenticated_client(api_client, create_user):
    def _authenticated_client(email='testuser@yo.com', password='testpass'):
        user = create_user(email=email, password=password)
        api_client.force_authenticate(user=user)
        return api_client, user
    return _authenticated_client


@pytest.mark.django_db
def test_create_tag(api_client, create_user, authenticated_client):
    client, user = authenticated_client()

    data = {
        'name': 'Test Tag'
    }

    response = api_client.post(reverse('tags-list'), data)

    assert response.status_code == status.HTTP_201_CREATED

    # Verify the tag is created and the user is correctly assigned
    tag = Tag.objects.get(name='Test Tag')
    assert tag.user == user


@pytest.mark.django_db
def test_update_tag(api_client, create_user, authenticated_client):
    authenticated_client()

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


@pytest.mark.django_db
def test_delete_tag(api_client, create_user, authenticated_client):
    authenticated_client()

    data = {
        'name': 'Test Tag'
    }
    api_client.post(reverse('tags-list'), data)

    response = api_client.delete(reverse('tags-detail', kwargs={'pk': 3}))
    assert response.status_code == status.HTTP_204_NO_CONTENT
    tag = Tag.objects.filter(id=2).count()
    assert tag == 0


@pytest.mark.django_db
def test_list_tags(api_client, create_user, authenticated_client):
    authenticated_client()

    data = {
        'name': 'Test Tag'
    }
    api_client.post(reverse('tags-list'), data)

    response = api_client.get(reverse('tags-list'))
    assert response.status_code == status.HTTP_200_OK

    assert response.data['count'] == 1


@pytest.mark.django_db
def test_tag_detail(api_client, create_user, authenticated_client):
    authenticated_client()

    data = {
        'name': 'Test Tag'
    }

    api_client.post(reverse('tags-list'), data)

    response = api_client.get(reverse('tags-detail', kwargs={'pk': 5}))

    assert response.status_code == status.HTTP_200_OK
    assert response.data['name'] == 'Test Tag'


@pytest.mark.django_db
def test_only_authenticated_user_can_access(api_client, create_user):
    response = api_client.get(reverse('tags-list'))
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.data['detail'] == 'Authentication credentials were not provided.'


@pytest.mark.django_db
def test_tag_is_unique_for_each_user(api_client, create_user, authenticated_client):
    authenticated_client()

    data = {
        'name': 'Test Tag'
    }

    api_client.post(reverse('tags-list'), data)
    response = api_client.post(reverse('tags-list'), data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['non_field_errors'][0] == 'A tag with this name already exists for the user.'



