from django.test import TestCase, TransactionTestCase
from .models import Tag, Notes, Diary
from django.utils import timezone
from rest_framework.test import APIRequestFactory, APIClient
from django.contrib.auth.models import User
from rest_framework_jwt.views import obtain_jwt_token


class ModelTest(TransactionTestCase):
    """
    Test all models
    """
    current_date_time = timezone.now()
    reset_sequences = True

    def setUp(self):
        tag = Tag.objects.create(name="Test tag")
        Notes.objects.create(tag=tag, content="test content ", date=self.current_date_time)
        Diary.objects.create(tag=tag, title="Hello title", content="test content", date=self.current_date_time)

    def test_tag_model(self):
        tag_item = Tag.objects.all()
        self.assertEqual(tag_item.count(), 1)

        tag_result = Tag.objects.get(name="Test tag")
        self.assertEqual(tag_result.name, "Test tag")

    def test_notes_model(self):
        note_item = Notes.objects.all()
        self.assertEqual(note_item.count(), 1)

        note_result = Notes.objects.get(content="test content ")
        self.assertEqual(note_result.content, "test content ")

        self.assertEqual(note_result.tag.id, 1)

    def test_diary_model(self):
        diary_item = Diary.objects.all()
        self.assertEqual(diary_item.count(), 1)

        diary_result = Diary.objects.get(title="Hello title")
        self.assertEqual(diary_result.title, "Hello title")

        self.assertEqual(diary_result.tag.id, 1)

        self.assertEqual(diary_result.date, self.current_date_time)


class AuthTest(TestCase):
    """
    Test JWT auth  (now I am thinking , do I really need this test ? :/ )
    """
    current_date_time = timezone.now()

    def setUp(self):
        User.objects.create_user('hiren', 'a@b.com', 'password')
        tag = Tag.objects.create(name="Test tag")
        Notes.objects.create(tag=tag, content="test content ", date=self.current_date_time)
        Diary.objects.create(tag=tag, title="Hello title", content="test content", date=self.current_date_time)

        self.factory = APIRequestFactory()

    def test_jwt_auth(self):
        request = self.factory.post('/api-token-auth/', {'username': 'hiren', 'password': 'password'})
        response = obtain_jwt_token(request)
        response.render()
        self.assertEqual(response.status_code, 200)


class UserViewTest(TransactionTestCase):
    """
    Test User View
    """
    reset_sequences = True

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('hiren', 'a@b.com', 'password')

    def test_login_works(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, 200)

        self.client.logout()
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, 403)

    def test_get_correct_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/users/')
        self.assertEqual(response.json(), [{'email': 'a@b.com', 'id': 1, 'username': 'hiren'}])


class TagViewTest(TransactionTestCase):
    """
        Test Tag View
    """
    reset_sequences = True

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('hiren', 'a@b.com', 'password')
        self.client.force_authenticate(user=self.user)
        tag = Tag.objects.create(name="Test tag")

    def test_login_works(self):
        response = self.client.get('/api/tags/')
        self.assertEqual(response.status_code, 200)

        self.client.logout()
        response = self.client.get('/api/tags/')
        self.assertEqual(response.status_code, 403)

    def test_return_correct_tag(self):
        response = self.client.get('/api/tags/1/')
        self.assertEqual(response.json(), {'name': 'Test tag', 'id': 1})

    def test_tag_update_works(self):
        response = self.client.patch('/api/tags/1/', data={'name': 'Updated tag'})
        self.assertEqual(response.json(), {'name': 'Updated tag', 'id': 1})

    def test_new_tag_creation_works(self):
        response = self.client.post('/api/tags/', data={'name': 'Updated tag'})
        self.assertEqual(response.json(), {'name': 'Updated tag', 'id': 2})

    def test_deleting_tag_works(self):
        self.client.post('/api/tags/', data={'name': 'New tag'})
        response = self.client.delete('/api/tags/2/')
        self.assertEqual(response.status_code, 204)


class NotesViewTest(TransactionTestCase):
    """
        Test Notes View
    """
    reset_sequences = True
    current_date_time = timezone.now()

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('hiren', 'a@b.com', 'password')
        self.client.force_authenticate(user=self.user)
        self.tag = Tag.objects.create(name="Test tag")
        Notes.objects.create(tag=self.tag, content="test content", date=self.current_date_time)

    def test_login_works(self):
        response = self.client.get('/api/notes/')
        self.assertEqual(response.status_code, 200)

        self.client.logout()
        response = self.client.get('/api/notes/')
        self.assertEqual(response.status_code, 403)

    def test_return_correct_note(self):
        response = self.client.get('/api/notes/1/')
        self.assertEqual(response.json(), {'content': 'test content', 'id': 1,
                                           'tag': 1, 'date': self.current_date_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')})

    def test_note_update_works(self):
        response = self.client.patch('/api/notes/1/', data={'content': 'Updated content'})
        self.assertEqual(response.json(), {'content': 'Updated content', 'id': 1,
                                           'tag': 1, 'date': self.current_date_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')})

    def test_new_note_creation_works(self):
        response = self.client.post('/api/notes/', data={'tag': self.tag.id, 'content': "New content",
                                                         'date': self.current_date_time})
        self.assertEqual(response.json(), {'id': 2, 'tag': self.tag.id, 'content': "New content",
                                           'date': self.current_date_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')})

    def test_deleting_note_works(self):
        self.client.post('/api/notes/', data={'tag': self.tag.id, 'content': "New content !",
                                              'date': self.current_date_time})
        response = self.client.delete('/api/notes/2/')
        self.assertEqual(response.status_code, 204)


class DiaryViewTest(TransactionTestCase):
    """
        Test Diary View
    """
    reset_sequences = True
    current_date_time = timezone.now()

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('hiren', 'a@b.com', 'password')
        self.client.force_authenticate(user=self.user)
        self.tag = Tag.objects.create(name="Test tag")
        Diary.objects.create(tag=self.tag, title="Hello title", content="test content", date=self.current_date_time)

    def test_login_works(self):
        response = self.client.get('/api/diary/')
        self.assertEqual(response.status_code, 200)

        self.client.logout()
        response = self.client.get('/api/diary/')
        self.assertEqual(response.status_code, 403)

    def test_return_correct_diary_object(self):
        response = self.client.get('/api/diary/1/')
        self.assertEqual(response.json(), {'content': 'test content', 'id': 1,
                                           'tag': 1, 'title': 'Hello title', 'date': self.current_date_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')})

    def test_diary_update_works(self):
        response = self.client.patch('/api/diary/1/', data={'content': 'Updated content'})
        self.assertEqual(response.json(), {'content': 'Updated content', 'id': 1,
                                           'tag': 1, 'title': 'Hello title', 'date': self.current_date_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')})

    def test_new_diary_creation_works(self):
        response = self.client.post('/api/diary/', data={'tag': self.tag.id, 'content': "New content",
                                                         'date': self.current_date_time, 'title': 'New Title'})
        self.assertEqual(response.json(), {'id': 2, 'tag': self.tag.id, 'content': "New content",
                                           'date': self.current_date_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ'), 'title': 'New Title' })

    def test_deleting_diary_works(self):
        self.client.post('/api/diary/', data={'tag': self.tag.id, 'content': "New content !",
                                              'date': self.current_date_time, 'title': 'Delete me :D '})
        response = self.client.delete('/api/diary/2/')
        self.assertEqual(response.status_code, 204)
