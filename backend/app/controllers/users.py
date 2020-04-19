from flask import Blueprint
from flask import g
from flask import session

from app.database import db
from app.models import User

from .helpers import abort_with_message


bp = Blueprint("users", __name__, url_prefix="/users")


@bp.route("/", methods=["GET"])
def get_users_list():
    return {
        "users": [ user.to_json() for user in User.query.all() ]
    }


def _get_user(id):
    user = User.query.get(id)
    if user is None:
        abort_with_message(f"No such user with id {id}", 400)
    return user


@bp.route("/<int:id>", methods=["GET"])
def get_user(id):
    return _get_user(id).to_json()


@bp.route("/<int:id>/bots", methods=["GET"])
def get_user_bots(id):
    return {
        "bots": [
            bot.to_json() for bot in _get_user(id).bots
        ]
    }
