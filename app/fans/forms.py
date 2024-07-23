from flask_wtf import FlaskForm
from wtforms import DecimalRangeField, DecimalField, BooleanField, StringField, HiddenField, SubmitField, SelectField, validators, IntegerField
from wtforms.validators import DataRequired
from decimal import ROUND_HALF_UP


class FanForm(FlaskForm):
    name = HiddenField('Name')
    swtch = BooleanField('Turn fan on', render_kw={'class': 'swtch'})
    speed = DecimalRangeField(
        'Speed', render_kw={'class': 'speed'}, validators=[DataRequired()])
    edit = SubmitField('Edit fan', render_kw={
                       'class': 'btn btn-outline-warning'})
    delete = SubmitField('Delete fan', render_kw={
                         'class': 'btn btn-outline-danger'})


class EditFanForm(FlaskForm):
    disp_title = StringField('Display title')
    name = StringField('Name', validators=[DataRequired()])
    id = IntegerField('Serial', validators=[DataRequired()])
    has_swtch = SelectField('Pi can swtch fan power',
                            choices=['', 'Yes', 'No'],
                            validate_choice=False,
                            coerce=lambda x: x == 'Yes' or x == True)
    swtch_pin = IntegerField('GPIO PIN used for switch',
                             validators=[DataRequired()])
    has_pwm = SelectField('Pi can control speed via PWM',
                          choices=['', 'Yes', 'No'],
                          validate_choice=False,
                          coerce=lambda x: x == 'Yes' or x == True)
    pwm_channel = SelectField('PWM channel for this fan',
                              choices=['0', '1'],
                              validate_choice=False,
                              coerce=int)
    cancel = SubmitField('Cancel', render_kw={
                         'class': 'btn btn-outline-secondary'})
    save = SubmitField('Save Fan', render_kw={
                       'class': 'btn btn-outline-primary'})
