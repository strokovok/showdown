from flask import Blueprint
from flask import g
from flask import session

from app.database import db
from app.models import User

from .helpers import abort_with_message
from .helpers import cur_user
from .helpers import get_json_request
from .helpers import get_str_field


bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=["POST"])
def register():
    data = get_json_request()
    login = get_str_field(data, 'login', 1, 30)
    password = get_str_field(data, 'password', 1, 100)
    user = User.query.filter_by(login=login).first()
    if user is not None:
        abort_with_message(f"User with login {login} already exists", 400)
    user = User(login=login, password=password)
    db.session.add(user)
    db.session.commit()
    session.clear()
    session["user_id"] = user.id
    return user.to_json()


@bp.route("/login", methods=["POST"])
def login():
    data = get_json_request()
    login = get_str_field(data, 'login', 1, 30)
    password = get_str_field(data, 'password', 1, 100)
    user = User.query.filter_by(login=login).first()
    if user is None:
        abort_with_message(f"No such user with login '{login}'", 400)
    if not user.check_password(password):
        abort_with_message(f"Incorrect password", 400)
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
