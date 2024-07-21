from flask import render_template, flash, redirect, url_for, request, current_app
import sqlalchemy as sa
from app import db
from . import bp
from .forms import FanForm, EditFanForm
from app.models import Fan
import RPi.GPIO as GPIO

@bp.route('/', methods=['GET', 'POST'])
def fans_index():
    if Fan.query.count() == 0:
      return redirect(url_for('.edit_fan')+'?name=_new_')
    form = FanForm(request.form)
    if form.validate_on_submit():
      if fan := Fan.query.filter_by(name=form.name.data).first():
        if form.edit.data == True:
          return redirect(url_for('.edit_fan')+'?name='+fan.name)
        elif form.delete.data == True:
          GPIO.cleanup(fan.swtch_pin)
          db.session.delete(fan)
          flash(f'DELETED Fan: {form.name.data}')
        else:
          if not fan.swtch and form.swtch: #fan is being turned on
            GPIO.output(fan.swtch_pin, GPIO.HIGH)
          elif fan.swtch and not form.swtch: #fan is being turned off
            GPIO.output(fan.swtch_pin, GPIO.LOW)
          elif fan.speed != form.speed: #change to fan.speed needed
            current_app.pwm[fan.pwm_channel].change_duty_cycle(form.speed)
          else:
            flash(f'Unknown reason for POST: {form.name.data}')
            current_app.logger.warning('Fans Index: unknown reason for POST')
          fan.copy_from_form(form)
        db.session.commit()
    forms = [FanForm(formdata=None, obj=fan) for fan in Fan.query.all()]
    return render_template('fans_index.html', title='Fans', forms=forms)

@bp.route('/edit_fan', methods=['GET', 'POST'])
def edit_fan():
    if (name := request.args.get('name')) == '_new_':
      fan = Fan()
      prefixes = ('New', 'Created new')
    else:
      fan = Fan.query.filter_by(name=name).first()
      if not fan:
        flash('Error: fan "{name}" was not found')
        return redirect(url_for('.fans_index'))
      prefixes = ('Edit', 'Edited')
    form = EditFanForm(obj=fan, disp_title=prefixes[0]+' fan')
    if form.validate_on_submit():
      if form.cancel.data: 
         return redirect(url_for('.fans_index'))
      if fan.has_swtch and (fan.swtch_pin != form.swtch_pin):
        GPIO.cleanup(fan.swtch_pin) # pin is changing, cleanup old one
      fan.copy_from_form(form)
      if fan.has_swtch:
        GPIO.setup(fan.swtch_pin, GPIO.OUT) # set up new pin
      db.session.add(fan)
      db.session.commit()
      flash(prefixes[1]+f' fan {fan.name}')
      return redirect(url_for('.fans_index'))
    return render_template('edit_fan.html', title=prefixes[0]+' fan', form=form)
