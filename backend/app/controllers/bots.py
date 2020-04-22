from flask import Blueprint

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


bp = Blueprint("bots", __name__, url_prefix="/api/bots")


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

    bot = Bot(name=name, rank=0, owner=cur_user(), game=game, access_token=generate_token())
    db.session.add(bot)
    db.session.commit()

    return bot.to_json(owner=True, game=True)


@bp.route("/<int:id>", methods=["GET"])
def get_bot_route(id):
    return get_bot(id=id).to_json(owner=True, game=True)


@bp.route("/<int:id>/matches", methods=["GET"])
def get_bot_matches(id):
    return get_bot(id=id).to_json(owner=True, game=True, matches={"participants":{"owner":True}})


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
        **(bot.to_json(owner=True, game=True)),
        "access_token": token
    }

    return res


@bp.route("/<int:id>/authorize", methods=["POST"])
def authorize_bot(id):
    require_game_management()

    schema = {
        "type": "object",
        "properties": {
            "access_token": {"type": "string"},
        },
        "required": ["access_token"]
    }
    req = get_json_request(schema)
    token, game_id = req["access_token"], req["game"]["id"]

    bot = get_bot(id=id)
    if bot.game_id != game_id:
        ErrorMessage.WRONG_BOT_GAME.abort(bot_id=bot.id, game_id=game_id)

    return {
        "success": bot.check_access_token(token),
        "bot": bot.to_json(owner=True)
    }
