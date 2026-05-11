import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "frontend.settings")
django.setup()

from ui.models import Job, Client

class DatabaseBackend:
    def __init__(self):
        pass
    def get_clients(self):

        self.clients = list(Client.objects.all().values_list())
        
        return self.clients

    def get_jobs(self):
        self.jobs = list(Job.objects.all().values_list())
        return self.jobs
    
    