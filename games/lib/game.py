from lib.player import Player
from lib.server import WebSocketServer

import lib.master_api as master_api


class Game(WebSocketServer):
    def __init__(self, game_id, master_addr, token, match_factory):
        self.game_id = game_id
        self.master_addr = master_addr
        self.token = token
        self.match_factory = match_factory

        self.queue = set()
        self.match_of_player = dict()

    # OVERRIDE
    def _create_client(self):
        return Player(self)

    def on_player_init(self, player):
        pass

    def on_player_message(self, player, t, payload):
        if player in self.queue:
            player.send("DEBUG", "You are in game queue")
            return

        if player in self.match_of_player:
            self.match_of_player[player].on_player_message(player, t, payload)
            return

        if t != "AUTH":
            player.send("DEBUG", "You are not authorized")
            return

        id = self._auth_player(payload)
        if id == None:
            player.send("DEBUG", "Authorization failed")
            return

        player.set_id(id)
        self.queue.add(player)

        if len(self.queue) < 2:
            return

        players = list(self.queue)
        self.queue.clear()
        match = self.match_factory(players)
        for p in players:
            self.match_of_player[p] = match
        match.init_on_master(self.master_addr, self.game_id, self.token)

    def on_player_close(self, player):
        if player in self.queue:
            self.queue.remove(player)
            return

        if player in self.match_of_player:
            self.match_of_player.pop(player).on_player_close(player)

    def _auth_player(self, data):
        try:
            assert isinstance(data.get("id", None), int)
            assert isinstance(data.get("token", None), str)
        except:
            return None
        if master_api.auth_bot(self.master_addr, self.game_id, self.token, data["id"], data["token"]):
            return data["id"]
        return None
