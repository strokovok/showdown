from flask import Blueprint
from flask import current_app


bp = Blueprint("avatars", __name__, url_prefix="/avatars/")

@bp.route("/get/<name>", methods=["GET"])
def get_avatar(name):
    return send_from_directory(current_app.config['AVATARS_PATH'], name)
