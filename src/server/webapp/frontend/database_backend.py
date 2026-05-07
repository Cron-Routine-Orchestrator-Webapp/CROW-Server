import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "frontend.settings")
django.setup()

from ui.models import Job, Client

class DatabaseBackend:
    def __init__(self):
        self.clients = list(Client.objects.all().values_list())
        self.jobs = list(Job.objects.all().values_list())

    def get_clients(self):
        return self.clients

    def get_jobs(self):
        return self.jobs