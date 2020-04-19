from flask import Blueprint
from flask import session

from app.database import db
from app.models import User

from .errors import ErrorMessage


bp = Blueprint("users", __name__, url_prefix="/users")


@bp.route("/", methods=["GET"])
def get_users_list():
    return {
        "users": [ user.to_json() for user in User.query.all() ]
    }


@bp.route("/<int:id>", methods=["GET"])
def get_user(id):
    user = User.query.get(id)
    if user is None:
        ErrorMessage.NO_SUCH_USER_ID.abort(id=id)
    return user.to_json(bots=True)
