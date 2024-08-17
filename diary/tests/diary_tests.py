import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.reverse import reverse

from diary.models import Tag, Diary

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
def test_diary_create(authenticated_client):
    client, user = authenticated_client()

    data = {
        'title': 'Test Diary',
        'content': 'Test content',
    }
    response = client.post(reverse('diaries-list'), data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['title'] == 'Test Diary'
    assert response.data['content'] == 'Test content'


@pytest.mark.django_db
def test_diary_endpoint_without_auth(api_client):

    data = {
        'title': 'Test Diary',
        'content': 'Test content',
    }
    response = api_client.post(reverse('diaries-list'), data)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_diary_update(authenticated_client):
    client, user = authenticated_client()
    Diary.objects.create(title='Test Diary', content='Test content', user=user)

    data = {
        'title': 'Test Diary update',
        'content': 'Test content update',
    }
    response = client.patch(reverse('diaries-detail', kwargs={'pk': 2}), data)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['title'] == data['title']
    assert response.data['content'] == data['content']


@pytest.mark.django_db
def test_diary_delete(authenticated_client):
    client, user = authenticated_client()
    Diary.objects.create(title='Test Diary', content='Test content', user=user)

    response = client.delete(reverse('diaries-detail', kwargs={'pk': 3}))
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_diary_detail(authenticated_client):
    client, user = authenticated_client()

    Diary.objects.create(title='Test Diary', content='Test content', user=user)

    response = client.get(reverse('diaries-detail', kwargs={'pk': 4}))
    assert response.status_code == status.HTTP_200_OK
    assert response.data['title'] == 'Test Diary'
    assert response.data['content'] == 'Test content'


# @pytest.mark.django_db
# def test_tag_update_in_diary_details(authenticated_client):
#     client, user = authenticated_client()
#     Diary.objects.create(title='Test Diary', content='Test content', user=user)
#     Tag.objects.create(name='Test Tag', user=user)
#
#     data = {
#         'tag_attach': ['Test Tag']
#     }
#     response = client.patch(reverse('diaries-detail', kwargs={'pk': 5}), data)
#     print(response.data)
#     print(response.status_code)
#     #assert response.status_code == status.HTTP_200_OK
#     #assert response.data['tag'] == ['Test Tag']