from flask import Blueprint

from app.models import User

from .utils.getters import get_user


bp = Blueprint("users", __name__, url_prefix="/api/users")


@bp.route("/", methods=["GET"])
def get_users_list():
    return {
        "users": [ user.to_json() for user in User.query.all() ]
    }


@bp.route("/<int:id>", methods=["GET"])
def get_user_route(id):
    return get_user(id=id).to_json()
