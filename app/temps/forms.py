from flask_wtf import FlaskForm
from wtforms import DecimalRangeField, BooleanField, validators, IntegerField
from wtforms.validators import DataRequired

class TempForm(FlaskForm):
    temp = IntegerField('Temp', validators=[DataRequired()])
