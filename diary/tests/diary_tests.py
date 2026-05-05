import datetime
from io import BytesIO
from unittest.mock import Mock, patch

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from PIL import Image
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.reverse import reverse

from diary.models import Tag, Diary, DiaryAnalysis


User = get_user_model()

VALID_CONTENT = {
    "version": 1,
    "blocks": [
        {"type": "heading", "level": 1, "text": "Today"},
        {"type": "paragraph", "text": "Good day."},
    ],
}


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
    def _create_tag(email="example@example.com", **kwargs):
        user = User.objects.filter(email=email).first()
        return Tag.objects.create(user=user, **kwargs)

    return _create_tag


@pytest.fixture
def authenticated_client(api_client, create_user):
    def _authenticated_client(email="example@example.com", password="password"):
        user = create_user(email=email, password=password)
        api_client.force_authenticate(user=user)
        return api_client, user

    return _authenticated_client


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_diary_create(authenticated_client, create_tag):
    client, user = authenticated_client()
    create_tag(name="test tag")

    data = {
        "title": "Test Diary",
        "date": "01-01-2024",
        "content": VALID_CONTENT,
        "tags_attach": ["test tag"],
    }
    response = client.post(reverse("diaries-list"), data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["title"] == "Test Diary"
    assert response.data["tags"] == [{"id": 1, "name": "test tag"}]


@pytest.mark.django_db
def test_diary_endpoint_without_auth(api_client):
    data = {"title": "Test Diary", "date": "01-01-2024", "content": VALID_CONTENT}
    response = api_client.post(reverse("diaries-list"), data, format="json")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_diary_update(authenticated_client):
    client, user = authenticated_client()
    diary = Diary.objects.create(
        title="Test Diary",
        content=VALID_CONTENT,
        user=user,
        date=datetime.date(2024, 1, 1),
    )

    updated_content = {
        "version": 1,
        "blocks": [{"type": "paragraph", "text": "Updated."}],
    }
    data = {"title": "Test Diary update", "content": updated_content}
    response = client.patch(
        reverse("diaries-detail", kwargs={"pk": diary.pk}), data, format="json"
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data["title"] == "Test Diary update"


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_diary_delete(authenticated_client):
    client, user = authenticated_client()
    diary = Diary.objects.create(
        title="Test Diary",
        content=VALID_CONTENT,
        user=user,
        date=datetime.date(2024, 1, 1),
    )
    response = client.delete(reverse("diaries-detail", kwargs={"pk": diary.pk}))
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_diary_delete_removes_associated_images(authenticated_client):
    client, user = authenticated_client()
    image_url = "https://example.r2.cloudflarestorage.com/users/1/photo.jpg"
    duplicate_image_url = f"{image_url}?X-Amz-Signature=old"
    diary = Diary.objects.create(
        title="Test Diary",
        content={
            "version": 1,
            "blocks": [
                {"type": "paragraph", "text": "With image."},
                {"type": "image", "url": image_url},
                {"type": "image", "url": duplicate_image_url},
                {"type": "image", "url": "https://cdn.example.com/external.jpg"},
                {"type": "image", "url": "data:image/png;base64,abc"},
            ],
        },
        user=user,
        date=datetime.date(2024, 1, 1),
    )
    uploader = Mock()
    uploader.delete_file.return_value = True
    uploader.is_managed_url.side_effect = lambda url: (
        "example.r2.cloudflarestorage.com" in url
    )

    with patch("diary.views.get_s3_uploader", return_value=uploader):
        response = client.delete(reverse("diaries-detail", kwargs={"pk": diary.pk}))

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert uploader.delete_file.call_count == 2
    uploader.delete_file.assert_any_call(image_url)
    uploader.delete_file.assert_any_call(duplicate_image_url)
    assert not Diary.objects.filter(pk=diary.pk).exists()


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_diary_delete_keeps_entry_when_image_delete_fails(authenticated_client):
    client, user = authenticated_client()
    image_url = "https://example.r2.cloudflarestorage.com/users/1/photo.jpg"
    diary = Diary.objects.create(
        title="Test Diary",
        content={
            "version": 1,
            "blocks": [{"type": "image", "url": image_url}],
        },
        user=user,
        date=datetime.date(2024, 1, 1),
    )
    uploader = Mock()
    uploader.delete_file.return_value = False
    uploader.is_managed_url.return_value = True

    with patch("diary.views.get_s3_uploader", return_value=uploader):
        response = client.delete(reverse("diaries-detail", kwargs={"pk": diary.pk}))

    assert response.status_code == status.HTTP_502_BAD_GATEWAY
    assert Diary.objects.filter(pk=diary.pk).exists()


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_image_upload_converts_to_webp_and_uploads(authenticated_client):
    client, user = authenticated_client()
    buffer = BytesIO()
    Image.new("RGB", (1, 1), "white").save(buffer, format="PNG")
    image_bytes = buffer.getvalue()
    upload = SimpleUploadedFile("photo.png", image_bytes, content_type="image/png")
    uploader = Mock()
    uploader.upload_file.return_value = "https://example.r2/photo.webp"

    with (
        patch("diary.views.get_s3_uploader", return_value=uploader),
        patch(
            "diary.views.convert_image_to_web",
            return_value=("photo.webp", b"webp-bytes"),
        ),
    ):
        response = client.post(
            reverse("uploads-image"),
            {"image": upload},
            format="multipart",
        )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data == {
        "file_url": "https://example.r2/photo.webp",
        "filename": "photo.webp",
        "content_type": "image/webp",
    }
    uploader.upload_file.assert_called_once_with(
        b"webp-bytes",
        user_id=user.pk,
        category="diary-images",
        filename="photo.webp",
    )


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_diary_detail(authenticated_client):
    client, user = authenticated_client()
    diary = Diary.objects.create(
        title="Test Diary",
        content=VALID_CONTENT,
        user=user,
        date=datetime.date(2024, 1, 1),
    )
    response = client.get(reverse("diaries-detail", kwargs={"pk": diary.pk}))
    assert response.status_code == status.HTTP_200_OK
    assert response.data["title"] == "Test Diary"
    assert response.data["content"] == VALID_CONTENT


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_tag_update_in_diary_details(authenticated_client, create_tag):
    client, user = authenticated_client()
    diary = Diary.objects.create(
        title="Test Diary",
        content=VALID_CONTENT,
        user=user,
        date=datetime.date(2024, 1, 1),
    )
    create_tag(email=user.email, name="tag")

    data = {"tags_attach": ["tag"]}
    response = client.patch(
        reverse("diaries-detail", kwargs={"pk": diary.pk}), data, format="json"
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data["tags"] == [{"id": 1, "name": "tag"}]


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_diary_content_validation_rejects_invalid_block_type(authenticated_client):
    client, user = authenticated_client()

    bad_content = {"version": 1, "blocks": [{"type": "unknown_block", "text": "test"}]}
    data = {"title": "Bad Diary", "date": "01-01-2024", "content": bad_content}
    response = client.post(reverse("diaries-list"), data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_diary_content_validation_rejects_invalid_heading_level(authenticated_client):
    client, user = authenticated_client()

    bad_content = {
        "version": 1,
        "blocks": [{"type": "heading", "level": 5, "text": "H5?"}],
    }
    data = {"title": "Bad Diary", "date": "01-01-2024", "content": bad_content}
    response = client.post(reverse("diaries-list"), data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_diary_content_validation_rejects_image_without_url(authenticated_client):
    client, user = authenticated_client()

    bad_content = {"version": 1, "blocks": [{"type": "image"}]}
    data = {"title": "Bad Diary", "date": "01-01-2024", "content": bad_content}
    response = client.post(reverse("diaries-list"), data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db(transaction=True, reset_sequences=True)
@pytest.mark.parametrize(
    "query",
    [
        "Morning",
        "SHORT",
        "fitness",
        "Lemon",
        "energized",
        "মন",
        "happy",
        "মন happy",
        "10-01-2024",
        "2024-01-10",
    ],
)
def test_diary_list_search_across_diary_and_analysis_fields(
    authenticated_client, query
):
    client, user = authenticated_client()

    matching = Diary.objects.create(
        title="Morning Run",
        post_type="SHORT",
        content={
            "version": 1,
            "blocks": [
                {"type": "paragraph", "text": "Lemon tea and jogging in the park."}
            ],
        },
        user=user,
        date=datetime.date(2024, 1, 10),
    )
    non_matching = Diary.objects.create(
        title="Evening Notes",
        post_type="LONG",
        content={
            "version": 1,
            "blocks": [{"type": "paragraph", "text": "Project retro and deadlines."}],
        },
        user=user,
        date=datetime.date(2024, 1, 11),
    )

    fitness_tag = Tag.objects.create(user=user, name="fitness")
    work_tag = Tag.objects.create(user=user, name="work")
    matching.tags.add(fitness_tag)
    non_matching.tags.add(work_tag)

    DiaryAnalysis.objects.create(
        diary=matching,
        status="DONE",
        bangla_content={
            "version": 1,
            "blocks": [{"type": "paragraph", "text": "আজ মন ভালো ছিল।"}],
        },
        mood="happy",
        summary="Felt energized and focused.",
    )
    DiaryAnalysis.objects.create(
        diary=non_matching,
        status="DONE",
        bangla_content={
            "version": 1,
            "blocks": [{"type": "paragraph", "text": "আজ খুব ব্যস্ত ছিলাম।"}],
        },
        mood="anxious",
        summary="A stressful and overloaded day.",
    )

    response = client.get(reverse("diaries-list"), {"search": query})
    assert response.status_code == status.HTTP_200_OK

    result_ids = {entry["id"] for entry in response.data}
    assert matching.id in result_ids
    assert non_matching.id not in result_ids


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_diary_list_search_matches_diary_id(authenticated_client):
    client, user = authenticated_client()
    matching = Diary.objects.create(
        title="Target Entry",
        content=VALID_CONTENT,
        user=user,
        date=datetime.date(2024, 1, 12),
    )
    Diary.objects.create(
        title="Other Entry",
        content=VALID_CONTENT,
        user=user,
        date=datetime.date(2024, 1, 13),
    )

    response = client.get(reverse("diaries-list"), {"search": str(matching.id)})
    assert response.status_code == status.HTTP_200_OK
    assert [entry["id"] for entry in response.data] == [matching.id]
