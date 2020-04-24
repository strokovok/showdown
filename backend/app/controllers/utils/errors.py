import enum

from flask import abort
from flask import make_response


class ErrorMessage(enum.Enum):

    # Parsing
    INVALID_JSON = (101, "Invalid JSON.", 400)
    INVALID_JSON_STRUCTURE = (102, "Invalid JSON structure: {message}.", 400)

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
    NO_SUCH_BOT = (501, "No such bot with params {params}.", 404)
    BOT_NAME_ALREADY_EXISTS = (502, "Bot with name '{name}' already exists.", 400)
    NOT_YOUR_BOT = (503, "Bot with id '{id}' is not yours!", 401)
    WRONG_BOT_GAME = (504, "Bot with id '{bot_id}' does not belong to game with id '{game_id}'.", 400)
    WRONG_BOT_MATCH = (505, "Bot with id '{bot_id}' doesn't participate in match with id '{match_id}'", 400)

    # Match
    NO_SUCH_MATCH = (601, "No such match with params {params}.", 404)
    WRONG_MATCH_GAME = (602, "Match with id '{match_id}' does not belong to game with id '{game_id}'.", 400)
    WRONG_MATCH_STATE = (603, "Can't do this action, because current match state is '{state}:{state_name}'", 400)
    MISSING_RESULT = (604, "Missing result of match '{match_id}' for bot '{bot_id}'", 400)


    def abort(self, **kwargs):
        abort(make_response({
            "error": {
                "code": self.value[0],
                "message": self.value[1].format(**kwargs),
                "details": kwargs
            }
        }, self.value[2]))
