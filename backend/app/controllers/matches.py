import json

from flask import Blueprint
from flask import session

from app.database import db
from app.models import Match
from app.models import MatchState

from .utils.errors import ErrorMessage
from .utils.getters import get_bot
from .utils.getters import get_game
from .utils.getters import get_match
from .utils.helpers import cur_user
from .utils.helpers import generate_token
from .utils.helpers import get_field
from .utils.helpers import get_json_field
from .utils.helpers import get_json_request
from .utils.helpers import get_str_field
from .utils.helpers import require_game_management
from .utils.helpers import require_login


bp = Blueprint("Matches", __name__, url_prefix="/api/matches")


@bp.route("/<int:id>", methods=["GET"])
def get_match_route(id):
    return get_match(id=id).to_json(data=True, game=True, participants={"owner":True})


@bp.route("/create", methods=["POST"])
def create_match():
    require_game_management()

    req = get_json_request()
    game_id = req["game"]["id"]

    game = get_game(id=game_id)

    match = Match(game=game, state=MatchState.CREATED)
    db.session.add(match)
    db.session.commit()

    return match.to_json()


def _get_match_and_check_management(match_id):
    require_game_management()

    match = get_match(id=match_id)
    if match.game_id != get_json_request()["game"]["id"]:
        ErrorMessage.WRONG_MATCH_GAME.abort(match_id=match_id, game_id=game_id)

    return match


@bp.route("/<int:id>/start", methods=["POST"])
def start_match(id):
    match = _get_match_and_check_management(id)

    match.state = MatchState.INPROCESS
    db.session.commit()

    return { "success": True }


@bp.route("/<int:id>/finish", methods=["POST"])
def finish_match(id):
    match = _get_match_and_check_management(id)

    schema = {
        "type": "object",
        "properties": {
            "results": {
                "type": "object"
            },
            "data": {
                "type": "object"
            }
        },
        "required": ["results", "data"]
    }
    req = get_json_request()
    results, data

    match.state = MatchState.FINISHED


    db.session.commit()

    return { "success": True }
