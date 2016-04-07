from django.test import TestCase
from .models import Tag, Notes, Diary
from django.utils import timezone
# Create your tests here.


class ModelTest(TestCase):

    def setUp(self):
        current_date_time = timezone.now()
        tag = Tag.objects.create(name="Test tag")
        Notes.objects.create(tag=tag, content="Uhalala Uhalla :D ", date=current_date_time)
        Diary.objects.create(tag=tag, title="Hello title", content="test content", date=current_date_time)

    def test_tag_model(self):
        tag_item = Tag.objects.all()
        self.assertEqual(tag_item.count(), 1)