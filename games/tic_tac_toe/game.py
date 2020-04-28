from enum import Enum


class RowDirection(Enum):
    H = [1, 0]
    V = [0, 1]
    D1 = [1, 1]
    D2 = [1, -1]


class GameState:
    def __init__(self, x_len, y_len, win_len):
        self.x_len, self.y_len, self.win_len = x_len, y_len, win_len
        self.field = [[None for y in range(y_len)] for x in range(x_len)]
        self.shadow = [[None for y in range(y_len)] for x in range(x_len)]
        self.shadow_list = []
        self.free_cnt = x_len * y_len

    def get(self, x, y):
        if self.shadow[x][y] != None:
            return self.shadow[x][y]
        return self.field[x][y]

    # True -> win
    # False -> continue game
    # None -> tie
    def set(self, x, y, val):
        self.field[x][y] = val
        self.free_cnt -= 1
        for d in RowDirection:
            if self.count_row(d, x, y)[0] >= self.win_len:
                return True
        return None if self.free_cnt == 0 else False

    def set_shadow(self, x, y, val):
        self.shadow[x][y] = val
        self.shadow_list.append([x, y])

    def clear_shadow(self):
        for x, y in self.shadow_list:
            self.shadow[x][y] = None
        self.shadow_list = []

    def is_inside(self, x, y):
        return 0 <= x < self.x_len and 0 <= y < self.y_len

    def count_row(self, d, x, y):
        f, fp, fd = self.count_ray(d, x, y, 1)
        b, bp, bd = self.count_ray(d, x, y, -1)
        return f + b - 1, fp + bp, (fd, bd,)

    def count_ray(self, d, x, y, m):
        val = self.get(x, y)
        for i in range(1, self.win_len * 10):
            nx, ny = x + i * d.value[0] * m, y + i * d.value[1] * m
            if not self.is_inside(nx, ny):
                return i, 0, (nx, ny,)
            nval = self.get(nx, ny)
            if nval == None:
                return i, 1, (nx, ny,)
            if nval != val:
                return i, 0, (nx, ny,)
