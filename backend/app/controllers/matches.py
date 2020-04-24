import json

from flask import Blueprint
from flask import request

from app.database import db
from app.models import Match
from app.models import MatchState

from .utils.errors import ErrorMessage
from .utils.getters import get_match
from .utils.helpers import get_json_request
from .utils.helpers import require_game_management
from .utils.helpers import require_login


bp = Blueprint("Matches", __name__, url_prefix="/api/matches")


@bp.route("/<int:id>", methods=["GET"])
def get_match_route(id):
    return get_match(id=id).to_json(data=True, game=True, participants={"owner":True})


@bp.route("/", methods=["GET"])
def get_matches():
    query = Match.query

    game_id = request.args.get("game_id", None, int)
    if game_id is not None:
        query = query.filter_by(game_id=game_id)

    bot_id = request.args.get("bot_id", None, int)
    if bot_id is not None:
        query = query.filter(Match.participants.any(id=bot_id))

    user_id = request.args.get("user_id", None, int)
    if user_id is not None:
        query = query.filter(Match.participants.any(owner_id=user_id))

    return {
        "matches": [match.to_json(game=True, participants={"owner": True}) for match in query.all()]
    }
