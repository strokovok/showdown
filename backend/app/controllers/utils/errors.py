import enum

from flask import abort
from flask import make_response


class ErrorMessage(enum.Enum):

    # Parsing
    INVALID_JSON = (101, "Invalid JSON data.", 400)
    MISSING_FIELD = (102, "Missing field '{field}'.", 400)
    INVALID_FIELD_TYPE = (103, "Invalid type of field '{field}'. Expected: {expected}. Got: {got}.", 400)
    INVALID_FIELD_LENGTH = (104, "Invalid length of field '{field}'. Allowed range is [{mn}; {mx}]. Got {l}.", 400)

    # Auth
    LOGIN_REQUIRED = (201, "Login required.", 401)
    INCORRECT_PASSWORD = (202, "Incorrect password.", 400)

    # User
    NO_SUCH_USER = (301, "No such user with params {params}.", 404)
    USER_LOGIN_ALREADY_EXISTS = (302, "User with login '{login}' already exists.", 400)

    # Game
    NO_SUCH_GAME = (401, "No such game with params {params}.", 404)
    INCORRECT_MANAGER_TOKEN = (402, "Incorrect manager token.", 401)

    # Bot
    NO_SUCH_BOT = (501, "No such bot with params {params}", 404)
    BOT_NAME_ALREADY_EXISTS = (502, "Bot with name '{name}' already exists.", 400)
    NOT_YOUR_BOT = (503, "Bot with id '{id}' is not yours!", 401)


    def abort(self, **kwargs):
        abort(make_response({
            "error": {
                "code": self.value[0],
                "message": self.value[1].format(**kwargs),
                "details": kwargs
            }
        }, self.value[2]))
