import random

from lib.match import Match


class TurnBasedMatch(Match):
    def __init__(self, players):
        super().__init__(players)
        self.moving_player, self.waiting_player = random.sample(players, k=2)
        self.moving_player.send("YOU_START", None)

    # OVERRIDE
    def _on_player_message(self, player, t, payload):
        if player != self.moving_player:
            player.send("DEBUG", "Not your turn")
            return

        if t != "MOVE":
            player.send("DEBUG", "Unknown message type")
            return

        try:
            res = self._make_move(player, payload)
        except:
            player.send("DEBUG", "Invalid move")
            return

        self.logs.append({
            "bot_id": player.id,
            "move": payload
        })
        if res == True:
            self._finish({
                self.moving_player: 1,
                self.waiting_player: 0
            })
        elif res == None:
            self._finish({
                self.moving_player: 0.5,
                self.waiting_player: 0.5
            })
        else:
            self.waiting_player.send("OPPONENT_MOVE", payload)
            self.moving_player, self.waiting_player = self.waiting_player, self.moving_player

    def _make_move(self, player, move):
        pass
