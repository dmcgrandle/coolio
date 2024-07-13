from flask import render_template, redirect, request, url_for
from app import db
from . import bp
from app.models import Automation
from .forms import AutomationForm

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
          auto.swtch = form.swtch.data
          auto.speed = round(form.speed.data)
          db.session.commit()
    forms = [AutomationForm(formdata=None, obj=auto) for auto in Automation.query.all()]
    return render_template('automations.html', title='Automations', forms=forms)
