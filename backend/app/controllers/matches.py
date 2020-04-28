import json

from datetime import datetime

from flask import Blueprint
from flask import request

from app.database import db
from app.models import Bot
from app.models import Match
from app.models import MatchState

from .utils.errors import ErrorMessage
from .utils.getters import get_match
from .utils.helpers import get_json_request
from .utils.helpers import require_game_management
from .utils.helpers import require_match_management


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


@bp.route("/create", methods=["POST"])
def create_match():
    game = require_game_management()

    schema = {
        "type": "object",
        "properties": {
            "participants": {
                "type": "array",
                "items": {"type": "integer"},
                "uniqueItems": True,
                "minItems": 2,
                "maxItems": 2 # Temporary limitation (or maybe not, WHO KNOWS..)
            }
        },
        "required": ["participants"]
    }
    req = get_json_request(schema)
    participants_ids = req["participants"]

    participants = Bot.query.filter(Bot.id.in_(participants_ids)).all()
    for id in (set(participants_ids) - {bot.id for bot in participants}):
        ErrorMessage.NO_SUCH_BOT.abort(params={"id": id})

    for bot in participants:
        if bot.game_id != game.id:
            ErrorMessage.WRONG_BOT_GAME.abort(bot_id=bot.id, game_id=game.id)

    match = Match(state=MatchState.CREATED, game=game, participants=participants)
    db.session.add(match)
    db.session.commit()

    return match.to_json()


@bp.route("/<int:id>/start", methods=["POST"])
def start_match(id):
    match = require_match_management(id)

    if match.state not in [MatchState.CREATED]:
        ErrorMessage.WRONG_MATCH_STATE.abort(state=match.state.value, state_name=match.state.name)

    match.state = MatchState.INPROCESS
    match.start_time = datetime.now()
    db.session.commit()

    return { "success": True }


@bp.route("/<int:id>/finish", methods=["POST"])
def finish_match(id):
    match = require_match_management(id)

    if match.state not in [MatchState.INPROCESS]:
        ErrorMessage.WRONG_MATCH_STATE.abort(state=match.state.value, state_name=match.state.name)

    schema = {
        "type": "object",
        "properties": {
            "data": {"type": "object"},
            "results": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "score": {
                            "type": "number"
                        }
                    },
                    "required": ["id", "score"]
                },
                "minItems": 2,
                "maxItems": 2 # Temporary limitation (or maybe not, WHO KNOWS..)
            }
        },
        "required": ["data", "results"]
    }
    req = get_json_request(schema)
    data = req["data"]
    results = {res["id"]: res["score"] for res in req["results"]}

    results_ids = set(results.keys())
    participants_ids = {bot.id for bot in match.participants}
    for bot_id in (results_ids - participants_ids):
        ErrorMessage.WRONG_BOT_MATCH.abort(bot_id=bot_id, match_id=id)
    for bot_id in (participants_ids - results_ids):
        ErrorMessage.MISSING_RESULT.abort(match_id=id, bot_id=bot_id)

    # TEMPORARY RANKING
    for bot in match.participants:
        bot.rank = bot.rank + results[bot.id]

    match.results = json.dumps({
        "game_results": results,
        "rerank": results
    })
    # TEMPORARY RANKING

    match.data = json.dumps(data)

    match.state = MatchState.FINISHED
    match.end_time = datetime.now()

    db.session.commit()

    return { "success": True }


@bp.route("/<int:id>/cancel", methods=["POST"])
def cancel_match(id):
    match = require_match_management(id)

    if match.state not in [MatchState.CREATED, MatchState.INPROCESS]:
        ErrorMessage.WRONG_MATCH_STATE.abort(state=match.state.value, state_name=match.state.name)

    match.state = MatchState.CANCELLED
    match.end_time = datetime.now()
    db.session.commit()

    return { "success": True }
