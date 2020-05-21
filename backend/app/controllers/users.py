from flask import Blueprint

from app.database import db
from app.models import User

from .utils.getters import get_user
from .utils.helpers import cur_user
from .utils.helpers import get_json_request
from .utils.helpers import require_login


bp = Blueprint("users", __name__, url_prefix="/api/users")


@bp.route("/", methods=["GET"])
def get_users_list():
    return {
        "users": [ user.to_json() for user in User.query.all() ]
    }


@bp.route("/<int:id>", methods=["GET"])
def get_user_route(id):
    return get_user(id=id).to_json(description=True, detailed_description=True)


@bp.route("/update", methods=["POST"])
def update_user():
    require_login()

    schema = {
        "type": "object",
        "properties": {
            "description": {"type": "string", "maxLength": 50},
            "detailed_description": {"type": "string"},
        }
    }
    req = get_json_request(schema)

    user = cur_user()
    user.description = req.get('description', user.description)
    user.detailed_description = req.get('detailed_description', user.detailed_description)
    db.session.commit()

    return user.to_json(description=True, detailed_description=True)
