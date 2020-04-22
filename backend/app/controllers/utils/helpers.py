import random
import string
import jsonschema

from flask import g
from flask import request
from flask import session

from .errors import ErrorMessage
from .getters import get_game
from .getters import get_user


def get_json_request(schema=None):
    if g.get("json_request", None) is None:
        g.json_request = request.get_json(force=True)
        if g.json_request is None:
            ErrorMessage.INVALID_JSON.abort()

    if schema is not None:
        try:
            jsonschema.validate(g.json_request, schema)
        except jsonschema.exceptions.ValidationError as e:
            ErrorMessage.INVALID_JSON_STRUCTURE.abort(message=e.message)

    return g.json_request


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


def require_game_management():
    schema = {
        "type": "object",
        "properties": {
            "game": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "manager_token": {"type": "string"}
                },
                "required": ["id", "manager_token"]
            }
        },
        "required": ["game"]
    }
    req = get_json_request(schema)
    game_id, token = req["game"]["id"], req["game"]["manager_token"]

    game = get_game(id=id)
    if not game.check_manager_token(token):
        ErrorMessage.INCORRECT_MANAGER_TOKEN.abort()

    return game
