import secrets
from datetime import timedelta

from django.db import models
from django.db.models.functions import ExtractMonth, ExtractDay
from django.utils import timezone

from utils.enums import AnalysisStatus, ShareType


class TagManager(models.Manager):
    def create_tag(self, user, name):
        return self.create(user=user, name=name)

    def get_tag(self, user, tag):
        return self.filter(user=user, name=tag).first()

    def is_tag_exists_for_user(self, user, tag):
        return self.filter(user=user, name=tag).exists()

    def get_all_tags(self, user=None):
        if user:
            return self.filter(user=user).order_by("name")
        return self.order_by("name")


class DiaryManager(models.Manager):
    def get_diary_by_tag(self, user, tag):
        return self.filter(user=user, tags__name=tag).prefetch_related("tags").all()

    def get_all_diaries(self, user=None):
        if user:
            return (
                self.filter(user=user)
                .order_by("-date")
                .select_related("user")
                .prefetch_related("tags")
            )
        return self.order_by("-date").select_related("user").prefetch_related("tags")

    def get_on_this_day(self, user, today):
        """Return entries from previous years on the same month/day as today."""
        return (
            self.filter(
                user=user,
                date__month=today.month,
                date__day=today.day,
                date__year__lt=today.year,
            )
            .order_by("-date")
            .select_related("user")
            .prefetch_related("tags")
        )

    def get_next_available_in_past_years(self, user, today):
        """
        Return entries from the next available date (in calendar order, going forward
        and wrapping around) that exists in previous years when no entries exist for
        today's month/day in past years.
        """
        current_year = today.year
        month = today.month
        day = today.day

        past_entries = self.filter(user=user, date__year__lt=current_year).annotate(
            entry_month=ExtractMonth("date"),
            entry_day=ExtractDay("date"),
        )

        # Entries after today's month/day in the calendar year
        after = past_entries.filter(
            models.Q(entry_month__gt=month)
            | models.Q(entry_month=month, entry_day__gt=day)
        ).order_by("entry_month", "entry_day")

        if after.exists():
            first = after.values("entry_month", "entry_day").first()
            return (
                self.filter(
                    user=user,
                    date__year__lt=current_year,
                    date__month=first["entry_month"],
                    date__day=first["entry_day"],
                )
                .order_by("-date")
                .select_related("user")
                .prefetch_related("tags")
            )

        # Wrap around: entries before today's month/day (start of year)
        before = past_entries.filter(
            models.Q(entry_month__lt=month)
            | models.Q(entry_month=month, entry_day__lt=day)
        ).order_by("entry_month", "entry_day")

        if before.exists():
            first = before.values("entry_month", "entry_day").first()
            return (
                self.filter(
                    user=user,
                    date__year__lt=current_year,
                    date__month=first["entry_month"],
                    date__day=first["entry_day"],
                )
                .order_by("-date")
                .select_related("user")
                .prefetch_related("tags")
            )

        return self.none()


class ShareLinkManager(models.Manager):
    def create_share(
        self, diary, user, expiry_seconds, share_type=ShareType.FULL, excerpt=""
    ):
        """Create a new share link with a secure random token."""
        token = secrets.token_urlsafe(32)
        expires_at = timezone.now() + timedelta(seconds=expiry_seconds)
        return self.create(
            diary=diary,
            created_by=user,
            token=token,
            share_type=share_type,
            excerpt=excerpt,
            expires_at=expires_at,
        )

    def get_valid(self, token):
        """Return a non-expired share link by token, or None."""
        return self.filter(token=token, expires_at__gt=timezone.now()).first()

    def get_all_for_user(self, user):
        return (
            self.filter(created_by=user).select_related("diary").order_by("-created_at")
        )

    def delete_expired(self):
        """Housekeeping: delete all expired share links."""
        return self.filter(expires_at__lte=timezone.now()).delete()


class DiaryAnalysisManager(models.Manager):
    def get_for_diary(self, diary):
        return self.filter(diary=diary).first()

    def get_or_create_for_diary(self, diary):
        """Get existing analysis or create a new PENDING one."""
        return self.get_or_create(diary=diary)

    def set_processing(self, diary, task_id):
        """Mark analysis as PROCESSING with the given Celery task id."""
        obj, _ = self.get_or_create(diary=diary)
        obj.status = AnalysisStatus.PROCESSING
        obj.task_id = task_id
        obj.error = ""
        obj.save(update_fields=["status", "task_id", "error", "updated_at"])
        return obj

    def set_done(self, diary, bangla_content, mood, summary):
        obj, _ = self.get_or_create(diary=diary)
        obj.status = AnalysisStatus.DONE
        obj.bangla_content = bangla_content
        obj.mood = mood
        obj.summary = summary
        obj.error = ""
        obj.save(
            update_fields=[
                "status",
                "bangla_content",
                "mood",
                "summary",
                "error",
                "updated_at",
            ]
        )
        return obj

    def set_failed(self, diary, error):
        obj, _ = self.get_or_create(diary=diary)
        obj.status = AnalysisStatus.FAILED
        obj.error = str(error)
        obj.save(update_fields=["status", "error", "updated_at"])
        return obj
