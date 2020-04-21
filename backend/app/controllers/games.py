from flask import Blueprint
from flask import session

from .getters import get_game


bp = Blueprint("games", __name__, url_prefix="/games")


@bp.route("/", methods=["GET"])
def get_games_list():
    return {
        "games": [ game.to_json() for game in Game.query.all() ]
    }


@bp.route("/<int:id>", methods=["GET"])
def get_game(id):
    return get_game(id=id).to_json()


@bp.route("/<int:id>/bots", methods=["GET"])
def get_game_bots(id):
    return get_game(id=id).to_json(bots={"owner":True})


@bp.route("/<int:id>/matches", methods=["GET"])
def get_game_matches(id):
    return get_game(id=id).to_json(matches={"participants":{"owner": True}})
