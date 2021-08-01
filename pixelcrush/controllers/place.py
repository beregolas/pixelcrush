from flask import Blueprint
from pixelcrush.authentication import require_authentication

bp = Blueprint('place', __name__, url_prefix='/place')


@bp.route('/admin', methods=['POST'])
@require_authentication
def overwrite():

    return 'test'

    pass
