from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from diary.managers import (
    TagManager,
    DiaryManager,
    ShareLinkManager,
    DiaryAnalysisManager,
)
from utils.enums import PostType, ShareType, AnalysisStatus, Mood


def default_diary_content():
    return {"version": 1, "blocks": []}


class Tag(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=50, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = TagManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "name"], name="unique_tag_name_per_user"
            )
        ]

    def __str__(self):
        return self.name


class Diary(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    tags = models.ManyToManyField(Tag, blank=True)
    post_type = models.CharField(
        max_length=50, choices=PostType.choices, default=PostType.LONG
    )
    content = models.JSONField(default=default_diary_content)
    date = models.DateField()  # manually selected date for the diary entry
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = DiaryManager()

    def __str__(self):
        return self.title


class ShareLink(models.Model):
    """A time-limited public share link for a diary entry (or excerpt of it)."""

    diary = models.ForeignKey(
        Diary, on_delete=models.CASCADE, related_name="share_links"
    )
    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    token = models.CharField(max_length=64, unique=True, db_index=True)
    share_type = models.CharField(
        max_length=10, choices=ShareType.choices, default=ShareType.FULL
    )
    # For EXCERPT shares – a plain-text snippet extracted by the client.
    excerpt = models.TextField(blank=True, default="")
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    objects = ShareLinkManager()

    def __str__(self):
        return f"Share({self.token[:8]}…) → {self.diary}"

    @property
    def is_expired(self):
        return timezone.now() > self.expires_at


class DiaryAnalysis(models.Model):
    """
    LLM generated analysis of a diary entry.
    One-to-one with Diary; re-triggering overwrites the previous result.
    """

    diary = models.OneToOneField(
        Diary, on_delete=models.CASCADE, related_name="analysis"
    )
    status = models.CharField(
        max_length=12,
        choices=AnalysisStatus.choices,
        default=AnalysisStatus.PENDING,
        db_index=True,
    )
    # Converted content — same block-JSON structure as Diary.content but in Bengali
    bangla_content = models.JSONField(null=True, blank=True)
    mood = models.CharField(
        max_length=20, choices=Mood.choices, default=Mood.UNKNOWN, blank=True
    )
    summary = models.TextField(blank=True, default="")
    # Celery task id for status tracking
    task_id = models.CharField(max_length=255, blank=True, default="", db_index=True)
    error = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = DiaryAnalysisManager()

    def __str__(self):
        return f"Analysis({self.diary}) [{self.status}]"
