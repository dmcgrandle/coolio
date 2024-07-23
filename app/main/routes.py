from flask import render_template, redirect, request, flash, url_for
from app import db
from . import bp
from app.models import Automation, Fan, TempSensor
from .forms import AutomationForm, EditAutomationForm


@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html')


@bp.route('/automations', methods=['GET', 'POST'])
def automations():
    if Fan.query.count() == 0 or TempSensor.query.count() == 0:
        flash(f'Must have at least one fan and one Temp Sensor for automations')
        redirect(url_for('main.index'))
    if Automation.query.count() == 0:
        return redirect(url_for('.edit_automation')+'?name=_new_')
    form = AutomationForm(request.form)
    if form.validate_on_submit():
        if auto := Automation.query.filter_by(name=form.name.data).first():
            if form.edit.data == True:
                return redirect(url_for('.edit_automation')+'?name='+auto.name)
            elif form.delete.data == True:
                db.session.delete(auto)
                flash(f'DELETED Automation: {form.name.data}')
            elif form.enabled.data:
                auto.enabled = True
                auto.start_automation()
            else:
                auto.enabled = False
                auto.stop_automation()
            db.session.commit()
    forms = [AutomationForm(formdata=None, obj=auto)
             for auto in Automation.query.all()]
    return render_template('automations.html', title='Automations', forms=forms)


@bp.route('/edit_automation', methods=['GET', 'POST'])
def edit_automation():
    if Fan.query.count() == 0 or TempSensor.query.count() == 0:
        flash(f'Must have at least one fan and one Temp Sensor for automations')
        redirect(url_for('main.index'))
    if (name := request.args.get('name')) == '_new_':
        auto = Automation()
        prefixes = ('New', 'Created new')
    else:
        auto = Automation.query.filter_by(name=name).first()
        if not auto:
            flash('Error: automation {name} was not found')
            return redirect(url_for('.automations'))
        prefixes = ('Edit', 'Edited')
    form = EditAutomationForm(obj=auto, disp_title=prefixes[0]+' automation')
    if form.validate_on_submit():
        if form.cancel.data:
            return redirect(url_for('.automations'))
        auto.copy_from_form(form)
        db.session.add(auto)
        db.session.commit()
        flash(f'{prefixes[1]} automation named {auto.name}')
        return redirect(url_for('.automations'))
    return render_template('edit_automation.html', title=f'{prefixes[0]} automation', form=form)
