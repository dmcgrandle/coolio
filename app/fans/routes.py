from flask import render_template, flash, redirect, url_for, request
import sqlalchemy as sa
from app import db
from app.fans import bp
from app.fans.forms import SliderFanForm, SwitchFanForm, NewFanForm, FanForm
from app.fans.models import Fan, SpeedChange

@bp.route('/', methods=['GET', 'POST'])
def fans_index():
    fans = Fan.query.all() # query the database for all Fans
    if fans.__len__() == 0:
      return redirect(url_for('fans.newfan'))
    fans_and_forms =[]
    for fan in fans:
      form = FanForm()
      fans_and_forms.append((fan, form))
    for fan, form in fans_and_forms:
      if form.validate_on_submit():
        fan.is_on = form.is_on.data
        fan.speed = round(form.speed.data)
        db.session.commit()
#        db.session.add(fan)
#        db.session.commit()
        form.name.data = fan.name
      elif request.method == 'GET':
        form.name.data = fan.name
        form.serial.data = fan.id
        form.is_on.data = fan.is_on
        form.speed.data = fan.speed
        form.speed.data = fan.speed
        form.is_on.data = fan.is_on

    return render_template('fans_index.html', title='Fans!', fans_and_forms=fans_and_forms)

@bp.route('/newfan', methods=['GET', 'POST'])
def newfan():
    newfan = Fan()
    newfan_form = NewFanForm()
    if newfan_form.validate_on_submit():
      newfan.name = newfan_form.name.data
      newfan.id = newfan_form.serial.data 
      newfan.has_switch = newfan_form.has_switch.data == 'True'
      newfan.switch_pin = newfan_form.switch_pin.data 
      newfan.has_pwm = newfan_form.has_pwm.data == 'True'
      newfan.pwm_pin = newfan_form.pwm_pin.data
      newfan.is_on = False
      newfan.speed = 0
      db.session.add(newfan)
      db.session.commit()
      flash('Created new fan {}'.format(newfan.name))
      return redirect(url_for('fans.fans_index'))
    elif request.method == 'GET':
       print('GET')
       #do something
    
    return render_template('newfan.html', title='New Fan', newfan_form=newfan_form)
