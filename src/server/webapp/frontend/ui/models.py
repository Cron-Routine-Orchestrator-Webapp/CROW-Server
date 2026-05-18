from django.db import models

class Job(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    
    enabled = models.BooleanField(default=True)
    
    client_id = models.CharField(max_length=255, null=False, blank=True)

    task_id = models.CharField(max_length=255, null=False, blank=True)

    time_to_run = models.DateTimeField(null=False, blank=True,default=1)

    last_run = models.DateTimeField(null=True, blank=True)
    
    last_task_status = models.CharField(max_length=50, null=True, blank=True)


class Task(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    #job = models.ForeignKey(Job, on_delete=models.CASCADE)
    task_type = models.CharField(max_length=255,default = None, null=True, blank=True)
    task_data = models.JSONField(default=dict, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class Client(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    ip = models.GenericIPAddressField()
    os = models.CharField(max_length=255)