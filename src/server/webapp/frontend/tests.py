import os
import django
import uuid
from datetime import datetime

# 👉 wichtig: dein Projekt heißt "frontend"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "frontend.settings")

django.setup()

from ui.models import Job, Task, Client


def run():
    client_id = "test_client"
    client_name = "Test Client"
    client_ip = "192.168.178.54"
    client_os = "lin" # lin / win / mac
    
    client, created = Client.objects.get_or_create(
        id=client_id,
        defaults={
            "id": client_id,
            "name": client_name,
            "ip": client_ip,
            "os": client_os,
        },
    )
    


    if created:
        print("Client gespeichert:", client.id)


if __name__ == "__main__":
    run()