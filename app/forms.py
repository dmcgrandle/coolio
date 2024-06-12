from flask_wtf import FlaskForm
from wtforms import DecimalRangeField, validators, SubmitField
from wtforms.validators import DataRequired

class FansForm(FlaskForm):
    slider_val = DecimalRangeField('Slider Value', validators=[DataRequired()])
    submit = SubmitField('Enter Data')
