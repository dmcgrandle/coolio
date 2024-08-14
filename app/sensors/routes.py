import pytz
from flask import render_template, flash, redirect, url_for, request
from urllib.parse import urlsplit
import sqlalchemy as sa
from bokeh.plotting import figure, curdoc
from bokeh.embed import components 
from bokeh.themes import DARK_MINIMAL
from app import db
from app import db
from app.sensors import bp
from app.sensors.forms import EditTempSensorForm, SensorForm, NewSensorForm
from app.models import Sensor, TempSensor, TempReading


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
            db.session.commit()
        else:
            flash(f'Error: Sensor "{form.name.data}" was not found.')
            return redirect(url_for('main.index'))
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


@bp.route('/new_sensor', methods=['GET', 'POST'])
def new_sensor():
    form = NewSensorForm(request.form)
    if form.validate_on_submit():
        if form.cancel.data:
            return redirect(url_for('main.index'))
        elif form.next.data:
            if form.type.data == 'Temp Sensor':
                return redirect(url_for('.edit_temp_sensor')+'?name=_new_')
            else:
                flash('Currently only Temperature Sensors are implemented.')
    return render_template('new_sensor.html', title='New sensor', form=form)


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
    form = EditTempSensorForm(
        obj=temp_sensor, disp_title=prefixes[0]+' temperature sensor')
    if form.validate_on_submit():
        if form.cancel.data:
            return redirect(url_for('.sensors_index'))
        temp_sensor.copy_from_form(form)
        db.session.add(temp_sensor)
        db.session.commit()
        flash(f'{prefixes[1]} Temp Sensor named {temp_sensor.name}')
        return redirect(url_for('.sensors_index'))
    return render_template('edit_temp_sensor.html', title=f'{prefixes[0]} Temp Sensor', form=form)

@bp.route('/graphs/temp_readings')
def graph_temp_readings():
    if TempReading.query.count() == 0:
        flash('Error: Currently no Temp Readings.  Setup some Temp Sensors')
        return redirect(url_for('.new_sensor'))
    # Prepare the data
    x = [1, 2, 3, 4, 5]
    y1 = [6, 7, 2, 4, 5]
    y2 = [2, 4, 7, 2, 8]
    # Create a new plot

    p = figure(title="Multiple Lines Example", x_axis_label='X', y_axis_label='Y')
    # Add multiple lines
    p.line(x, y1, legend_label="Line 1", line_width=2, color="blue")
    p.line(x, y2, legend_label="Line 2", line_width=2, color="green")

    curdoc().theme = DARK_MINIMAL
    curdoc().add_root(p)

    # Get Chart Components 
    script, div = components(p) 
  
    # Return the components to the HTML template 
    return render_template('graph_readings.html', script=script, div=div) 
    #return render_template('graphs_index.html', title='Fans')
