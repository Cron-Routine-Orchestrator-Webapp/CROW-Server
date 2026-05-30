import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "frontend.settings")

django.setup()

from server.webapp.frontend.ui.models import Client  # noqa: E402


def run() -> None:
    client_id = "test_client"
    client_name = "Test Client"
    client_ip = "192.168.178.54"
    client_os = "lin"  # lin / win / mac

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
