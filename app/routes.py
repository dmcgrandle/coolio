from flask import render_template, flash, redirect, url_for, request
import sqlalchemy as sa
from app import app, db
from app.forms import FansForm
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
    form = FansForm()
    query = sa.select(Fan).where(Fan.name == 'All')
    fan = db.session.scalar(query)
    if fan is None:
      # need to create the default 'All' fan if it doesn't exist
      fan = Fan(name='All', speed=20)
      db.session.add(fan)
      db.session.commit()
      flash('Created new fan {}'.format(fan.name))
      return redirect(url_for('fans'))
    if form.validate_on_submit():
      form.speed.data = round(form.speed.data)
      fan.name = form.name.data
      fan.speed = round(form.speed.data)
      new_speed_reading = SpeedChange(fan=fan, speed=fan.speed, change_reason='Form Update')
      db.session.add(new_speed_reading) # save the new reading
      db.session.add(fan) # update the fan speed
      db.session.commit()
    elif request.method == 'GET':
       form.speed.data = fan.speed
       form.name.data = fan.name       
    return render_template('fans.html', title='Fans!', form=form)
