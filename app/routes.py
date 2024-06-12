from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import FansForm

@app.route('/')
@app.route('/index')
def index():
    temps = [
        {'name': 'Outside HP Room', 'tempF': '65'},
        {'name': 'Back of Cabinet', 'tempF': '80'},
        {'name': 'By Dreamwall', 'tempF': '72'},
    ]
    return render_template('index.html', temps=temps)

@app.route('/fans', methods=['GET', 'POST'])
def fans():
    form = FansForm()
    if form.validate_on_submit():
        flash('New data in slider {}'.format(
            form.slider_val.data))
        return redirect(url_for('index'))
    return render_template('fans.html', title='Fans!', form=form)