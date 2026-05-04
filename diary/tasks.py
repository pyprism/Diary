"""
Celery tasks for the diary app.

analyze_diary_task
  - Sends diary content to OpenRouter (configurable model via OPENROUTER_MODEL env var)
  - Converts Banglish blocks → Bengali script
  - Extracts mood + writes a Bengali summary
  - Saves result to DiaryAnalysis
  - Retries automatically on timeout / network errors / LLM 5xx (up to 3 times)
"""

import json
import logging

import requests
from celery import shared_task
from celery.exceptions import Retry, SoftTimeLimitExceeded
from django.conf import settings
from rest_framework import serializers

from utils.enums import Mood

logger = logging.getLogger(__name__)
RETRYABLE_HTTP_STATUS_CODES = {408, 409, 425, 429, 500, 502, 503, 504}

# Prompt

SYSTEM_PROMPT = """\
You are a multilingual assistant for a Bengali personal diary application.

The user will give you diary content as a JSON object (same structure every time):
{
  "version": <int>,
  "blocks": [
    { "type": "heading",    "level": 1|2|3, "text": "..." },
    { "type": "paragraph",  "text": "..." },
    { "type": "bullet_list","items": ["...", "..."] },
    { "type": "checklist",  "items": [{"text": "...", "checked": true|false}] },
    { "type": "quote",      "text": "..." },
    { "type": "divider" },
    { "type": "image",      "url": "..." }
  ]
}

Your THREE tasks:
1. TRANSLATE: Convert all Banglish (romanised Bengali) text into proper Bengali script (বাংলা).
   - Non-Bengali / pure English words, proper nouns and URLs stay unchanged.
   - Keep the exact same JSON structure; only modify text values.
2. MOOD: Determine the single dominant mood of the entry.
   Choose ONE of: happy | sad | nostalgic | anxious | excited | angry | calm | romantic | reflective | grateful | unknown
3. SUMMARY: Write a 2-3 sentence summary of the entry in Bengali.

Return ONLY a single valid JSON object — no markdown, no extra keys — with this exact shape:
{
  "bangla_content": { ...converted blocks JSON... },
  "mood": "<mood>",
  "summary": "<Bengali summary>"
}
"""


