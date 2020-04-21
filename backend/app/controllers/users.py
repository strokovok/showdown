from flask import Blueprint
from flask import session

from .errors import ErrorMessage
from .getters import get_user


bp = Blueprint("users", __name__, url_prefix="/users")


@bp.route("/", methods=["GET"])
def get_users_list():
    return {
        "users": [ user.to_json() for user in User.query.all() ]
    }


@bp.route("/<int:id>", methods=["GET"])
def get_user(id):
    return get_user(id=id).to_json(bots={"game":True})
