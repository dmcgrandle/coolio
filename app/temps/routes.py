from flask import render_template, flash, redirect, url_for, request
from urllib.parse import urlsplit
import sqlalchemy as sa
from app import db
from app.temps import bp
from app.temps.forms import TempForm
from app.models import Sensor, TempReading, Task


@bp.route('/', methods=['GET', 'POST'])
def temps_index():
    temps = [
        {'name': 'Outside HP Room', 'tempF': '65'},
        {'name': 'Back of Cabinet', 'tempF': '80'},
        {'name': 'By Dreamwall', 'tempF': '72'},
    ]
    return render_template('temps_index.html', temps=temps)