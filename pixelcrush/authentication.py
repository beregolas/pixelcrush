import string
from base64 import b64decode
from http import HTTPStatus
from flask import request, Response, current_app


def authenticate(auth: string):
    try:
        if auth is None:
            return False
        auth_type, auth_content = auth.split(' ')
        if auth_type == 'Basic':
            # decode base64 and convert to string
            auth_name, auth_password = str(b64decode(auth_content))[2:-1].split(':')
            if auth_name == 'admin' and auth_password == current_app.config['SECRET_KEY']:
                return True
    except Exception as e:
        print(f'Handled authentication error: {e}')
        pass
    return False


def register_authentication(app):
    @app.before_request
    def authenticate_request():
        if request.endpoint \
                and getattr(app.view_functions[request.endpoint], 'protected', False) \
                and not request.method == 'OPTIONS':
            request.authenticated = authenticate(request.headers.get('Authorization', None))
            if not request.authenticated and getattr(app.view_functions[request.endpoint], 'auth_required', True):
                return Response('Authentication failed', status=HTTPStatus.UNAUTHORIZED)
            pass
        pass
    pass


def add_authentication(required):
    def _add_authentication(controller):
        controller.protected = True
        controller.auth_required = required
        return controller
    return _add_authentication
