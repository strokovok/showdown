from lib_client.client import WebSocketClient


class Bot(WebSocketClient):
    def __init__(self):
        pass

    def set_auth(self, id, token):
        self.id, self.token = id, token

    def on_init(self):
        payload = { "id": self.id, "token": self.token }
        self.send("AUTH", payload)
