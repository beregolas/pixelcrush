from os import getenv
from flask import Blueprint, redirect

bp = Blueprint('homepage', __name__)

homepage = getenv('PROJECT_HOMEPAGE')


@bp.route('/')
def favicon():
    return redirect(homepage)
