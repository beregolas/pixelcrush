import hashlib
from os import getenv
from dotenv import load_dotenv
from flask import Flask

from .authentication import register_authentication
from .crusher import Crusher
from .controllers import images, homepage, place


class MissingEnvironmentException(Exception):
    """ An Exception for when crucial environment variables are missing """
    pass


class CrusherApp(Flask):
    """ A normal Flask app object, with additional fields """
    crusher: Crusher


def create_app():
    """ The main factory function for the server. This is called by flask as an entry point. All server configuration
    happens here
    """

    # 1) load environment variables
    # this overrides system environment variables.
    load_dotenv('.env', override=True)

    # 2) start Flask server and set Flask options
    app = CrusherApp(__name__, instance_relative_config=True)
    secret_key = getenv('SECRET_KEY')
    if secret_key is None:
        raise MissingEnvironmentException('SECRET_KEY not found in environment variables')
    app.config.from_mapping(
        SECRET_KEY=secret_key
    )

    # 3) initialize the crusher
    # app.crusher = Crusher('')

    # 4) register all paths with our app
    register_paths(app)

    # 5) setup authentication
    register_authentication(app)

    return app


def register_paths(app):
    """ Registers all paths(blueprints) to the app

    Parameters
    ----------
    app
        the Flask app object

    Returns
    -------

    """
    app.register_blueprint(images.bp)
    app.register_blueprint(homepage.bp)
    app.register_blueprint(place.bp)
