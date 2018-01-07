from django.test import TestCase, TransactionTestCase
from .models import Notes, Diary
from django.utils import timezone
from rest_framework.test import APIRequestFactory, APIClient
from django.contrib.auth.models import User
from freezegun import freeze_time
from rest_framework_jwt.views import obtain_jwt_token
import json


class ModelTest(TransactionTestCase):
    """
    Test all models
    """
    current_date_time = timezone.now()
    reset_sequences = True

    def setUp(self):
        self.tag = "Test tag"
        note = Notes.objects.create(content="test content ",
                                    iv="something random", date=self.current_date_time)
        note.tag.add(self.tag)
        diary = Diary.objects.create(title="Hello title", content="test content",
                                     iv="something random", date=self.current_date_time)
        diary.tag.add(self.tag)

    def test_notes_model(self):
        note_item = Notes.objects.all()
        self.assertEqual(note_item.count(), 1)

        note_result = Notes.objects.get(content="test content ")
        self.assertEqual(note_result.content, "test content ")

        self.assertEqual(note_result.tag.names()[0], self.tag)

    def test_diary_model(self):
        diary_item = Diary.objects.all()
        self.assertEqual(diary_item.count(), 1)

        diary_result = Diary.objects.get(title="Hello title")
        self.assertEqual(diary_result.title, "Hello title")

        self.assertEqual(diary_result.tag.names()[0], self.tag)

        self.assertEqual(diary_result.date, self.current_date_time)


# class AuthTest(TestCase):
#     """
#     Test JWT auth  (now I am thinking , do I really need this test ? :/ )
#     """
#     current_date_time = timezone.now()
#
#     def setUp(self):
#         User.objects.create_user('hiren', 'a@b.com', 'password')
#         tag = Tag.objects.create(name="Test tag")
#         Notes.objects.create(tag=tag, content="test content ", date=self.current_date_time)
#         Diary.objects.create(tag=tag, title="Hello title", content="test content", date=self.current_date_time)
#
#         self.factory = APIRequestFactory()
#
#     def test_jwt_auth(self):
#         request = self.factory.post('/api-token-auth/', {'username': 'hiren', 'password': 'password'})
#         response = obtain_jwt_token(request)
#         response.render()
#         self.assertEqual(response.status_code, 200)


class NotesViewTest(TransactionTestCase):
    """
        Test Notes View
    """
    reset_sequences = True
    current_date_time = timezone.now()
    # current_date_time = "2017-01-14T00:00:00Z"

    @freeze_time("2012-01-14")
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('hiren', 'a@b.com', 'password')
        self.client.force_authenticate(user=self.user)
        self.tag = "Test tag"
        note = Notes.objects.create(iv="random", content="test content", date=self.current_date_time)
        note.tag.add(self.tag)

    def test_login_works(self):
        response = self.client.get('/api/notes/')
        self.assertEqual(response.status_code, 200)

        self.client.logout()
        response = self.client.get('/api/notes/')
        self.assertEqual(response.status_code, 403)

    def test_return_correct_note(self):
        response = self.client.get('/api/notes/1/')
        self.assertEqual(response.json(), {'content': 'test content', 'id': 1,
                                           'tag': [self.tag], 'iv': "random",
                                           'salt': '',
                                           'date': self.current_date_time.strftime('%Y-%m-%dT%H:%M:%S.%f'),
                                           'created_at': '2012-01-14T00:00:00',
                                           'updated_at': '2012-01-14T00:00:00'})

    @freeze_time("2012-01-14")
    def test_note_update_works(self):
        response = self.client.patch('/api/notes/1/', data={'content': 'Updated content'})
        self.assertEqual(response.json(), {'content': 'Updated content', 'id': 1,
                                           'tag': [self.tag], 'iv': 'random',
                                           'salt': '',
                                           'date': self.current_date_time.strftime('%Y-%m-%dT%H:%M:%S.%f'),
                                           'created_at': '2012-01-14T00:00:00',
                                           'updated_at': '2012-01-14T00:00:00'})

    # @freeze_time("2012-01-14")
    # def test_new_note_creation_works(self):
    #     response = self.client.post('/api/notes/', data={'tag': ["xyz"], 'iv': 'random', 'content': "New content",
    #                                                      'salt': 'sa', 'date': "2012-01-14T00:00:00"}, format="json")
    #     print(response.json())
    #     self.assertEqual(response.json(), {'id': 2, 'tag': [self.tag], 'iv': 'random', 'content': "New content",
    #                                        'date': '2012-01-14T00:00:00',
    #                                        'created_at': '2012-01-14T00:00:00',
    #                                        'updated_at': '2012-01-14T00:00:00'})
    #
    # def test_deleting_note_works(self):
    #     #self.client.post('/api/notes/', data={'tag': [self.tag], 'iv': 'random', 'content': "New content !",
    #     #                                      'date': self.current_date_time})
    #     response = self.client.delete('/api/notes/1/')
    #     self.assertEqual(response.status_code, 204)
#
#
# class DiaryViewTest(TransactionTestCase):
#     """
#         Test Diary View
#     """
#     reset_sequences = True
#     current_date_time = timezone.now()
#
#     def setUp(self):
#         self.client = APIClient()
#         self.user = User.objects.create_user('hiren', 'a@b.com', 'password')
#         self.client.force_authenticate(user=self.user)
#         self.tag = "Test tag"
#         Diary.objects.create(tag=self.tag, title="Hello title", content="test content", date=self.current_date_time)
#
#     def test_login_works(self):
#         response = self.client.get('/api/diary/')
#         self.assertEqual(response.status_code, 200)
#
#         self.client.logout()
#         response = self.client.get('/api/diary/')
#         self.assertEqual(response.status_code, 403)
#
#     def test_return_correct_diary_object(self):
#         response = self.client.get('/api/diary/1/')
#         self.assertEqual(response.json(), {'content': 'test content', 'id': 1,
#                                            'tag': 1, 'title': 'Hello title', 'date': self.current_date_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')})
#
#     def test_diary_update_works(self):
#         response = self.client.patch('/api/diary/1/', data={'content': 'Updated content'})
#         self.assertEqual(response.json(), {'content': 'Updated content', 'id': 1,
#                                            'tag': 1, 'title': 'Hello title', 'date': self.current_date_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')})
#
#     def test_new_diary_creation_works(self):
#         response = self.client.post('/api/diary/', data={'tag': self.tag.id, 'content': "New content",
#                                                          'date': self.current_date_time, 'title': 'New Title'})
#         self.assertEqual(response.json(), {'id': 2, 'tag': self.tag.id, 'content': "New content",
#                                            'date': self.current_date_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ'), 'title': 'New Title' })
#
#     def test_deleting_diary_works(self):
#         self.client.post('/api/diary/', data={'tag': self.tag.id, 'content': "New content !",
#                                               'date': self.current_date_time, 'title': 'Delete me :D '})
#         response = self.client.delete('/api/diary/2/')
#         self.assertEqual(response.status_code, 204)
