import sys
sys.path.append('../..')

from lib.game import Game

from match import TicTacToeMatch


GAME_ID = 1
MASTER_ADDRESS = "localhost:5000"
TOKEN = "password"
PORT = 5050

X_LEN, Y_LEN = 10, 10
WIN_LEN = 5


match_factory = lambda players: TicTacToeMatch(X_LEN, Y_LEN, WIN_LEN, players)

Game(GAME_ID, MASTER_ADDRESS, TOKEN, match_factory).serve(PORT)
