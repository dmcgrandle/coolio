from flask import Blueprint

bp = Blueprint('main', __name__)

from app import environment_state
from app.main import routes, forms