# Task
@shared_task(
    bind=True,
    max_retries=5,
    soft_time_limit=180,  # 3-minute soft limit → SoftTimeLimitExceeded raised
    time_limit=240,  # 4-minute hard kill
    name="diary.tasks.analyze_diary_task",
)
def analyze_diary_task(self, diary_id):
    """
    Analyse a single diary entry with the configured OpenRouter LLM.

    Args:
        diary_id: Primary key of the Diary to analyse.
    """
    # Import here to avoid circular imports at module load time
    from diary.models import Diary, DiaryAnalysis

    #  1. Fetch diary
    try:
        diary = Diary.objects.select_related("user").get(pk=diary_id)
    except Diary.DoesNotExist:
        logger.error("analyze_diary_task: Diary %s not found, aborting.", diary_id)
        return

    task_id = self.request.id or ""
    if not _is_current_task(DiaryAnalysis, diary, task_id):
        logger.info(
            "analyze_diary_task: diary %s task %s is stale, aborting.",
            diary_id,
            task_id,
        )
        return

    # 2. Mark as PROCESSING
    DiaryAnalysis.objects.set_processing(diary, task_id=task_id)

    api_key = settings.OPENROUTER_API_KEY
    if not api_key:
        logger.error("analyze_diary_task: OPENROUTER_API_KEY not configured.")
        if _is_current_task(DiaryAnalysis, diary, task_id):
            DiaryAnalysis.objects.set_failed(diary, "OPENROUTER_API_KEY is not set.")
        return

    model = settings.OPENROUTER_MODEL
    timeout = settings.OPENROUTER_TIMEOUT

    # 3. Call OpenRouter
    try:
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": json.dumps(diary.content, ensure_ascii=False),
                },
            ],
            "response_format": {"type": "json_object"},
        }

        response = requests.post(
            settings.OPENROUTER_API_URL,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://diary-app.local",
                "X-Title": "Diary App",
            },
            json=payload,
            timeout=timeout,
        )

    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as exc:
        logger.warning(
            "analyze_diary_task: network error for diary %s (attempt %s/%s): %s",
            diary_id,
            self.request.retries + 1,
            self.max_retries + 1,
            exc,
        )
        _retry_or_fail(self, DiaryAnalysis, diary, exc)
        return

    except SoftTimeLimitExceeded as exc:
        logger.warning(
            "analyze_diary_task: soft time limit exceeded for diary %s, retrying.",
            diary_id,
        )
        _retry_or_fail(self, DiaryAnalysis, diary, exc)
        return

    except Exception as exc:
        logger.exception(
            "analyze_diary_task: unexpected error for diary %s: %s", diary_id, exc
        )
        if _is_current_task(DiaryAnalysis, diary, task_id):
            DiaryAnalysis.objects.set_failed(diary, exc)
        return

    # 4. Handle HTTP errors
    if response.status_code in RETRYABLE_HTTP_STATUS_CODES:
        err = f"OpenRouter HTTP {response.status_code}: {response.text[:200]}"
        logger.warning("analyze_diary_task: %s — diary %s, retrying.", err, diary_id)
        _retry_or_fail(self, DiaryAnalysis, diary, RuntimeError(err))
        return

    if response.status_code != 200:
        err = f"OpenRouter HTTP {response.status_code}: {response.text[:500]}"
        logger.error(
            "analyze_diary_task: non-retryable error for diary %s: %s", diary_id, err
        )
        if _is_current_task(DiaryAnalysis, diary, task_id):
            DiaryAnalysis.objects.set_failed(diary, err)
        return

    # 5. Parse response
    try:
        data = response.json()
        raw_content = data["choices"][0]["message"]["content"]
        result = json.loads(raw_content)

        bangla_content = result["bangla_content"]
        mood = result.get("mood", "unknown")
        summary = result.get("summary", "")

        from diary.serializers import validate_diary_content_shape

        validate_diary_content_shape(bangla_content)
        if not isinstance(summary, str):
            raise TypeError("summary must be a string")

        # Normalise mood to allowed values
        allowed_moods = {m.value for m in Mood}
        if mood not in allowed_moods:
            mood = Mood.UNKNOWN.value

    except (
        KeyError,
        IndexError,
        json.JSONDecodeError,
        TypeError,
        serializers.ValidationError,
    ) as exc:
        err = f"Failed to parse LLM response: {exc} | raw={str(raw_content if 'raw_content' in dir() else response.text)[:300]}"
        logger.error("analyze_diary_task: %s — diary %s", err, diary_id)
        if _is_current_task(DiaryAnalysis, diary, task_id):
            DiaryAnalysis.objects.set_failed(diary, err)
        return

    #  6. Save result
    if not _is_current_task(DiaryAnalysis, diary, task_id):
        logger.info(
            "analyze_diary_task: diary %s task %s became stale before save.",
            diary_id,
            task_id,
        )
        return

    DiaryAnalysis.objects.set_done(diary, bangla_content, mood, summary)
    logger.info(
        "analyze_diary_task: diary %s analysed successfully. mood=%s", diary_id, mood
    )


#  Helpers


def _backoff(retry_count):
    """Exponential back-off: 60 s, 120 s, 240 s."""
    return 60 * (2**retry_count)


def _retry_or_fail(task, analysis_model, diary, exc):
    task_id = task.request.id or ""
    if task.request.retries >= task.max_retries:
        if _is_current_task(analysis_model, diary, task_id):
            analysis_model.objects.set_failed(diary, exc)
        return

    if _is_current_task(analysis_model, diary, task_id):
        analysis_model.objects.set_processing(diary, task_id=task_id)

    try:
        raise task.retry(exc=exc, countdown=_backoff(task.request.retries))
    except Retry:
        raise


def _is_current_task(analysis_model, diary, task_id):
    analysis = analysis_model.objects.get_for_diary(diary)
    return analysis is not None and (
        not analysis.task_id or analysis.task_id == task_id
    )
