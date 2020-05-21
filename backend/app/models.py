import enum
import json

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import deferred
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from .database import db


def gen_json(obj, fields=None, rels=None, list_rels=None):
    res = dict()
    if fields is not None:
        for field in fields:
            name, f = field if isinstance(field, tuple) else (field, lambda x: x)
            if f is not None:
                val = getattr(obj, name)
                res[name] = val if f == True else f(val)
    if rels is not None:
        for name, opts in rels.items():
            if opts is not None:
                args = opts if isinstance(opts, dict) else dict()
                res[name] = getattr(obj, name).to_json(**args)
    if list_rels is not None:
        for name, opts in list_rels.items():
            if opts is not None:
                args = opts if isinstance(opts, dict) else dict()
                res[name] = [x.to_json(**args) for x in getattr(obj, name)]
    return res


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String, unique=True, nullable=False)
    reg_time = db.Column(db.DateTime, nullable=False, server_default=db.func.current_timestamp())
    description = db.Column(db.String, nullable=False, server_default="")
    detailed_description = db.Column(db.String, nullable=False, server_default="")
    _password = db.Column('password', db.String, nullable=False)

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = generate_password_hash(value)

    def check_password(self, value):
        return check_password_hash(self.password, value)

    def to_json(self, bots=None, description=None, detailed_description=None):
        return gen_json(self,
            fields=[
                "id",
                "login",
                ("reg_time", str),
                ("description", description),
                ("detailed_description", detailed_description)
            ],
            list_rels={"bots": bots}
        )


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String, nullable=False, server_default="")
    detailed_description = db.Column(db.String, nullable=False, server_default="")
    _manager_token = db.Column('manager_token', db.String, nullable=False)

    @hybrid_property
    def manager_token(self):
        return self._manager_token

    @manager_token.setter
    def manager_token(self, value):
        self._manager_token = generate_password_hash(value)

    def check_manager_token(self, value):
        return check_password_hash(self.manager_token, value)

    def to_json(self, bots=None, matches=None, description=None, detailed_description=None):
        return gen_json(self,
            fields=[
                "id",
                "name",
                ("description", description),
                ("detailed_description", detailed_description)
            ],
            list_rels={"bots": bots, "matches": matches}
        )


class Bot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    creation_time = db.Column(db.DateTime, nullable=False, server_default=db.func.current_timestamp())
    description = db.Column(db.String, nullable=False, server_default="")
    detailed_description = db.Column(db.String, nullable=False, server_default="")
    rank = db.Column(db.Float, nullable=False)

    owner_id = db.Column(db.ForeignKey(User.id), nullable=False)
    owner = db.relationship(User, lazy=False, uselist=False, backref=db.backref('bots', lazy=True, uselist=True))

    game_id = db.Column(db.ForeignKey(Game.id), nullable=False)
    game = db.relationship(Game, lazy=False, uselist=False, backref=db.backref('bots', lazy=True, uselist=True))

    _access_token = db.Column('access_token', db.String, nullable=False)

    @hybrid_property
    def access_token(self):
        return self._access_token

    @access_token.setter
    def access_token(self, value):
        self._access_token = generate_password_hash(value)

    def check_access_token(self, value):
        return check_password_hash(self.access_token, value)

    def to_json(self, owner=None, game=None, matches=None, description=None, detailed_description=None):
        return gen_json(self,
            fields=[
                "id",
                "name",
                ("creation_time", str),
                "rank",
                "owner_id",
                "game_id",
                ("description", description),
                ("detailed_description", detailed_description)
            ],
            rels={"owner": owner, "game": game},
            list_rels={"matches": matches}
        )


bots_matches = db.Table('bots_matches',
    db.Column('bot_id', db.Integer, db.ForeignKey('bot.id'), primary_key=True),
    db.Column('match_id', db.Integer, db.ForeignKey('match.id'), primary_key=True)
)


class MatchState(enum.Enum):
    CREATED = 1
    INPROCESS = 2
    FINISHED = 3
    CANCELLED = 4


class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    creation_time = db.Column(db.DateTime, nullable=False, server_default=db.func.current_timestamp())
    start_time = db.Column(db.DateTime, nullable=True)
    end_time = db.Column(db.DateTime, nullable=True)
    state = db.Column(db.Enum(MatchState), nullable=False)
    results = db.Column(db.String, nullable=False, server_default="{}")
    data = deferred(db.Column(db.String, nullable=False, server_default="{}"))

    game_id = db.Column(db.ForeignKey(Game.id), nullable=False)
    game = db.relationship(Game, lazy=False, uselist=False, backref=db.backref('matches', lazy=True, uselist=True))

    participants = db.relationship(
        Bot,
        secondary=bots_matches,
        lazy=True, uselist=True,
        backref=db.backref('matches', lazy=True, uselist=True)
    )

    def to_json(self, data=None, game=None, participants=None):
        return gen_json(self,
            fields=[
                "id",
                ("creation_time", str),
                ("start_time", str),
                ("end_time", str),
                ("state", lambda s: s.value),
                ("results", json.loads),
                ("data", json.loads if data else None),
                "game_id"
            ],
            rels={"game": game},
            list_rels={"participants": participants}
        )
