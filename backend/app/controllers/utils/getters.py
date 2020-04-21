from app.models import User, Game, Bot, Match

from .errors import ErrorMessage


def get_entity(model, params, error_obj, fail):
    if 'id' in params:
        entity = model.query.get(params['id'])
    else:
        entity = model.query.filter_by(**params).first()
    if entity is None and fail:
        error_obj.abort(params=params)
    return entity


def get_user(fail=True, **params):
    return get_entity(User, params, ErrorMessage.NO_SUCH_USER, fail)


def get_game(fail=True, **params):
    return get_entity(Game, params, ErrorMessage.NO_SUCH_GAME, fail)


def get_bot(fail=True, **params):
    return get_entity(Bot, params, ErrorMessage.NO_SUCH_BOT, fail)
