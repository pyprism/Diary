import pytest
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
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
def create_tag():
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
def test_diary_create(authenticated_client, create_tag):
    client, user = authenticated_client()

    tag1 = create_tag(name="test tag")

    data = {
        'title': 'Test Diary',
        'content': 'Test content',
        'tags_attach': [tag1,]
    }
    response = client.post(reverse('diaries-list'), data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['title'] == 'Test Diary'
    assert response.data['content'] == 'Test content'
    assert response.data['tags'] == [{'id': 1, 'name': 'test tag'}]


@pytest.mark.django_db
def test_diary_endpoint_without_auth(api_client):

    data = {
        'title': 'Test Diary',
        'content': 'Test content',
    }
    response = api_client.post(reverse('diaries-list'), data)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_diary_update(authenticated_client):
    client, user = authenticated_client()
    diary = Diary.objects.create(title='Test Diary', content='Test content', user=user)

    data = {
        'title': 'Test Diary update',
        'content': 'Test content update',
    }
    response = client.patch(reverse('diaries-detail', kwargs={'pk': diary.pk}), data)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['title'] == data['title']
    assert response.data['content'] == data['content']


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_diary_delete(authenticated_client):
    client, user = authenticated_client()
    diary = Diary.objects.create(title='Test Diary', content='Test content', user=user)

    response = client.delete(reverse('diaries-detail', kwargs={'pk': diary.pk}))
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_diary_detail(authenticated_client):
    client, user = authenticated_client()

    diary = Diary.objects.create(title='Test Diary', content='Test content', user=user)

    response = client.get(reverse('diaries-detail', kwargs={'pk': diary.pk}))
    assert response.status_code == status.HTTP_200_OK
    assert response.data['title'] == 'Test Diary'
    assert response.data['content'] == 'Test content'


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_tag_update_in_diary_details(authenticated_client, create_tag):
    client, user = authenticated_client()
    diary = Diary.objects.create(title='Test Diary', content='Test content', user=user)
    create_tag(email=user.email, name="tag")

    data = {
        'tags_attach': ['tag']
    }
    response = client.patch(reverse('diaries-detail', kwargs={'pk': diary.pk}), data)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['tags'] == [{'id': 1, 'name': 'tag'}]

# @pytest.mark.django_db(transaction=True, reset_sequences=True)
# def test_one_user_cannot_access_another_users_diary(authenticated_client):
#     email = f"user{get_random_string(length=8)}@example.com"
#     client_two, user_two = authenticated_client(email=email)
#     _, user = authenticated_client()
#     diary = Diary.objects.create(title='Test Diary for user 1', content='Test content for user 1', user=user)
#     print(diary.user)
#     print(user_two)
#
#     response = client_two.get(reverse('diaries-detail', kwargs={'pk': diary.pk}))
#     print(response.status_code)
#     print(response.data)
