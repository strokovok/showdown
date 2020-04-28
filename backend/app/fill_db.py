import click
import random

from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy

from .database import db
from .models import User, Game, Bot, Match, MatchState


def init_app(app):
    app.cli.add_command(fill_db_command)


def fill_db_old():
    games = []
    for i in range(3):
        game = Game(name=f'Game_{i}', manager_token=f'manager_token_{i}')
        db.session.add(game)
        games.append(game)

    for i in range(3):
        user = User(login=f'User_{i}', password=f'password_{i}')
        db.session.add(user)
        for j in range(3):
            bot = Bot(name=f'Bot_{i}_{j}', rank=0, owner=user, game=games[j], access_token=f'access_token_{i}')
            db.session.add(bot)

    for i in range(10):
        j = random.randint(0, 2)
        game = games[j]
        match = Match(
            state=MatchState(random.randint(1, 4)),
            game=game,
            participants=random.sample(game.bots, k=2)
        )
        db.session.add(match)
    db.session.commit()


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
            bot = Bot(name=bot_name, rank=0, owner=user, game=game, access_token='password')
            db.session.add(bot)
    db.session.commit()


@click.command('fill-db')
@with_appcontext
def fill_db_command():
    fill_db()
    click.echo('Filled the database.')
