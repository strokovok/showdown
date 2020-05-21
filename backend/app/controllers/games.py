from flask import Blueprint

from app.models import Game

from .utils.getters import get_game


bp = Blueprint("games", __name__, url_prefix="/api/games")


@bp.route("/", methods=["GET"])
def get_games_list():
    return {
        "games": [ game.to_json() for game in Game.query.all() ]
    }


@bp.route("/<int:id>", methods=["GET"])
def get_game_route(id):
    return get_game(id=id).to_json(description=True, detailed_description=True)
