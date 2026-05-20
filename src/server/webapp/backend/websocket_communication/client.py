from websockets.sync.client import connect
from ..helper.types import Request, Response


class WebSocketClient:
    def __init__(self) -> None:
        self.port: str = "5000"

    def sending(self, data: Request, ip: str) -> Response:
        uri: str = f"ws://{ip}:{self.port}"

        with connect(uri) as websocket:
            # send request
            websocket.send(data.model_dump_json())

            # wait for response
            raw = websocket.recv()
            print(raw)
            print()
            print(Response.model_validate_json(raw))

        return Response.model_validate_json(raw)
