import random


class BotRandomer:
    def __init__(self, gs, c):
        self.gs, self.c = gs, c

    def make_move(self):
        options = []
        for x in range(self.gs.x_len):
            for y in range(self.gs.y_len):
                if self.gs.get(x, y) == None:
                    options.append([x, y])
        return random.choice(options)
