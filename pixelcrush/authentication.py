import string
from base64 import b64decode
from http import HTTPStatus
from os import getenv
from flask import request, Response

secret_key = getenv('SECRET_KEY')


def authenticate(auth: string):
    try:
        auth_type, auth_content = auth.split(' ')
        if auth_type == 'Basic':
            # decode base64 and convert to string
            auth_name, auth_password = str(b64decode(auth_content))[2:-1].split(':')
            if auth_name == 'admin' and auth_password == secret_key:
                return True
    except Exception as e:
        print(e)
        print('Error during authentication')
        pass
    return False


def register_authentication(app):
    @app.before_request
    def authenticate_request():
        if request.endpoint \
                and getattr(app.view_functions[request.endpoint], 'protected', False) \
                and not request.method == 'OPTIONS':
            authenticated = authenticate(request.headers.get('Authorization', None))
            if not authenticated:
                return Response('Authentication failed', status=HTTPStatus.UNAUTHORIZED)
            pass
        pass
    pass


def require_authentication(controller):
    controller.protected = True
    return controller
