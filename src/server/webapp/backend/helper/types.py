from pydantic import BaseModel
from typing import Literal
import datetime


class Request(BaseModel):
    PID: int
    ACTION_TYPE: str
    COMMAND: str | None
    ARGS: list[str] | None
    ABSOLUT_PATH: str | None
    PYTHON_EXE: str | None


class Response(BaseModel):
    STATUS: str
    CODE: int
    PID: int
    ACTION_TYPE: str
    OUTPUT: str


class Client(BaseModel):
    ID: str
    NAME: str
    IP: str
    OS: str


class Job(BaseModel):
    ID: str
    ENABLED: bool
    CLIENT_ID: str
    TASK_ID: str
    TIME_TO_RUN: datetime.datetime
    REPEAT: Repeat
    LAST_RUN: datetime.datetime | None
    LAST_TASK_STATUS: str | None


class Task(BaseModel):
    ID: str
    TASK_TYPE: str | None
    TASK_PARAMETERS: TaskParameters
    CREATED_AT: datetime.datetime
    UPDATED_AT: datetime.datetime


class TaskParameters(BaseModel):
    CMD: str | None
    SHELL_CMD: str | None
    ARGS: list[str] | None
    PYTHON_FILE: str | None
    PYTHON_EXE: str | None


Repeat = Literal["None", "daily", "weekly", "2-weekly", "monthly", "yearly"]
