import os

from flask import Blueprint, send_from_directory, current_app as app

bp = Blueprint('images', __name__)


@bp.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
