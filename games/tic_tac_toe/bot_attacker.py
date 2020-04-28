import random
import json

from game import RowDirection


INF = int(1e15)


class BotAttacker:
    def __init__(self, gs, c, weights):
        self.gs, self.c, self.weights = gs, c, weights
        self.op = 'o' if c == 'x' else 'x'
        self.log_file = None

    def make_move(self, log=None):
        if log:
            self.log_file = open(f'logs/{log}({self.c})', 'w')

        best_result = None
        best_points = []
        for x in range(self.gs.x_len):
            for y in range(self.gs.y_len):
                if self.gs.get(x, y) != None:
                    continue
                res = self.get_point_profit(x, y)

                if self.log_file:
                    self.log_file.write(f"[{x}, {y}] = {res}\n")

                if best_result != None and best_result > res:
                    continue
                if best_result == None or best_result < res:
                    best_result = res
                    best_points = []
                best_points.append([x, y])

        if self.log_file:
            self.log_file.close()

        return random.choice(best_points)

    def get_point_profit(self, x, y):
        mn = INF * 10

        if self.log_file:
            worst = ""
            worst_before = ""
            worst_after = ""

        for ex in range(self.gs.x_len):
            for ey in range(self.gs.y_len):
                if self.gs.get(ex, ey) != None or (ex == x and ey == y):
                    continue
                if random.randint(1, 100) < 50:
                    continue

                if self.log_file:
                    _before = self.kek(x, y)
                    _before.update(self.kek(ex, ey))

                before = self.eval_point(x, y) + self.eval_point(ex, ey)
                self.gs.set_shadow(x, y, self.c)
                half_after = self.eval_point(x, y)
                if half_after - before > INF // 2:
                    self.gs.clear_shadow()
                    return INF * 10
                self.gs.set_shadow(ex, ey, self.op)
                after = self.eval_point(x, y) + self.eval_point(ex, ey)

                if self.log_file:
                    _after = self.kek(x, y)
                    _after.update(self.kek(ex, ey))

                if after - before < mn:
                    mn = after - before
                    if self.log_file:
                        worst = f"enemy[{ex}, {ey}]"
                        worst_before = json.dumps(_before, indent=4)
                        worst_after = json.dumps(_after, indent=4)
                self.gs.clear_shadow()
        if self.log_file:
            self.log_file.write(f"\n\n\n\n\nworst: {worst}\n")
            self.log_file.write(f"\nworst_before: {worst_before}\n")
            self.log_file.write(f"\nworst_after: {worst_after}\n")
        return mn
#         before = self.eval_point(x, y)
#
#         self.gs.set_shadow(x, y, self.c)
#         after = self.eval_point(x, y)
#         self.gs.clear_shadow()
#
#         return after - before

    def kek(self, x, y):
        impact = dict()
        for d in RowDirection:
            impact.update(self.get_impact(x + d.value[0], y + d.value[1], d))
            impact.update(self.get_impact(x - d.value[0], y - d.value[1], d))
        return {str(_k): _v for _k, _v in impact.items()}

    def eval_point(self, x, y):
        impact = dict()
        for d in RowDirection:
            impact.update(self.get_impact(x + d.value[0], y + d.value[1], d))
            impact.update(self.get_impact(x - d.value[0], y - d.value[1], d))
        val = 0
        for k, v in impact.items():
            val += v
#         impact = {str(_k): _v for _k, _v in impact.items()}
#         self.log_file.write(json.dumps(impact, indent=4) + "\n")
        return val

    def get_impact(self, x, y, d):
        if not self.gs.is_inside(x, y) or self.gs.get(x, y) == None:
            return dict()

        val, p, ind = self.gs.count_row(d, x, y)
        if val >= self.gs.win_len:
            w = INF
        else:
            w = self.weights[val][p]
        if self.gs.get(x, y) != self.c:
            w *= -1
        return { ind: w }
