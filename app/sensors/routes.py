import pytz
from flask import render_template, flash, redirect, url_for, request
from urllib.parse import urlsplit
import sqlalchemy as sa
from app import db
from app.sensors import bp
from app.sensors.forms import EditTempSensorForm, SensorForm, NewSensorForm
from app.models import Sensor, TempSensor

@bp.route('/', methods=['GET', 'POST'])
def sensors_index():
    if Sensor.query.count() == 0:
      return redirect(url_for('.new_sensor'))
    form = SensorForm(request.form)
    if form.validate_on_submit():
      if sensor := Sensor.query.filter_by(name=form.name.data).first():
        if form.edit.data == True and sensor.type == 'Temp Sensor':
          return redirect(url_for('.edit_temp_sensor')+'?name='+sensor.name)
        # future: add redirect for another sensor.type here
        elif form.delete.data == True:
          db.session.delete(sensor)
          flash(f'DELETED Sensor: {form.name.data}')
        else:
          pass # nothing to update with SensorForm
        db.session.commit()
      else:
         pass #todo: handle error of name not found
    data = []
    for sensor in Sensor.query.all():
      form = SensorForm(formdata=None, obj=sensor)
      type_sensor = None
      reading = None
      if sensor.type == 'Temp Sensor':
        type_sensor = TempSensor.query.filter_by(name=sensor.name).first()
        reading = db.session.scalars(type_sensor.readings.select()).first()
      # elif sensor.type == 'Another': #todo: add for another sensor.type
      data.append((form, type_sensor, reading))
    return render_template('sensors_index.html', title='Sensors', data=data)

@bp.route('/edit_temp_sensor', methods=['GET', 'POST'])
def edit_temp_sensor():
    if (name := request.args.get('name')) == '_new_':
      temp_sensor = TempSensor()
      prefixes = ('New', 'Created New')
    else:
      temp_sensor = TempSensor.query.filter_by(name=name).first()
      if not temp_sensor:
        flash('Error: Temperature Sensor {name} was not found')
        return redirect(url_for('.sensors_index'))
      prefixes = ('Edit', 'Edited')
    form = EditTempSensorForm(request.form)
    if form.validate_on_submit():
      temp_sensor.copy_from_form(form)
      db.session.add(temp_sensor)
      db.session.commit()
      flash(f'{prefixes[1]} Temp Sensor named {temp_sensor.name}')
      return redirect(url_for('.sensors_index'))
    form = EditTempSensorForm(formdata=None, obj=temp_sensor)
    return render_template('edit_temp_sensor.html', title=f'{prefixes[0]} Temp Sensor', form=form)