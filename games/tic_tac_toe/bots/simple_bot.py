import json # Необходимо для запаковки/распаковки WebSocket сообщений
import asyncio # Необходимо для запуска асинхронного WebSocket клиента
import websockets # Необходимо для WebSocket подключения
import random # Для совершения случайного хода


X_LEN, Y_LEN = 10, 10 # Константы - размеры игрового поля

# Класс, реализующий бота
class SimpleTicTacToeBot:
    def __init__(self, id, token):
        self.id = id
        self.token = token

        # Сохраняем все свободные клетки
        self.free_cells = set()
        for x in range(X_LEN):
            for y in range(Y_LEN):
                self.free_cells.add(tuple([x, y]))

    # Асинхронный метод для обработки цикла подключения
    async def _connect(self, uri):
        # Подключение к WebSocket
        async with websockets.connect(uri) as websocket:

            # Отправка сообщения авторизации
            await websocket.send(json.dumps({
                "type": "AUTH",
                "payload": { "id": self.id, "token": self.token }
            }))

            # Получаем входящие сообщения
            async for message in websocket:
                data = json.loads(message)

                # Если оппонент сделал ход, исключаем клетку из свободных
                if data["type"] == "OPPONENT_MOVE":
                    x, y = data["payload"]
                    self.free_cells.remove(tuple(data["payload"]))

                # Выбираем случайную свободную клетку
                move = random.choice(list(self.free_cells))
                self.free_cells.remove(move)
                # Делаем игровой ход
                await websocket.send(json.dumps({
                    "type": "MOVE",
                    "payload": list(move)
                }))

    # Метод запуска подключения
    def connect(self, address, port):
        uri = f"ws://{address}:{port}"
        asyncio.get_event_loop().run_until_complete(self._connect(uri))


ID, TOKEN = 1, "password" # Константы cо значениями для авторизации
ADDRESS, PORT = "localhost", 5050 # Константы с параметрами подключения

# Создание и запуск бота
SimpleTicTacToeBot(ID, TOKEN).connect(ADDRESS, PORT)
