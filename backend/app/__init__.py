import os

from flask import Flask


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.url_map.strict_slashes = False
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(app.instance_path, 'showdown.sqlite'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        AVATARS_PATH = os.path.join(app.instance_path, "avatars")
    )
    os.makedirs(app.instance_path, exist_ok=True)
    os.makedirs(app.config['AVATARS_PATH'], exist_ok=True)

    app.config.from_pyfile('config.py', silent=True)

    from .models import User, Game, Bot, Match

    from . import database
    database.init_app(app)

    from . import fill_db
    fill_db.init_app(app)

    from .controllers import auth, users, games, bots, matches, avatars
    app.register_blueprint(auth.bp)
    app.register_blueprint(users.bp)
    app.register_blueprint(games.bp)
    app.register_blueprint(bots.bp)
    app.register_blueprint(matches.bp)
    app.register_blueprint(avatars.bp)

    return app
