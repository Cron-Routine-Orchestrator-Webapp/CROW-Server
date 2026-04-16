from websockets.sync.client import connect

class server:
    def __init__(self):
        """
        **change uri for final version!**
        """
        self.uri = "ws://localhost:5000"
        pass

def send_data(self, data: any) -> None:
    """
    Sends data on uri ( see init )\n
    via websockets
    """
    with connect(self.uri) as weboscket:
        weboscket.send(data)


def receive_data(self) -> any:
    """
    Receives data from uri ( see init )
    via websockets
    """
    with connect(self.uri) as websocket:
        data=websocket.recv()
    return data


