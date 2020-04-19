from flask import Blueprint
from flask import session

from app.database import db
from app.models import Game

from .errors import ErrorMessage


bp = Blueprint("games", __name__, url_prefix="/games")


@bp.route("/", methods=["GET"])
def get_games_list():
    return {
        "games": [ game.to_json() for game in Game.query.all() ]
    }


@bp.route("/<int:id>", methods=["GET"])
def get_game(id):
    game = Game.query.get(id)
    if game is None:
        ErrorMessage.NO_SUCH_GAME_ID.abort(id=id)
    return game.to_json()


@bp.route("/<int:id>/bots", methods=["GET"])
def get_game_bots(id):
    game = Game.query.get(id)
    if game is None:
        ErrorMessage.NO_SUCH_GAME_ID.abort(id=id)
    return game.to_json(bots=True)


@bp.route("/<int:id>/matches", methods=["GET"])
def get_game_matches(id):
    game = Game.query.get(id)
    if game is None:
        ErrorMessage.NO_SUCH_GAME_ID.abort(id=id)
    return game.to_json(matches=True)
