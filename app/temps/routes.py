from flask import render_template, flash, redirect, url_for, request
from urllib.parse import urlsplit
import sqlalchemy as sa
from app import db
from app.temps import bp
from app.temps.forms import TempForm
from app.temps.models import Sensor, TempReading, TempTask

@bp.route('/', methods=['GET', 'POST'])
def temps_index():
    temps = [
        {'name': 'Outside HP Room', 'tempF': '65'},
        {'name': 'Back of Cabinet', 'tempF': '80'},
        {'name': 'By Dreamwall', 'tempF': '72'},
    ]
    query = sa.select(Sensor).where(Sensor.name == 'Testing')
    test_sensor = db.session.scalar(query)
    if test_sensor is None:
        test_sensor = Sensor(id='0000006a41e9', name='Testing')
        db.session.add(test_sensor)
        db.session.commit()
        flash('Created new sensor {}'.format(test_sensor.name))
    temp_form = TempForm()
    if temp_form.validate_on_submit():
        sensor = test_sensor
#        sensor.launch_task('read_temperature', 'Taking Temp Reading...')
        
    return render_template('temps_index.html', form=temp_form, temps=temps)