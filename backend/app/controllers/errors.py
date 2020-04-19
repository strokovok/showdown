import enum

from flask import abort
from flask import make_response


class ErrorMessage(enum.Enum):
    INVALID_JSON = (1, "Invalid JSON data.", 400)
    MISSING_FIELD = (2, "Missing field '{field}'.", 400)
    INVALID_FIELD_TYPE = (3, "Invalid type of field '{field}'. Expected: {expected}. Got: {got}.", 400)
    INVALID_FIELD_LENGTH = (4, "Invalid length of field '{field}'. Allowed range is [{mn}; {mx}]. Got {l}.", 400)
    LOGIN_REQUIRED = (5, "Login required.", 401)
    USER_LOGIN_ALREADY_EXISTS = (6, "User with login '{login}' already exists.'", 400)
    NO_SUCH_USER_LOGIN = (7, "No such user with login '{login}.'", 404)
    INCORRECT_PASSWORD = (8, "Incorrect password.", 400)
    NO_SUCH_USER_ID = (9, "No such user with id '{id}'.", 404)
    NO_SUCH_GAME_ID = (10, "No such game with id '{id}'.", 404)

    def abort(self, **kwargs):
        abort(make_response({
            "error_code": self.value[0],
            "error_message": self.value[1].format(**kwargs)
        }, self.value[2]))
