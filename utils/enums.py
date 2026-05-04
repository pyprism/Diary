from django.db import models


class PostType(models.TextChoices):
    SHORT = "SHORT", "Short"
    LONG = "LONG", "Long"


class ShareType(models.TextChoices):
    FULL = "FULL", "Full post"
    EXCERPT = "EXCERPT", "Text excerpt"


class AnalysisStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    PROCESSING = "PROCESSING", "Processing"
    DONE = "DONE", "Done"
    FAILED = "FAILED", "Failed"


class Mood(models.TextChoices):
    HAPPY = "happy", "Happy"
    SAD = "sad", "Sad"
    NOSTALGIC = "nostalgic", "Nostalgic"
    ANXIOUS = "anxious", "Anxious"
    EXCITED = "excited", "Excited"
    ANGRY = "angry", "Angry"
    CALM = "calm", "Calm"
    ROMANTIC = "romantic", "Romantic"
    REFLECTIVE = "reflective", "Reflective"
    GRATEFUL = "grateful", "Grateful"
    UNKNOWN = "unknown", "Unknown"
