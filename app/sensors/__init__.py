from flask import Blueprint

bp = Blueprint('sensors', __name__, template_folder='templates', static_folder='static')

from app.sensors import scheduled_tasks
from app.sensors import forms, routes