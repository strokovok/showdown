import os

from flask import Flask


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI="sqlite:///" + os.path.join(app.instance_path, "showdown.sqlite"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )
    os.makedirs(app.instance_path, exist_ok=True)
    app.config.from_pyfile("config.py", silent=True)

    from . import database
    database.init_app(app)

    return app
