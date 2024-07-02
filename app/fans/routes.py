from flask import render_template, flash, redirect, url_for, request
import sqlalchemy as sa
from app import db
from app.fans import bp
from app.fans.forms import EditFanForm, FanForm
from app.fans.models import Fan

@bp.route('/', methods=['GET', 'POST'])
def fans_index():
    fans = Fan.query.all()
    if fans.__len__() == 0:
      return redirect(url_for('fans.newfan'))
    form = FanForm(request.form)
    if form.validate_on_submit():
      for fan in fans:
        if fan.name == form.name.data: 
          if form.edit.data == True:
             return redirect(url_for('fans.edit_fan')+'?name='+fan.name)
          if form.delete.data == True:
             db.session.delete(fan)
             db.session.commit()
             flash('Fan {} DELETED!'.format(form.name.data))
             return redirect(url_for('fans.fans_index'))
          fan.swtch = form.swtch.data
          fan.speed = round(form.speed.data)
          db.session.commit()
      return redirect(url_for('fans.fans_index'))
    else: # request.method == 'GET'
      pass
    forms = []
    for fan in fans:
      form = FanForm()
      form.name.data = fan.name
      form.swtch.data = fan.swtch
      form.speed.data = fan.speed
      forms.append(form)
    return render_template('fans_index.html', title='Fans!', forms=forms)

@bp.route('/newfan', methods=['GET', 'POST'])
def newfan():
    fan = Fan()
    form = EditFanForm(disp_title='New Fan')
    if form.validate_on_submit():
      fan.name = form.name.data
      fan.id = form.serial.data 
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
