from django.db import models

class Job(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    schedule = models.CharField(max_length=255)
    enabled = models.BooleanField(default=True)

    last_run = models.DateTimeField(null=True, blank=True)
    last_task_status = models.CharField(max_length=50, null=True, blank=True)
    active_task_id = models.CharField(max_length=255, null=True, blank=True)


class Task(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)

    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)