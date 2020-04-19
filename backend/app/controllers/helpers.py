from flask import g
from flask import request
from flask import session

from app.models import User

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
        user_id = session.get("user_id")
        g.user = User.query.get(user_id) if user_id is not None else None
    return g.user


def require_login():
    if cur_user() is None:
        ErrorMessage.LOGIN_REQUIRED.abort()
