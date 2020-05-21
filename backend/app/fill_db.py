import click
import random

from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy

from .controllers.utils.rank_system import DEFAULT_RANK
from .database import db
from .models import User, Game, Bot, Match, MatchState


def init_app(app):
    app.cli.add_command(fill_db_command)


def fill_db():
    tmp = {
        "Алиса": ["Терминатор", "Мегатрон"],
        "Боб": ["Пылесос", "Чайник"],
        "Дмитрий": ["T-2000", "R2-D2"],
        "Петр": ["С-3PO", "Эш"],
        "Данил": ["Рой Батти", "Вертер"],
        "Вадим": ["Бишоп", "Робокоп"],
        "Владимир": ["Эндрю", "Бендер"],
        "Сергей": ["Sonny NS5", "Оптимус"],
    }
    game = Game(name='Крестики нолики', manager_token='password')
    db.session.add(game)
    for login, bot_names in tmp.items():
        user = User(login=login, password='password')
        db.session.add(user)
        for bot_name in bot_names:
            bot = Bot(name=bot_name, rank=DEFAULT_RANK, owner=user, game=game, access_token='password')
            db.session.add(bot)
    db.session.commit()


@click.command('fill-db')
@with_appcontext
def fill_db_command():
    fill_db()
    click.echo('Filled the database.')
