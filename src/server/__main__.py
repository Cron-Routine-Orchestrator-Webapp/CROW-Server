import os
import sys
import threading
import time
from pathlib import Path
from django.core.management import execute_from_command_line

DJANGO_SETTINGS_MODULE = "server.webapp.frontend.frontend.settings"


def run_django():
    """
    Starts Django runserver in the main thread (blocking).
    """
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", DJANGO_SETTINGS_MODULE)
    path_to_manage: str = os.path.join(
        str(Path(__file__).resolve().parent), "webapp", "frontend", "manage.py"
    )

    sys.argv = [
        path_to_manage,
        "runserver",
        "0.0.0.0:8000",
    ]

    execute_from_command_line(sys.argv)


def run_cron_loop():
    """
    Runs cron in a separate thread AFTER Django is initialized.
    """
    # Import *inside* function to avoid AppRegistry/import cycle issues
    from server.webapp.backend.cron_backend.cron_clock import CronClock

    clock = CronClock()

    while True:
        try:
            clock.run()
        except Exception as e:
            print(f"[CRON ERROR] {e}")

        time.sleep(1)  # prevents CPU spin


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", DJANGO_SETTINGS_MODULE)

    # Cron runs in background thread
    cron_thread = threading.Thread(target=run_cron_loop, daemon=True)
    cron_thread.start()

    # Django runs in main thread (blocking)
    run_django()


if __name__ == "__main__":
    main()
