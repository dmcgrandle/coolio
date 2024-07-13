import pytz
from flask import render_template, flash, redirect, url_for, request
from urllib.parse import urlsplit
import sqlalchemy as sa
from app import db
from app.sensors import bp
from app.sensors.forms import EditSensorForm, SensorForm
from app.models import TempSensor

@bp.route('/', methods=['GET', 'POST'])
def sensors_index():
    sensors = TempSensor.query.all()
    if sensors.__len__() == 0:
      return redirect(url_for('sensors.new_sensor'))
    form = SensorForm(request.form)
    if form.validate_on_submit():
      for sensor in sensors:
        if sensor.name == form.name.data:
          if form.edit.data == True:
            return redirect(url_for('sensors.new_sensor')+'?name='+sensor.name)
          elif form.delete.data == True:
            db.session.delete(sensor)
            db.session.commit()
            flash('Sensor {} DELETED!'.format(form.name.data))
            return redirect(url_for('sensors.sensors_index'))
          else:
            pass #todo: implement error conditions
    else: #request.method == 'GET'
       pass
    forms = []
    for sensor in sensors:
      query = sensor.readings.select()
      reading = db.session.scalars(query).first()
      form = SensorForm()
      form.name.data = sensor.name
      if reading:
        form.reading.data = reading.temp
        form.timestamp.data = reading.timestamp.astimezone(
            pytz.timezone('America/Los_Angeles')
          ).strftime('%m/%d/%y, %H:%M:%S')
      form.serial.data = sensor.id
      form.type.data = sensor.type
      form.model.data = sensor.model
      forms.append(form)
    return render_template('sensors_index.html', title='Sensors', forms=forms)

@bp.route('/newsensor', methods=['GET', 'POST'])
def new_sensor():
    sensor = TempSensor()
    form = EditSensorForm(disp_title='New Sensor')
    if form.validate_on_submit():
      sensor.name = form.name.data
      sensor.id = form.serial.data 
      sensor.type = form.type.data
      sensor.model = form.model.data
      db.session.add(sensor)
      db.session.commit()
      flash('Created new {} named {}'.format(sensor.type, sensor.name))
      return redirect(url_for('sensors.sensors_index'))
    return render_template('edit_sensor.html', title='New Sensor', form=form)

@bp.route('/editsensor', methods=['GET', 'POST'])
def edit_sensor():
    sensor = TempSensor.query.filter_by(name=request.args.get('name')).first()
    if sensor == None:
       flash('Sensor {} not found'.format(request.args.get('name')))
       return redirect(url_for('sensors.sensors_index'))
    form = EditSensorForm(request.form)
    if form.validate_on_submit():
      sensor.name = form.name.data
      sensor.id = form.serial.data 
      sensor.type = form.type.data
      sensor.model = form.model.data
      db.session.commit()
      flash('Edited {} named {}'.format(sensor.type, sensor.name))
      return redirect(url_for('sensors.sensors_index'))
    elif request.method == 'GET':
       form.disp_title.data = 'Edit Sensor'
       form.name.data = sensor.name
       form.serial.data = sensor.id
       form.type.data = sensor.type
       form.model.data = sensor.model
    return render_template('edit_sensor.html', title='Edit Sensor', form=form)