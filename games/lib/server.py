import asyncio
import websockets


class WebSocketClient:
    def __init__(self):
        pass

    def set_websocket(self, websocket):
        self.websocket = websocket
        self.on_init()

    def on_init(self):
        pass

    def on_message(self, message):
        pass

    def on_close(self):
        pass

    def send(self, message):
        asyncio.create_task(self.websocket.send(message))

    def close(self):
        asyncio.create_task(self.websocket.close())


class WebSocketServer:
    def __init__(self):
        pass

    def _create_client(self):
        return WebSocketClient()

    async def _serve_client(self, websocket, path):
        client = self._create_client()
        client.set_websocket(websocket)

        try:
            async for message in websocket:
                client.on_message(message)
        except Exception as e:
            print(e)
            pass

        client.on_close()

    def serve(self, port):
        start_server = websockets.serve(self._serve_client, "localhost", port)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()
