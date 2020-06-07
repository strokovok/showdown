from lib.turn_based_match import TurnBasedMatch

from tic_tac_toe.game_state import GameState


class TicTacToeMatch(TurnBasedMatch):
    def __init__(self, x_len, y_len, win_len, players):
        super().__init__(players)
        self.gs = GameState(x_len, y_len, win_len)

    def _assert_is_valid_and_get_x_y(self, move):
        assert isinstance(move, list) and len(move) == 2
        x, y = move
        assert self.gs.is_inside(x, y)
        assert self.gs.get(x, y) == None
        return x, y

    # OVERRIDE
    def _make_move(self, player, move):
        x, y = self._assert_is_valid_and_get_x_y(move)
        return self.gs.set(x, y, player.id)
