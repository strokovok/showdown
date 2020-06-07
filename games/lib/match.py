import json

import lib.master_api as master_api


class Match:
    def __init__(self, players):
        self.players = players
        self.logs = []
        self.finished = False

    def on_player_close(self, player):
        if self.finished:
            return

        scores = { player : 0 }
        for p in self.players:
            if p != player:
                scores[p] = 1 / (len(self.players) - 1)

        self._finish(scores)

    def _halt(self):
        self.finished = True
        for p in self.players:
            p.close()

    def _finish(self, scores):
        self._halt()

        req = {
            "data": {
                "game_log": self.logs
            },
            "results": [
                {
                    "id": player.id,
                    "score": score
                } for player, score in scores.items()
            ]
        }

        self._finish_on_master(req)

    def init_on_master(self, master_addr, game_id, token):
        self.master_addr = master_addr
        self.game_id = game_id
        self.token = token

        ids = [p.id for p in self.players]
        self.match_id = master_api.create_match(master_addr, game_id, token, ids)
        if self.match_id == None:
            self._halt()
            return

        res = master_api.start_match(master_addr, game_id, token, self.match_id)
        if res == None:
            self._halt()
            return

    def _finish_on_master(self, req):
        master_api.finish_match(self.master_addr, self.game_id, self.token, self.match_id, req)

    def on_player_message(self, player, t, payload):
        if self.finished:
            return
        self._on_player_message(player, t, payload)

    def _on_player_message(self, player, t, payload):
        pass
