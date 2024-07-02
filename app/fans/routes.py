from flask import render_template, flash, redirect, url_for, request
import sqlalchemy as sa
from app import db
from app.fans import bp
from app.fans.forms import NewFanForm, FanForm
from app.fans.models import Fan

@bp.route('/', methods=['GET', 'POST'])
def fans_index():
    
    def copy_fan(fan):
       form = FanForm()
       form.name.data = fan.name
       form.serial.data = fan.id
       form.swtch.data = fan.swtch
       form.speed.data = fan.speed
       return form

    def make_forms(fans):
      temp = []
      for fan in fans:
        form = copy_fan(fan)
        temp.append(form)
      return temp

    fans = Fan.query.all() # query the database for all Fans
    if fans.__len__() == 0:
      return redirect(url_for('fans.newfan'))
    form = FanForm(request.form)
    if form.validate_on_submit():
      for fan in fans:
        if fan.name == form.name.data: # only update the fan that was submitted
          fan.swtch = form.swtch.data
          fan.speed = round(form.speed.data)
          db.session.commit()
      return redirect(url_for('fans.fans_index'))
    else: # request.method == 'GET'
      pass
    forms = make_forms(fans)
    return render_template('fans_index.html', title='Fans!', forms=forms)

@bp.route('/newfan', methods=['GET', 'POST'])
def newfan():
    newfan = Fan()
    newfan_form = NewFanForm()
    if newfan_form.validate_on_submit():
      newfan.name = newfan_form.name.data
      newfan.id = newfan_form.serial.data 
      newfan.has_swtch = newfan_form.has_swtch.data == 'True'
      newfan.swtch_pin = newfan_form.swtch_pin.data 
      newfan.has_pwm = newfan_form.has_pwm.data == 'True'
      newfan.pwm_pin = newfan_form.pwm_pin.data
      newfan.swtch = False
      newfan.speed = 0
      db.session.add(newfan)
      db.session.commit()
      flash('Created new fan {}'.format(newfan.name))
      return redirect(url_for('fans.fans_index'))
    elif request.method == 'GET':
       print('GET')
       #do something
    
    return render_template('newfan.html', title='New Fan', newfan_form=newfan_form)
