from flask_wtf import FlaskForm
from wtforms import DecimalRangeField, validators, SubmitField, StringField
from wtforms.validators import DataRequired

class FansForm(FlaskForm):
    name = StringField('All')
    speed = DecimalRangeField('Speed', validators=[DataRequired()])
    submit = SubmitField('Change Speed')
