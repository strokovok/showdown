import json
import os
import shutil
import time

from bot_randomer import BotRandomer
from bot_attacker import BotAttacker
from game import GameState


X_LEN, Y_LEN = 10, 10
WIN_LEN = 5


weights = [[0, 0, 0] for i in range(WIN_LEN)]

weights[1] = [0, 1, 5]
weights[2] = [0, 20, 50]
weights[3] = [0, 100, 10000]
weights[4] = [0, 100000, 1000000]


def run(ids):

#     shutil.rmtree("logs")
#     os.mkdir("logs")
    gs = GameState(X_LEN, Y_LEN, WIN_LEN)

    bots = [
        BotAttacker(gs, 'x', weights),
        BotAttacker(gs, 'o', weights)
    ]
    game_log = []

    cur = 0
    cnt = 1
    while True:
        move = bots[cur].make_move(log=None)
        game_log.append({
            "bot_id": ids[cur],
            "move": move
        })
        res = gs.set(move[0], move[1], bots[cur].c)

        print("\n" * 3)
        print(f"Move {cnt}:")
        for y in range(Y_LEN):
            s = ""
            for x in range(X_LEN):
                val = gs.get(x, y)
                if val == None:
                    val = "_"
                s += val
            print(s)

        if res == True:
            print(bots[cur].c + " wins!")
            return {
                "data": {
                    "game_log": game_log,
                },
                "results": [
                    {
                        "id": ids[cur],
                        "score": 1,
                    },
                    {
                        "id": ids[1 - cur],
                        "score": 0,
                    }
                ]
            }
        if res == None:
            print("Tie!")
            return {
                "data": {
                    "game_log": game_log,
                },
                "results": [
                    {
                        "id": ids[cur],
                        "score": 0.5,
                    },
                    {
                        "id": ids[1 - cur],
                        "score": 0.5,
                    }
                ]
            }
        cur = 1 - cur
        cnt += 1
#         time.sleep(0.2)

