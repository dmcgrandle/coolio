from flask import Blueprint

bp = Blueprint('fans', __name__, template_folder='templates', static_folder='static')

from app.fans import forms, routes