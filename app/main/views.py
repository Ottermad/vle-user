"""Views file."""
from flask import Blueprint

from .models import *

main_blueprint = Blueprint('main', __name__)


@main_blueprint.route("/")
def index():
    return "Index"
