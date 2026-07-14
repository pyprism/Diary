import datetime

import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone

from diary.models import Diary, ShareLink
from diary.tasks import purge_expired_share_links_task
from utils.enums import ShareType

User = get_user_model()

VALID_CONTENT = {"version": 1, "blocks": [{"type": "paragraph", "text": "Hello."}]}


@pytest.fixture
def user(db):
    return User.objects.create_user(email="owner@example.com", password="password")


@pytest.fixture
def diary_entry(user):
    return Diary.objects.create(
        user=user,
        title="Entry",
        content=VALID_CONTENT,
        date=datetime.date(2024, 4, 28),
    )


def _make_share_link(diary_entry, user, token, expires_at):
    return ShareLink.objects.create(
        diary=diary_entry,
        created_by=user,
        token=token,
        share_type=ShareType.FULL,
        expires_at=expires_at,
    )


@pytest.mark.django_db
def test_purge_task_deletes_only_expired_share_links(diary_entry, user):
    expired = _make_share_link(
        diary_entry, user, "expired-token", timezone.now() - datetime.timedelta(days=1)
    )
    active = _make_share_link(
        diary_entry, user, "active-token", timezone.now() + datetime.timedelta(days=1)
    )

    deleted_count = purge_expired_share_links_task()

    assert deleted_count == 1
    assert not ShareLink.objects.filter(pk=expired.pk).exists()
    assert ShareLink.objects.filter(pk=active.pk).exists()
