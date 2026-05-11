from typing import TypedDict, NotRequired


class Request(TypedDict):
    PID: int
    ACTION_TYPE: str
    COMMAND: NotRequired[str]
    ARGS: NotRequired[list[str]]
    ABSOLUT_PATH: NotRequired[str]
    PYTHON_EXE: NotRequired[str]


class Response(TypedDict):
    STATUS: str
    CODE: int
    PID: int
    ACTION_TYPE: str
    OUTPUT: str
