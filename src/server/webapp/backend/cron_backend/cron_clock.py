from datetime import datetime, timezone, timedelta
from dateutil.relativedelta import relativedelta
from time import sleep
from ..helper.types import Client, Job, Task, TaskParameters, Request, Response
from ...frontend.database_backend import DatabaseBackend
from ..websocket_communication.handler import WebSocketHandler


class CronClock:
    def __init__(self) -> None:
        self.db_handler = DatabaseBackend()
        self.ws_handler = WebSocketHandler()
        self.pids: list[int] = []

    def run(self) -> None:

        self._refresh_data()
        for job in self.jobs:
            if job.ENABLED and job.TIME_TO_RUN <= datetime.now(tz=timezone.utc):
                try:
                    self.run_job(job)
                except Exception as e:
                    print(f"Error running job {job.ID}: {e}")
                    self.update_job_status(job, f"Error: {e}")
                else:
                    self.update_job_status(job, "Success")
        sleep(30)  # Sleep for 30 seconds before checking again

    def run_job(self, job: Job) -> Response:
        task: Task | None = next((t for t in self.tasks if t.ID == job.TASK_ID), None)
        self.pids.append(self.pids[-1] + 1 if self.pids else 100)  # Generate a new PID
        pid: int = self.pids[-1]
        if task is None:
            raise ValueError(f"Task with ID {job.TASK_ID} not found for Job {job.ID}")

        client: Client | None = next(
            (c for c in self.clients if c.ID == job.CLIENT_ID), None
        )
        if client is None:
            raise ValueError(
                f"Client with ID {job.CLIENT_ID} not found for Job {job.ID}"
            )

        match task.TASK_TYPE:
            case "command":
                cmd: str | None = task.TASK_PARAMETERS.CMD
                if cmd is None:
                    raise ValueError(f"Command missing for Task {task.ID}")
                return self.ws_handler.run_cmd(
                    ip=client.IP, pid=pid, cmd=cmd, args=task.TASK_PARAMETERS.ARGS or []
                )
            case "shell_command":
                shell_cmd: str | None = task.TASK_PARAMETERS.SHELL_CMD
                if shell_cmd is None:
                    raise ValueError(f"Shell command missing for Task {task.ID}")
                return self.ws_handler.run_shell_cmd(
                    ip=client.IP, pid=pid, cmd=shell_cmd
                )
            case "python":
                python_file: str | None = task.TASK_PARAMETERS.PYTHON_FILE
                if python_file is None:
                    raise ValueError(f"Python file path missing for Task {task.ID}")
                return self.ws_handler.run_python_file(
                    ip=client.IP,
                    pid=pid,
                    path=python_file,
                    python_exe=task.TASK_PARAMETERS.PYTHON_EXE or "python",
                )
            case _:
                raise ValueError(
                    f"Unknown task type {task.TASK_TYPE} for Task {task.ID}"
                )

    def update_job_status(self, job: Job, status: str) -> None:
        try:
            self.db_handler.update_job(
                job.ID, "last_run", datetime.now(tz=timezone.utc)
            )
            self.db_handler.update_job(job.ID, "last_task_status", status)
            self.check_for_repeats(job)
            print(f"Successfully updated Job: {job.ID} with status: {status}")
        except Exception as e:
            print(f"Fehler beim Aktualisieren: {e}")

    def check_for_repeats(self, job: Job) -> None:
        match job.REPEAT:
            case "None":
                self.db_handler.update_job(job.ID, "enabled", False)
            case "daily":
                next_run: datetime = job.TIME_TO_RUN + timedelta(days=1)
                self.db_handler.update_job(job.ID, "time_to_run", next_run)
            case "weekly":
                next_run: datetime = job.TIME_TO_RUN + timedelta(weeks=1)
                self.db_handler.update_job(job.ID, "time_to_run", next_run)
            case "2-weekly":
                next_run: datetime = job.TIME_TO_RUN + timedelta(weeks=2)
                self.db_handler.update_job(job.ID, "time_to_run", next_run)
            case "monthly":
                next_run: datetime = job.TIME_TO_RUN + relativedelta(months=1)
                self.db_handler.update_job(job.ID, "time_to_run", next_run)
            case "yearly":
                next_run: datetime = job.TIME_TO_RUN + relativedelta(years=1)
                self.db_handler.update_job(job.ID, "time_to_run", next_run)
            case _:
                return  # No repeat, do nothing

    def _refresh_data(self) -> None:
        self.clients: list[Client] = self.db_handler.get_clients()
        self.jobs: list[Job] = self.db_handler.get_jobs()
        self.tasks: list[Task] = self.db_handler.get_tasks()
