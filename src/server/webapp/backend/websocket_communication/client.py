from typing import cast
from websockets.sync.client import connect
from ..helper.types import Request, Response


class WebSocketClient:
    def __init__(self) -> None:
        """
        **change uri for final version!**
        """
        self.port: str = "5000"

    def send_data(self, data: Request, uri: str) -> None:
        """
        Sends data on uri ( see init )\n
        via websockets
        """
        with connect(uri) as websocket:
            # websocket.send expects a DataLike (str/bytes/etc.). Normalize
            # Request to bytes or str to satisfy the type checker and runtime.
            if isinstance(data, (bytes, bytearray, memoryview)):
                message = data
            else:
                message: bytes = str(data).encode()
            websocket.send(message)

    def receive_data(self, uri: str) -> Response:
        """
        Receives data from uri ( see init )
        via websockets
        """
        with connect(uri) as websocket:
            raw_data: str | bytes = websocket.recv()
        data = raw_data.decode() if isinstance(raw_data, bytes) else raw_data
        return Response.model_validate_json(data)

    def sending(self, data: Request, ip: str) -> Response:
        uri: str = f"ws://{ip}:{self.port}"

        self.send_data(data, uri)
        return self.receive_data(uri)
