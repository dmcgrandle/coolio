from flask_wtf import FlaskForm
from wtforms import DecimalRangeField, BooleanField, StringField, HiddenField, SubmitField, SelectField , validators, IntegerField
from wtforms.validators import DataRequired

class EditFanForm(FlaskForm):
    disp_title = StringField('Display Title')
    name = StringField('Name', validators=[DataRequired()])
    id = StringField('Serial', validators=[DataRequired()])
    has_swtch = SelectField('Pi can swtch fan power', choices=[('False', ''), ('True', 'Yes'), ('False', 'No')], validate_choice=False)
    swtch_pin = IntegerField('GPIO PIN used for switch', validators=[DataRequired()])
    has_pwm = SelectField('Pi can control speed via PWM', choices=[(False, ''), (True, 'Yes'), (False, 'No')], validate_choice=False)
    pwm_pin = IntegerField('GPIO PIN used for PWM', validators=[DataRequired()])
    submit = SubmitField('Save Fan')

class FanForm(FlaskForm):
    name = HiddenField('Name')
    swtch = BooleanField('Switch', render_kw={'class': 'swtch'})
    speed = DecimalRangeField('Speed', render_kw={'class': 'speed'}, validators=[DataRequired()])
    edit = SubmitField('Edit Fan', render_kw={'class': 'btn btn-outline-warning'})
    delete = SubmitField('Delete Fan', render_kw={'class': 'btn btn-outline-danger'})
