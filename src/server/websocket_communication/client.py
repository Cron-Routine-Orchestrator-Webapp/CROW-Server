from websockets.sync.client import connect
from .helper.types import Request, Response

class WebSocketClient:
    def __init__(self):
        """
        **change uri for final version!**
        """
        self.port: str = "5000"

    def send_data(self, data: Request, uri: str) -> None:
        """
        Sends data on uri ( see init )\n
        via websockets
        """
        with connect(uri) as weboscket:
            weboscket.send(data)


    def receive_data(self, uri: str) -> Respones:
        """
        Receives data from uri ( see init )
        via websockets
        """
        with connect(uri) as websocket:
            data=websocket.recv()
        return data

    def sending(self, data: Request, ip: str) -> Response:
        uri: str = f"ws://{ip}:{self.port}"

        self.send_data(data, uri)
        return self.receive_data(uri)


