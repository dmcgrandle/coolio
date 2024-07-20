from flask import render_template, flash, redirect, url_for, request
import sqlalchemy as sa
from app import db
from . import bp
from .forms import FanForm, EditFanForm
from app.models import Fan

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
          db.session.delete(fan)
          flash(f'DELETED Fan: {form.name.data}')
        else:
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
      fan.copy_from_form(form)
      db.session.add(fan)
      db.session.commit()
      flash(prefixes[1]+f' fan {fan.name}')
      return redirect(url_for('.fans_index'))
    return render_template('edit_fan.html', title=prefixes[0]+' fan', form=form)
