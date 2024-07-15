from flask import render_template, redirect, request, flash, url_for
from app import db
from . import bp
from app.models import Automation, Fan, TempSensor
from .forms import AutomationForm, EditAutomationForm

@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html')

@bp.route('/automations')
def automations():
    if Automation.query.count() == 0:
      return redirect(url_for('.newautomation'))
    form = AutomationForm(request.form)
    if form.validate_on_submit():
        if auto := Automation.query.filter_by(name=form.name.data).first():
          if form.edit.data == True:
            return redirect(url_for('.editautomation')+'?name='+auto.name)
          elif form.delete.data == True:
            db.session.delete(auto)
            db.session.commit()
            flash('Automation {} DELETED!'.format(form.name.data))
            # return redirect(url_for('.automations'))
          else:
            pass #todo: implement error conditions

          auto.enabled = form.enabled.data
          db.session.commit()
    forms = [AutomationForm(formdata=None, obj=auto) for auto in Automation.query.all()]
    return render_template('automations.html', title='Automations', forms=forms)

@bp.route('/newautomation', methods=['GET', 'POST'])
def newautomation():
    if Fan.query.count() == 0:
      flash(f'Need to create at least one fan before creating automations')
      redirect(url_for('main.index'))
    if TempSensor.query.count() == 0:
      flash(f'Need to create at least one Temp Sensor before creating automations')
      redirect(url_for('main.index'))
    form = EditAutomationForm(disp_title='New Automation')
    if form.validate_on_submit():
      # if auto := Automation.query.filter_by(name=form.name.data).first():
      auto = Automation(form)
      db.session.add(auto)
      db.session.commit()
      flash(f'Created new automation {auto.name}')
      return redirect(url_for('main.automations'))
    elif request.method == 'GET':
       form.sensor_name.choices = [sensor.name for sensor in TempSensor.query.all()]
       form.fan_name.choices = [fan.name for fan in Fan.query.all()]
    return render_template('edit_automation.html', title='New Automation', form=form)

@bp.route('/editautomation', methods=['GET', 'POST'])
def editautomation():
    if not (auto := Automation.query.filter_by(name=request.args.get('name')).first()):
      flash(f'Fan {request.args.get("name")} not found')
      return redirect(url_for('fans.fans_index'))
      #todo: handle errors better
    form = EditAutomationForm(request.form, disp_title='Edit Automation')
    if form.validate_on_submit():
      #if auto := Automation.query.filter_by(name=form.name.data).first():
        auto.name = form.name.data
        auto.sensor = form.sensor.data
        auto.fan = form.fan.data
        auto.temp_max = form.temp_max.data
        auto.temp_min = form.temp_min.data
        db.session.add(auto)
        db.session.commit()
        flash(f'Created new automation {auto.name}')
        return redirect(url_for('main.automations'))
    elif request.method == 'GET':
       form.sensor_name.choices = [sensor.name for sensor in TempSensor.query.all()]
       form.fan_name.choices = [fan.name for fan in Fan.query.all()]
    return render_template('edit_automation.html', title='Edit Automation', form=form)