import os
import django
import uuid
from datetime import datetime

# 👉 wichtig: dein Projekt heißt "frontend"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "frontend.settings")

django.setup()

from ui.models import Job, Task


def run():
    job_id = "test_job"

    job, created = Job.objects.get_or_create(
        id=job_id,
        defaults={
            "schedule": "* * * * *",
            "enabled": True,
        },
    )

    if created:
        print("Job erstellt")
    else:
        print("Job existiert schon")

    task = Task.objects.create(
        id=str(uuid.uuid4()),
        job=job,
        status="new",
    )

    job.active_task_id = task.id
    job.last_run = datetime.utcnow()
    job.last_task_status = "new"
    job.save()

    print("Task erstellt:", task.id)


if __name__ == "__main__":
    run()