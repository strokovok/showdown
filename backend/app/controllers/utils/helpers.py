import random
import string

from flask import g
from flask import request
from flask import session

from .getters import get_user
from .errors import ErrorMessage


def get_json_request():
    data = request.get_json(force=True)
    if data is None:
        ErrorMessage.INVALID_JSON.abort()
    return data


def get_field(data, field, types):
    if field not in data:
        ErrorMessage.MISSING_FIELD.abort(field=field)
    val = data[field]
    if type(val) not in types:
        ErrorMessage.INVALID_FIELD_TYPE.abort(
            field=field,
            expected=' or '.join([type(t()).__name__ for t in types]),
            got=type(val).__name__
        )
    return val


def get_str_field(data, field, mn, mx):
    val = get_field(data, field, [str])
    l = len(val)
    if l < mn or l > mx:
        ErrorMessage.INVALID_FIELD_LENGTH.abort(field=field, mn=mn, mx=mx, l=l)
    return val


def cur_user():
    if g.get('user', None) is None:
        id = session.get("user_id")
        g.user = get_user(id=id, fail=False) if id is not None else None
    return g.user


def require_login():
    if cur_user() is None:
        ErrorMessage.LOGIN_REQUIRED.abort()


def generate_token():
    base = string.ascii_lowercase
    base += string.ascii_uppercase
    base += string.digits
    return ''.join(random.choices(base, k=15))


def require_game_management(game):
    token = get_str_field(get_json_request(), 'manager_token', 1, 1000)
    if not game.check_manager_token(token):
        ErrorMessage.INCORRECT_MANAGER_TOKEN.abort()
