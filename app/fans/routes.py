from flask import render_template, flash, redirect, url_for, request
import sqlalchemy as sa
from app import db
from . import bp
from .forms import FanForm
from app.models import Fan

@bp.route('/', methods=['GET', 'POST'])
def fans_index():
    if Fan.query.count() == 0:
      return redirect(url_for('.new_fan'))
    form = FanForm(request.form)
    if form.validate_on_submit():
      if fan := Fan.query.filter_by(name=form.name.data).first():
        if form.edit.data == True:
          return redirect(url_for('.edit_fan')+'?name='+fan.name)
        elif form.delete.data == True:
          db.session.delete(fan)
          flash(f'DELETED Automation: {form.name.data}')
        else:
          fan.copy_from_form(form)
          #todo: launch the automation
        db.session.commit()
    forms = [FanForm(formdata=None, obj=fan) for fan in Fan.query.all()]
    return render_template('fans_index.html', title='Fans', forms=forms)

@bp.route('/new_fan', methods=['GET', 'POST'])
def new_fan():
    form = FanForm(disp_title='New Fan')
    if form.validate_on_submit():
      fan = Fan(form)
      db.session.add(fan)
      db.session.commit()
      flash('Created new fan {}'.format(fan.name))
      return redirect(url_for('fans.fans_index'))
    return render_template('edit_fan.html', title='New Fan', form=form)

@bp.route('/edit_fan', methods=['GET', 'POST'])
def edit_fan():
    fan = Fan.query.filter_by(name=request.args.get('name')).first()
    if fan == None:
       flash('Fan {} not found'.format(request.args.get('name')))
       return redirect(url_for('fans.fans_index'))
       #todo: handle errors better
    form = FanForm(obj=fan, disp_title='Edit Fan')
    if form.validate_on_submit():
      fan.copy_from_form(form)
      db.session.commit()
      flash('Edited fan {}'.format(fan.name))
      return redirect(url_for('fans.fans_index'))
    return render_template('edit_fan.html', title='Edit Fan', form=form)
