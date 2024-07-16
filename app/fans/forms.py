from flask_wtf import FlaskForm
from wtforms import DecimalRangeField, BooleanField, StringField, HiddenField, SubmitField, SelectField , validators, IntegerField
from wtforms.validators import DataRequired

class FanForm(FlaskForm):
    disp_title = StringField('Display Title')
    name = StringField('Name', validators=[DataRequired()])
    id = StringField('Serial', validators=[DataRequired()])
    swtch = BooleanField('Switch', render_kw={'class': 'swtch'})
    speed = DecimalRangeField('Speed', render_kw={'class': 'speed'}, validators=[DataRequired()])
    has_swtch = SelectField('Pi can swtch fan power', choices=[(False, ''), (True, 'Yes'), (False, 'No')], validate_choice=False)
    swtch_pin = IntegerField('GPIO PIN used for switch', validators=[DataRequired()])
    has_pwm = SelectField('Pi can control speed via PWM', choices=[(False, ''), (True, 'Yes'), (False, 'No')], validate_choice=False)
    pwm_pin = IntegerField('GPIO PIN used for PWM', validators=[DataRequired()])
    edit = SubmitField('Edit Fan', render_kw={'class': 'btn btn-outline-warning'})
    delete = SubmitField('Delete Fan', render_kw={'class': 'btn btn-outline-danger'})
    submit = SubmitField('Save Fan')

# class FanForm(FlaskForm):
#     name = HiddenField('Name')
#     id = HiddenField('id')
#     swtch = BooleanField('Switch', render_kw={'class': 'swtch'})
#     speed = DecimalRangeField('Speed', render_kw={'class': 'speed'}, validators=[DataRequired()])
#     has_swtch = HiddenField('has_swtch')
#     swtch_pin = HiddenField('swtch_pin')
#     has_pwm = HiddenField('has_pwm')
#     pwm_pin = HiddenField('pwm_pin')
#     edit = SubmitField('Edit Fan', render_kw={'class': 'btn btn-outline-warning'})
#     delete = SubmitField('Delete Fan', render_kw={'class': 'btn btn-outline-danger'})
