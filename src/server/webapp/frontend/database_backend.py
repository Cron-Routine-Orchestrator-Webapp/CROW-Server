import os
import django
import datetime
from typing import Any, Literal

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "server.webapp.frontend.frontend.settings"
)
django.setup()

from django.core.exceptions import ObjectDoesNotExist  # noqa: E402
from server.webapp.frontend.ui.models import Job, Client, Task  # noqa: E402
from server.webapp.backend.helper.types import (  # noqa: E402
    Client as TypesClient,
    Job as TypesJob,
    Task as TypesTask,
    TaskParameters,
)


class DatabaseBackend:
    def __init__(self) -> None:
        pass

    def get_clients(self) -> list[TypesClient]:
        clients: list[tuple[str, str, str, str]] = list(
            Client.objects.all().values_list()
        )
        typed_clients: list[TypesClient] = []

        for client in clients:
            typed_client: TypesClient = TypesClient(
                ID=client[0], NAME=client[1], IP=client[2], OS=client[3]
            )
            typed_clients.append(typed_client)
        return typed_clients

    def get_jobs(self) -> list[TypesJob]:
        jobs: list[
            tuple[
                str,
                bool,
                str,
                str,
                datetime.datetime,
                Literal["None", "daily", "weekly", "2-weekly", "monthly", "yearly"],
                datetime.datetime | None,
                str | None,
            ]
        ] = list(Job.objects.all().values_list())
        typed_jobs: list[TypesJob] = []

        for job in jobs:
            typed_job: TypesJob = TypesJob(
                ID=job[0],
                ENABLED=job[1],
                CLIENT_ID=job[2],
                TASK_ID=job[3],
                TIME_TO_RUN=job[4],
                REPEAT=job[5],
                LAST_RUN=job[6],
                LAST_TASK_STATUS=job[7],
            )
            typed_jobs.append(typed_job)
        return typed_jobs

    def get_tasks(self) -> list[TypesTask]:
        tasks: list[
            tuple[
                str,
                str | None,
                Any,
                datetime.datetime,
                datetime.datetime,
            ]
        ] = list(Task.objects.all().values_list())
        typed_tasks: list[TypesTask] = []

        for task in tasks:
            typed_task: TypesTask = TypesTask(
                ID=task[0],
                TASK_TYPE=task[1],
                TASK_PARAMETERS=TaskParameters.model_validate(task[2]),
                CREATED_AT=task[3],
                UPDATED_AT=task[4],
            )
            typed_tasks.append(typed_task)
        return typed_tasks

    def delete_job(self, job_id: str) -> None:
        try:
            job = Job.objects.get(id=job_id)
            job.delete()
            print(f"Successfully deleted Job: {job_id}")
        except Exception as e:
            print(f"Fehler beim Aktualisieren: {e}")

    def delete_task(self, task_id: str) -> None:
        try:
            task = Task.objects.get(id=task_id)
            task.delete()
            print(f"Successfully deleted Task: {task_id}")
        except Exception as e:
            print(f"Fehler beim Aktualisieren: {e}")

    def create_new_job(
        self,
        job_id: str,
        enabled: bool,
        task_id: str,
        client_id: str,
        date_to_run: str,
        time_to_run: str,
        repeat: str,
        last_task_status: str,
    ):
        """
        Format Date and Time as follows:\n
        date =  "YYYY-MM-DD"\n
        time =  "HH:MM"
        """

        try:
            Job.objects.create(
                id=job_id,
                enabled=enabled,
                task_id=task_id,
                client_id=client_id,
                time_to_run=f"{date_to_run} {time_to_run}",
                repeat=repeat,
                last_task_status=last_task_status,
            )
            print(f"Successfully created Job:  {job_id}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def update_job(self, job_id: str, field: str, value: Any) -> None:
        try:
            job_to_update = Job.objects.get(id=job_id)
            setattr(job_to_update, field, value)
            job_to_update.save(update_fields=[field])
            print(f"Job {job_id} updatet {field} to {value}!")
        except ObjectDoesNotExist:
            print(f"{job_id} does not exist!")
        except Exception as e:
            print(f"Fehler beim Aktualisieren: {e}")


def main() -> None:
    db_backend = DatabaseBackend()
    clients: list[TypesClient] = db_backend.get_clients()
    jobs: list[TypesJob] = db_backend.get_jobs()
    tasks: list[TypesTask] = db_backend.get_tasks()

    print("Clients:", clients)
    print("Jobs:", jobs)
    print("Tasks:", tasks)


if __name__ == "__main__":
    backend = DatabaseBackend()
    backend.create_new_job(
        job_id="Neuer_Job",
        enabled=True,
        task_id="test run",
        client_id="linux-pc",
        date_to_run="2026-05-20",
        time_to_run="18:00",
        repeat="daily",
        last_task_status="",
    )
