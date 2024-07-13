from flask import render_template, flash, redirect, url_for, request
import sqlalchemy as sa
from app import db
from . import bp
from .forms import EditFanForm, FanForm
from app.models import Fan

@bp.route('/', methods=['GET', 'POST'])
def fans_index():
    if Fan.query.count() == 0:
      return redirect(url_for('.newfan'))
    form = FanForm(request.form)
    if form.validate_on_submit():
        if fan := Fan.query.filter_by(name=form.name.data).first():
          fan.swtch = form.swtch.data
          fan.speed = round(form.speed.data)
          db.session.commit()
    forms = [FanForm(formdata=None, obj=fan) for fan in Fan.query.all()]
    return render_template('fans_index.html', title='Fans!', forms=forms)

@bp.route('/newfan', methods=['GET', 'POST'])
def newfan():
    fan = Fan()
    form = EditFanForm(disp_title='New Fan')
    if form.validate_on_submit():
      fan.name = form.name.data
      fan.id = form.id.data 
      fan.has_swtch = form.has_swtch.data == 'True'
      fan.swtch_pin = form.swtch_pin.data 
      fan.has_pwm = form.has_pwm.data == 'True'
      fan.pwm_pin = form.pwm_pin.data
      fan.swtch = False
      fan.speed = 0
      db.session.add(fan)
      db.session.commit()
      flash('Created new fan {}'.format(fan.name))
      return redirect(url_for('fans.fans_index'))
    elif request.method == 'GET':
       print('GET')
       #do something
    
    return render_template('edit_fan.html', title='New Fan', form=form)

@bp.route('/editfan', methods=['GET', 'POST'])
def edit_fan():
    fan = Fan.query.filter_by(name=request.args.get('name')).first()
    if fan == None:
       flash('Fan {} not found'.format(request.args.get('name')))
       return redirect(url_for('fans.fans_index'))
       #todo: handle errors better
    form = EditFanForm(request.form)
    if form.validate_on_submit():
      fan.name = form.name.data
      fan.id = form.serial.data
      fan.has_swtch = form.has_swtch.data == 'True'
      fan.swtch_pin = form.swtch_pin.data 
      fan.has_pwm = form.has_pwm.data == 'True'
      fan.pwm_pin = form.pwm_pin.data
      db.session.commit()
      flash('Edited fan {}'.format(fan.name))
      return redirect(url_for('fans.fans_index'))
    elif request.method == 'GET':
       form.disp_title.data = 'Edit Fan'
       form.name.data = fan.name
       form.serial.data = fan.id
       form.has_swtch.data = str(fan.has_swtch)
       form.swtch_pin.data = fan.swtch_pin
       form.has_pwm.data = str(fan.has_pwm)
       form.pwm_pin.data = fan.pwm_pin
    
    return render_template('edit_fan.html', title='Edit Fan', form=form)
