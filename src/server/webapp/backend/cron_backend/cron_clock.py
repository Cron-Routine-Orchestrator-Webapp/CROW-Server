from datetime import datetime, timezone
from ..helper.types import Client, Job, Task, TaskParameters, Repeat, Request, Response
from ...frontend.database_backend import DatabaseBackend
from ..websocket_communication.handler import WebSocketHandler


class CronClock:
    def __init__(self) -> None:
        self.db_handler = DatabaseBackend()
        self.ws_handler = WebSocketHandler()
        self.pids: list[int] = []

    def run(self) -> None:
        self.refresh_data()
        for job in self.jobs:
            if job.ENABLED and job.TIME_TO_RUN <= datetime.now(tz=timezone.utc):
                self.run_job(job)

    def run_job(self, job: Job) -> Response:
        task: Task | None = next((t for t in self.tasks if t.ID == job.TASK_ID), None)
        self.pids.append(self.pids[-1] + 1 if self.pids else 0)  # Generate a new PID
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
            case "cmd":
                cmd: str | None = task.TASK_PARAMETERS.CMD
                if cmd is None:
                    raise ValueError(f"Command missing for Task {task.ID}")
                return self.ws_handler.run_cmd(
                    ip=client.IP, pid=pid, cmd=cmd, args=task.TASK_PARAMETERS.ARGS or []
                )
            case "shell_cmd":
                shell_cmd: str | None = task.TASK_PARAMETERS.SHELL_CMD
                if shell_cmd is None:
                    raise ValueError(f"Shell command missing for Task {task.ID}")
                return self.ws_handler.run_shell_cmd(
                    ip=client.IP, pid=pid, cmd=shell_cmd
                )
            case "python_file":
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

    def refresh_data(self) -> None:
        self.clients: list[Client] = self.db_handler.get_clients()
        self.jobs: list[Job] = self.db_handler.get_jobs()
        self.tasks: list[Task] = self.db_handler.get_tasks()
