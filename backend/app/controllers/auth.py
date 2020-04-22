from flask import Blueprint
from flask import session

from app.database import db
from app.models import User

from .utils.errors import ErrorMessage
from .utils.getters import get_user
from .utils.helpers import cur_user
from .utils.helpers import get_json_request


bp = Blueprint("auth", __name__, url_prefix="/api/auth")


auth_schema = {
    "type": "object",
    "properties": {
        "login": {"type": "string", "minLength": 1, "maxLength": 30},
        "password": {"type": "string", "minLength": 1, "maxLength": 100},
    },
    "required": ["login", "password"]
}


@bp.route("/register", methods=["POST"])
def register():
    req = get_json_request(auth_schema)
    login, password = req["login"], req["password"]

    user = get_user(login=login, fail=False)
    if user is not None:
        ErrorMessage.USER_LOGIN_ALREADY_EXISTS.abort(login=login)

    user = User(login=login, password=password)
    db.session.add(user)
    db.session.commit()

    session.clear()
    session["user_id"] = user.id

    return user.to_json()


@bp.route("/login", methods=["POST"])
def login():
    req = get_json_request(auth_schema)
    login, password = req["login"], req["password"]

    user = get_user(login=login)
    if not user.check_password(password):
        ErrorMessage.INCORRECT_PASSWORD.abort()

    session.clear()
    session["user_id"] = user.id

    return user.to_json()


@bp.route("/info", methods=["GET"])
def info():
    if cur_user() is None:
        return {"logged_in": False}
    return {
        "logged_in": True,
        "user": cur_user().to_json()
    }


@bp.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return {"message": "Logged out successfully"}
