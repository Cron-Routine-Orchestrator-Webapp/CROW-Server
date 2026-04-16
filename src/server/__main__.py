from websocket_communication.websocket_util import server



if __name__ == "__main__":


    server_instance = server()

    server_instance.send_data("Hello, WebSocket!")