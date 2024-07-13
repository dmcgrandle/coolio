from flask import Blueprint

bp = Blueprint('main', __name__)

from app.main import environment_state, routes, forms
