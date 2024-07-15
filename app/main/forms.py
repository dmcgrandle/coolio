from flask_wtf import FlaskForm
from wtforms import DecimalRangeField, BooleanField, StringField, HiddenField, SubmitField, SelectField , validators, IntegerField, FloatField
from wtforms.validators import DataRequired

class EditAutomationForm(FlaskForm):
    disp_title = StringField('Display Title')
    name = StringField('Name', validators=[DataRequired()])
    sensor_name = SelectField('Choose a sensor', validate_choice=False)
    fan_name = SelectField('Choose a fan', validate_choice=False)
    temp_max = FloatField('Maximum Temperature', validators=[DataRequired()])
    temp_min = FloatField('Minimum Temperature', validators=[DataRequired()])
    submit = SubmitField('Save Automation')

class AutomationForm(FlaskForm):
    name = HiddenField('Name')
    sensor_name = StringField('Sensor', render_kw={'class': 'sensor'})
    fan_name = StringField('Fan', render_kw={'class': 'fan'})
    temp_max = FloatField('Maximum Temperature')
    temp_min = FloatField('Minimum Temperature')
    enabled = BooleanField('Enabled')
    edit = SubmitField('Edit Automation', render_kw={'class': 'btn btn-outline-warning'})
    delete = SubmitField('Delete Automation', render_kw={'class': 'btn btn-outline-danger'})

