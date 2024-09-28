import pytest
from django.contrib.auth import get_user_model
from django.template.base import kwarg_re
from django.utils.crypto import get_random_string
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
def create_tag(create_user):
    def _create_tag(email='example@example.com', **kwargs):
        user = User.objects.filter(email=email).first()
        return Tag.objects.create(user=user, **kwargs)

    return _create_tag


@pytest.fixture
def authenticated_client(api_client, create_user):
    def _authenticated_client(email='example@example.com', password='password'):
        user = create_user(email=email, password=password)
        api_client.force_authenticate(user=user)
        return api_client, user
    return _authenticated_client


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_create_tag(authenticated_client):
    client, user = authenticated_client()

    data = {
        'name': 'Test Tag'
    }

    response = client.post(reverse('tags-list'), data)

    assert response.status_code == status.HTTP_201_CREATED

    # Verify the tag is created and the user is correctly assigned
    tag = Tag.objects.get(name='Test Tag')
    assert tag.user == user


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_update_tag(authenticated_client, create_tag):
    client, user = authenticated_client()

    tag = create_tag(name='Test Tag')

    data = {
        'name': 'updated test Tag'
    }

    response = client.put(reverse('tags-detail', kwargs={'pk': tag.id}), data)

    assert response.status_code == status.HTTP_200_OK
    tag = Tag.objects.get(id=tag.id)
    assert tag.name == 'updated test Tag'


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_delete_tag(authenticated_client, create_tag):
    client, user = authenticated_client()

    tag = create_tag(name='Test Tag')

    response = client.delete(reverse('tags-detail', kwargs={'pk': tag.pk}))
    assert response.status_code == status.HTTP_204_NO_CONTENT
    tag = Tag.objects.count()
    assert tag == 0


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_list_tags(authenticated_client, create_tag):
    client, user = authenticated_client()

    create_tag(name='Test Tag')

    response = client.get(reverse('tags-list'))
    assert response.status_code == status.HTTP_200_OK

    assert response.data['count'] == 1


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_tag_detail(authenticated_client, create_tag):
    client, user = authenticated_client()

    tag = create_tag(name='Test Tag')

    response = client.get(reverse('tags-detail', kwargs={'pk': tag.pk}))

    assert response.status_code == status.HTTP_200_OK
    assert response.data['name'] == 'Test Tag'


@pytest.mark.django_db
def test_only_authenticated_user_can_access(api_client):
    response = api_client.get(reverse('tags-list'))
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.data['detail'] == 'Authentication credentials were not provided.'


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_tag_is_unique_for_each_user(authenticated_client, create_tag):
    client, user = authenticated_client()
    create_tag(name='Test Tag')

    response = client.post(reverse('tags-list'), {'name': 'Test Tag'})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['non_field_errors'][0] == 'A tag with this name already exists for the user.'


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_one_user_cannot_access_another_users_tag(authenticated_client, create_tag):
    email = f"user{get_random_string(length=8)}@example.com"
    client_two, user_two = authenticated_client(email=email)
    client, user = authenticated_client()

    tag = create_tag(email=email, name="UserTwo Tag")

    response = client.get(reverse('tags-detail', kwargs={'pk': tag.pk}))
    assert response.status_code == 404

