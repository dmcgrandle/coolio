from flask_wtf import FlaskForm
from wtforms import DecimalRangeField, BooleanField, StringField, SubmitField, SelectField , validators, IntegerField
from wtforms.validators import DataRequired

class NewFanForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    serial = StringField('Serial', validators=[DataRequired()])
    has_switch = SelectField('Pi can switch fan power', choices=[('False', ''), ('True', 'Yes'), ('False', 'No')], validate_choice=False)
    switch_pin = IntegerField('GPIO PIN used for switch', validators=[DataRequired()])
    has_pwm = SelectField('Pi can control speed via PWM', choices=[(False, ''), (True, 'Yes'), (False, 'No')], validate_choice=False)
    pwm_pin = IntegerField('GPIO PIN used for PWM', validators=[DataRequired()])
    submit = SubmitField('Save Fan')

class FanForm(FlaskForm):
    name = StringField('Name')
    serial = StringField('Serial')
    is_on = BooleanField('Switch')
    speed = DecimalRangeField('Speed', render_kw={'class': 'speed'}, validators=[DataRequired()])
    submit = SubmitField('Save Fan')
    ident = StringField()


