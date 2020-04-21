from flask import Blueprint
from flask import session

from app.database import db
from app.models import Bot

from .utils.errors import ErrorMessage
from .utils.getters import get_bot
from .utils.getters import get_game
from .utils.helpers import cur_user
from .utils.helpers import generate_token
from .utils.helpers import get_field
from .utils.helpers import get_json_request
from .utils.helpers import get_str_field
from .utils.helpers import require_game_management
from .utils.helpers import require_login


bp = Blueprint("bots", __name__, url_prefix="/bots")


@bp.route("/create", methods=["POST"])
def create_bot():
    require_login()
    data = get_json_request()

    name = get_str_field(data, "name", 1, 30)
    bot = get_bot(name=name, fail=False)
    if bot is not None:
        ErrorMessage.BOT_NAME_ALREADY_EXISTS.abort(name=name)

    game_id = get_field(data, "game_id", [int])
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
    bot = get_bot(id=id)
    require_game_management(bot.game)
    token = get_str_field(get_json_request(), 'access_token', 1, 1000)
    return {
        "success": bot.check_access_token(token),
        "bot": bot.to_json(owner=True)
    }
