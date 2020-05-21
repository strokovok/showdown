from flask import Blueprint
from flask import request

from app.database import db
from app.models import Bot

from .utils.errors import ErrorMessage
from .utils.getters import get_bot
from .utils.getters import get_game
from .utils.helpers import cur_user
from .utils.helpers import generate_token
from .utils.helpers import get_json_request
from .utils.helpers import require_game_management
from .utils.helpers import require_login
from .utils.rank_system import DEFAULT_RANK


bp = Blueprint("bots", __name__, url_prefix="/api/bots")


@bp.route("/", methods=["GET"])
def get_bots():
    query = Bot.query

    owner_id = request.args.get('owner_id', None, int)
    if owner_id is not None:
        query = query.filter_by(owner_id=owner_id)

    game_id = request.args.get('game_id', None, int)
    if game_id is not None:
        query = query.filter_by(game_id=game_id)

    match_id = request.args.get('match_id', None, int)
    if match_id is not None:
        query = query.filter(Bot.matches.any(id=match_id))

    query = query.order_by(Bot.rank.desc())

    return {
        "bots": [bot.to_json(owner=True, game=True) for bot in query.all()]
    }


@bp.route("/<int:id>", methods=["GET"])
def get_bot_route(id):
    return get_bot(id=id).to_json(owner=True, game=True, description=True, detailed_description=True)


@bp.route("/create", methods=["POST"])
def create_bot():
    require_login()

    schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string", "minLength": 1, "maxLength": 30},
            "game_id": {"type": "integer"},
        },
        "required": ["name", "game_id"]
    }
    req = get_json_request(schema)
    name, game_id = req["name"], req["game_id"]

    bot = get_bot(name=name, fail=False)
    if bot is not None:
        ErrorMessage.BOT_NAME_ALREADY_EXISTS.abort(name=name)

    game = get_game(id=game_id)

    token = generate_token()
    bot = Bot(name=name, rank=DEFAULT_RANK, owner=cur_user(), game=game, access_token=token)
    db.session.add(bot)
    db.session.commit()

    return {
        "bot": bot.to_json(owner=True, game=True),
        "access_token": token
    }


@bp.route("/<int:id>/renew_token", methods=["GET"])
def renew_bot_token(id):
    require_login()
    bot = get_bot(id=id)

    if bot.owner_id != cur_user().id:
        ErrorMessage.NOT_YOUR_BOT.abort(id=id)

    token = generate_token()
    bot.access_token = token
    db.session.commit()

    return {
        "bot": bot.to_json(owner=True, game=True),
        "access_token": token
    }


@bp.route("/<int:id>/authorize", methods=["POST"])
def authorize_bot(id):
    game = require_game_management()

    schema = {
        "type": "object",
        "properties": {
            "access_token": {"type": "string"},
        },
        "required": ["access_token"]
    }
    req = get_json_request(schema)
    token = req["access_token"]

    bot = get_bot(id=id)
    if bot.game_id != game_id:
        ErrorMessage.WRONG_BOT_GAME.abort(bot_id=bot.id, game_id=game.id)

    return {
        "success": bot.check_access_token(token),
        "bot": bot.to_json(owner=True)
    }


@bp.route("/<int:id>/update", methods=["POST"])
def update_bot(id):
    require_login()
    bot = get_bot(id=id)

    if bot.owner_id != cur_user().id:
        ErrorMessage.NOT_YOUR_BOT.abort(id=id)

    schema = {
        "type": "object",
        "properties": {
            "description": {"type": "string", "maxLength": 50},
            "detailed_description": {"type": "string"},
        }
    }
    req = get_json_request(schema)

    bot.description = req.get('description', bot.description)
    bot.detailed_description = req.get('detailed_description', bot.detailed_description)
    db.session.commit()

    return bot.to_json(owner=True, game=True, description=True, detailed_description=True)
