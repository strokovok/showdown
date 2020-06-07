import json
import random
import sys
sys.path.append('../..')

from lib_client.bot import Bot

from tic_tac_toe.game_state import GameState, RowDirection


X_LEN, Y_LEN = 10, 10
WIN_LEN = 5

WEIGHTS = [[0, 0, 0] for i in range(WIN_LEN)]
WEIGHTS[1] = [0, 1, 5]
WEIGHTS[2] = [0, 20, 50]
WEIGHTS[3] = [0, 100, 10000]
WEIGHTS[4] = [0, 100000, 1000000]

INF = int(1e15)


class BotAttacker(Bot):
    def __init__(self):
        self.gs = GameState(X_LEN, Y_LEN, WIN_LEN)

    def on_message(self, t, payload):
        if t == "YOU_START":
            self.make_move()

        if t == "OPPONENT_MOVE":
            x, y = payload
            self.gs.set(x, y, 'o')
            self.make_move()

    def make_move(self):
        best_result = None
        best_points = []
        for x in range(self.gs.x_len):
            for y in range(self.gs.y_len):
                if self.gs.get(x, y) != None:
                    continue
                res = self.get_point_profit(x, y)
                if best_result != None and best_result > res:
                    continue
                if best_result == None or best_result < res:
                    best_result = res
                    best_points = []
                best_points.append([x, y])
        move = random.choice(best_points)
        self.gs.set(move[0], move[1], 'x')
        self.send("MOVE", move)

    def get_point_profit(self, x, y):
        mn = INF * 10
        for ex in range(self.gs.x_len):
            for ey in range(self.gs.y_len):
                if self.gs.get(ex, ey) != None or (ex == x and ey == y):
                    continue
                if random.randint(1, 100) < 50:
                    continue

                before = self.eval_point(x, y) + self.eval_point(ex, ey)
                self.gs.set_shadow(x, y, 'x')
                half_after = self.eval_point(x, y)
                if half_after - before > INF // 2:
                    self.gs.clear_shadow()
                    return INF * 10
                self.gs.set_shadow(ex, ey, 'o')
                after = self.eval_point(x, y) + self.eval_point(ex, ey)

                if after - before < mn:
                    mn = after - before
                self.gs.clear_shadow()
        return mn

    def eval_point(self, x, y):
        impact = dict()
        for d in RowDirection:
            impact.update(self.get_impact(x + d.value[0], y + d.value[1], d))
            impact.update(self.get_impact(x - d.value[0], y - d.value[1], d))
        val = 0
        for k, v in impact.items():
            val += v
        return val

    def get_impact(self, x, y, d):
        if not self.gs.is_inside(x, y) or self.gs.get(x, y) == None:
            return dict()

        val, p, ind = self.gs.count_row(d, x, y)
        if val >= self.gs.win_len:
            w = INF
        else:
            w = WEIGHTS[val][p]
        if self.gs.get(x, y) != 'x':
            w *= -1
        return { ind: w }
