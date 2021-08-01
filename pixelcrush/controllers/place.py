from flask import Blueprint, request
from pixelcrush.authentication import add_authentication

bp = Blueprint('place', __name__, url_prefix='/place')


@bp.route('', methods=['POST'])
@add_authentication(False)
def set_pixel():
    print(request.authenticated)
    # TODO

    return 'test'

    pass


@bp.route('', methods=['GET'])
def get_image():
    # TODO
    return 'test'

    pass


@bp.route('/heatmap', methods=['GET'])
def get_heatmap():
    # TODO
    return 'test'

    pass


@bp.route('/hardness', methods=['GET'])
def get_hardness():
    # TODO
    return 'test'

    pass


