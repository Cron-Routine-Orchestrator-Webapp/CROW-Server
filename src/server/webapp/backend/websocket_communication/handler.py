import subprocess
from .client import WebSocketClient
from ..helper.types import Request, Response


class WebSocketHandler:
    def __init__(self) -> None:
        self.client = WebSocketClient()

    def run_cmd(self, ip: str, pid: int, cmd: str, args: list[str]) -> Response:
        if self._ping(ip):
            request: Request = Request(
                PID=pid,
                ACTION_TYPE="cmd",
                COMMAND=cmd,
                ARGS=args,
                ABSOLUT_PATH=None,
                PYTHON_EXE=None,
            )
            return self.client.sending(data=request, ip=ip)
        else:
            raise ConnectionError(
                f"The Client {ip} is currently not availibel please check the internet connection."
            )

    def run_shell_cmd(self, ip: str, pid: int, cmd: str) -> Response:
        if self._ping(ip):
            request: Request = Request(
                PID=pid,
                ACTION_TYPE="shell_cmd",
                COMMAND=cmd,
                ARGS=None,
                ABSOLUT_PATH=None,
                PYTHON_EXE=None,
            )
            return self.client.sending(data=request, ip=ip)
        else:
            raise ConnectionError(
                f"The Client {ip} is currently not availibel please check the internet connection."
            )

    def run_python_file(
        self, ip: str, pid: int, path: str, python_exe: str = "python"
    ) -> Response:
        if self._ping(ip):
            request: Request = Request(
                PID=pid,
                ACTION_TYPE="python_file",
                COMMAND=None,
                ARGS=None,
                ABSOLUT_PATH=path,
                PYTHON_EXE=python_exe,
            )
            return self.client.sending(data=request, ip=ip)
        else:
            raise ConnectionError(
                f"The Client {ip} is currently not availibel please check the internet connection."
            )

    def _ping(self, host: str) -> bool:
        try:
            result = subprocess.run(
                ["ping", "-c", "1", host],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            return result.returncode == 0
        except Exception:
            return False
