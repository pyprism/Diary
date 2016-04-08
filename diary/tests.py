from django.test import TestCase
from .models import Tag, Notes, Diary
from django.utils import timezone
from rest_framework.test import APIRequestFactory
from django.contrib.auth.models import User
from .views import UserViewSet
from rest_framework_jwt.views import obtain_jwt_token



class ModelTest(TestCase):
    """
    Test all models
    """
    current_date_time = timezone.now()

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

        self.assertEqual(note_result.tag.id, 2)

    def test_diary_model(self):
        diary_item = Diary.objects.all()
        self.assertEqual(diary_item.count(), 1)

        diary_result = Diary.objects.get(title="Hello title")
        self.assertEqual(diary_result.title, "Hello title")

        self.assertEqual(diary_result.tag.id, 1)

        self.assertEqual(diary_result.date, self.current_date_time)


class ViewTest(TestCase):
    """
    Test all views
    """
    current_date_time = timezone.now()

    def setUp(self):
        User.objects.create_user('hiren', 'a@b.com', 'password')
        tag = Tag.objects.create(name="Test tag")
        Notes.objects.create(tag=tag, content="test content ", date=self.current_date_time)
        Diary.objects.create(tag=tag, title="Hello title", content="test content", date=self.current_date_time)

    def test_user_viewset(self):
        factory = APIRequestFactory()
        request = factory.post('/api-token-auth/', {'username': 'hiren', 'password': 'password'})
        response = obtain_jwt_token(request)
        response.render()
        self.assertEqual(response.status_code, 200)