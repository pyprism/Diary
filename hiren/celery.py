import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hiren.settings")

app = Celery("hiren")

# All CELERY_* settings from Django settings will be picked up automatically.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-discover tasks in INSTALLED_APPS.
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
