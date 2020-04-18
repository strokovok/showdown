from flask import abort
from flask import g
from flask import make_response
from flask import request
from flask import session

from app.models import User


def abort_with_message(msg, status):
    abort(make_response({"error_message": msg}, status))


def get_json_request():
    data = request.get_json(force=True)
    if data is None:
        abort_with_message("Invalid JSON data", 400)
    return data


def get_field(data, field, types):
    if field not in data:
        abort_with_message(f"Missing field '{field}'", 400)
    val = data[field]
    if type(val) not in types:
        msg = f"Invalid type of field '{field}'. "
        msg += f"Expected: " + ' or '.join([type(t()).__name__ for t in types]) + ". "
        msg += f"Got: " + type(val).__name__
        abort_with_message(msg, 400)
    return val


def get_str_field(data, field, mn, mx):
    val = get_field(data, field, [str])
    l = len(val)
    if l < mn or l > mx:
        msg = f"Invalid length of field '{field}'. "
        msg += f"Allowed range is [{mn}; {mx}]. "
        msg += f"Got {l}"
        abort_with_message(msg, 400)
    return val


def cur_user():
    if g.get('user', None) is None:
        user_id = session.get("user_id")
        g.user = User.query.get(user_id) if user_id is not None else None
    return g.user


def require_login():
    if cur_user() is None:
        abort_with_message("Login required", 401)
