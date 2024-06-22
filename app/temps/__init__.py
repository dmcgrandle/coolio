from flask import Blueprint

bp = Blueprint('temps', __name__, template_folder='templates', static_folder='static')

from app.temps import forms, routes