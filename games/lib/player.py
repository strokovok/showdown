import json

from lib.server import WebSocketClient


class Player(WebSocketClient):
    def __init__(self, game):
        self.game = game
        self.id = None

    # OVERRIDE
    def on_init(self):
        self.game.on_player_init(self)

    # OVERRIDE
    def on_message(self, message):
        try:
            data = json.loads(message)
            t, payload = data["type"], data["payload"]
        except:
            self.send("DEBUG", "Invalid JSON message")
        self.game.on_player_message(self, data["type"], data["payload"])

    # OVERRIDE
    def on_close(self):
        self.game.on_player_close(self)

    def send(self, t, payload):
        data = {
            "type": t,
            "payload": payload
        }
        super().send(json.dumps(data))

    def set_id(self, id):
        self.id = id
