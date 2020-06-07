import json
import random
import sys
sys.path.append('../..')

from lib_client.bot import Bot

from tic_tac_toe.game_state import GameState


X_LEN, Y_LEN = 10, 10
WIN_LEN = 5


class BotRandomer(Bot):
    def __init__(self):
        self.gs = GameState(X_LEN, Y_LEN, WIN_LEN)

    def on_message(self, t, payload):
        if t == "YOU_START":
            self.make_move()

        if t == "OPPONENT_MOVE":
            x, y = payload
            self.gs.set(x, y, 'O')
            self.make_move()

    def make_move(self):
        options = []
        for x in range(self.gs.x_len):
            for y in range(self.gs.y_len):
                if self.gs.get(x, y) == None:
                    options.append([x, y])
        move = random.choice(options)

        self.gs.set(move[0], move[1], 'X')
        self.send("MOVE", move)
