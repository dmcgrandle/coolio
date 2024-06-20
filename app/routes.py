from flask import render_template, flash, redirect, url_for, request
import sqlalchemy as sa
from app import app, db
from app.forms import SliderFanForm, SwitchFanForm
from app.models import Fan, SpeedChange

@app.route('/')
@app.route('/index')
def index():
    temps = [
        {'name': 'Outside HP Room', 'tempF': '65'},
        {'name': 'Back of Cabinet', 'tempF': '80'},
        {'name': 'By Dreamwall', 'tempF': '72'},
    ]
    return render_template('index.html', temps=temps)

@app.route('/fans', methods=['GET', 'POST'])
def fans():
    array_form = SliderFanForm()
    query = sa.select(Fan).where(Fan.name == 'Array')
    array_fan = db.session.scalar(query)
    if array_fan is None:
      # need to create the default 'Array' fan if it doesn't exist
      array_fan = Fan(name='Array', speed=20, is_on=True)
      db.session.add(array_fan)
      db.session.commit()
      flash('Created new fan {}'.format(array_fan.name))
    wayback_form = SwitchFanForm()
    query = sa.select(Fan).where(Fan.name == 'Wayback')
    wayback_fan = db.session.scalar(query)
    if wayback_fan is None:
      # need to create the default 'Wayback' fan if it doesn't exist
      wayback_fan = Fan(name='Wayback', speed=0, is_on=False)
      db.session.add(wayback_fan)
      db.session.commit()
      flash('Created new fan {}'.format(wayback_fan.name))
      return redirect(url_for('fans'))
    if array_form.validate_on_submit():
      array_form.speed.data = round(array_form.speed.data)
      array_fan.name = 'Array'
      array_fan.speed = array_form.speed.data
      new_speed_reading = SpeedChange(fan=array_fan, speed=array_fan.speed, change_reason='Form Update')
      db.session.add(new_speed_reading) # save the new reading
      db.session.add(array_fan) # update the fan speed
      db.session.commit()
    elif wayback_form.validate_on_submit():
      wayback_fan.name = 'Wayback'
      wayback_fan.is_on = wayback_form.is_on.data
      db.session.add(wayback_fan) # update the fan state
      db.session.commit()
    elif request.method == 'GET':
       array_form.speed.data = array_fan.speed
       wayback_form.is_on.data = wayback_fan.is_on
    return render_template('fans.html', title='Fans!', array_form=array_form, wayback_form=wayback_form)
