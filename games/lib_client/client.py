import json

import asyncio
import websockets


class WebSocketClient:
    def __init__(self):
        pass

    async def _connect(self, uri):
        async with websockets.connect(uri) as websocket:
            self.websocket = websocket
            self.on_init()
            try:
                async for message in websocket:
                    data = json.loads(message)
                    t, payload = data["type"], data["payload"]
                    print(f"< [{t}]: {payload}")
                    self.on_message(data["type"], data["payload"])
            except Exception as e:
                print(e)
                pass

    def connect(self, address, port):
        uri = f"ws://{address}:{port}"
        asyncio.get_event_loop().run_until_complete(self._connect(uri))

    def send(self, t, payload):
        print(f"> [{t}]: {payload}")

        message = json.dumps({
            "type": t,
            "payload": payload
        })
        asyncio.create_task(self.websocket.send(message))

    def on_init(self):
        pass

    def on_message(self, t, payload):
        pass
