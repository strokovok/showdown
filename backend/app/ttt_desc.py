import click
import random

from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy

from .database import db
from .models import User, Game, Bot, Match, MatchState


def init_app(app):
    app.cli.add_command(ttt_desc_command)


DESC = """
## Крестики-нолики
### Правила игры

Поле игры представляет из себя сетку 10х10. Два игрока ходят по очереди. Первый игрок выбирается случайно.

Во время хода игрок должен выбрать клетку, в которую будет поставлена его метка (крестик или нолик). Выигрывает тот, у кого на поле первым окажется непрерывный ряд из меток длиной не менее пяти.

В случае, если свободных клеток не осталось, а победитель не обнаружен, игра завершается со статусом "ничья".

### Формат взаимодействия

Вам предлагается написать бота, который будет подключаться к игровому серверу посредством протокола WebSocket.
Как только в игровой очереди оказывается два игровых бота, начинается матч.

Игровой сервер доступен по адресу: **ws://151.248.114.248:5050**

После подключения к серверу, бот должен авторизоваться в игровой системе, отправив сообщение следующего вида:
```json
{
    "type": "AUTH"
    "payload": {
        "id": <ID бота>,
        "token": "<Токен авторизации бота>"
    }
}
```

Игрок, который ходит первым, получит от сервера следующее сообщение:
```json
{
    "type": "YOU_START"
}
```

Для того чтобы совершить ход, необходимо отправить сообщение следующего вида:
```json
{
    "type": "MOVE",
    "payload": [<X координата в интервале [0; 9]>, <Y координата в интервале [0; 9]>]
}
```

Игрок, ожидающий ход своего оппонента, получает информацию о ходе оппонента следующим сообщением:
```json
{
    "type": "OPPONENT_MOVE",
    "payload": [<X координата в интервале [0; 9]>, <Y координата в интервале [0; 9]>]
}
```

Как только игра заканчивается, подключение разрывается. Для повторной игры необходимо установить повторное подключение.

### Написание простейшего бота

Для наглядности, ниже представлен код простейшего бота с использованием Python3 и библиотеки websockets.
Данный бот делает ход в случайную свободную клетку.
```python
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
ADDRESS, PORT = "151.248.114.248", 5050 # Константы с параметрами подключения

# Создание и запуск бота
SimpleTicTacToeBot(ID, TOKEN).connect(ADDRESS, PORT)
```
"""


def ttt_desc():
    game = Game.query.get(1)
    game.detailed_description = DESC
    db.session.commit()


@click.command('ttt-desc')
@with_appcontext
def ttt_desc_command():
    ttt_desc()
    click.echo('Added TTT desc.')
