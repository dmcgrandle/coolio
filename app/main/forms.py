from flask_wtf import FlaskForm
from wtforms import DecimalRangeField, BooleanField, StringField, HiddenField, SubmitField, SelectField , validators, IntegerField, FloatField
from wtforms.validators import DataRequired

class EditAutomationForm(FlaskForm):
    disp_title = StringField('Display Title')
    name = StringField('Name', validators=[DataRequired()])
    sensor = SelectField('Choose a sensor', choices=[('False', ''), ('True', 'Yes'), ('False', 'No')], validate_choice=False)
    fan = SelectField('Choose a fan', choices=[(False, ''), (True, 'Yes'), (False, 'No')], validate_choice=False)
    temp_max = FloatField('Maximum Temperature', validators=[DataRequired()])
    temp_min = FloatField('Minimum Temperature', validators=[DataRequired()])
    submit = SubmitField('Save Automation')

class AutomationForm(FlaskForm):
    name = HiddenField('Name')
    sensor = StringField('Sensor', render_kw={'class': 'sensor'})
    fan = StringField('Fan', render_kw={'class': 'fan'})
    temp_max = FloatField('Maximum Temperature')
    temp_min = FloatField('Minimum Temperature')
    edit = SubmitField('Edit Fan', render_kw={'class': 'btn btn-outline-warning'})
    delete = SubmitField('Delete Fan', render_kw={'class': 'btn btn-outline-danger'})

