from flask_wtf import FlaskForm
from wtforms import DecimalRangeField, BooleanField, validators
from wtforms.validators import DataRequired

class SliderFanForm(FlaskForm):
    speed = DecimalRangeField('Speed', validators=[DataRequired()])

class SwitchFanForm(FlaskForm):
    is_on = BooleanField('Switch', validators=[DataRequired()])
