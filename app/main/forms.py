from flask_wtf import FlaskForm
from wtforms import DecimalRangeField, BooleanField, StringField, HiddenField, SubmitField, SelectField , validators, IntegerField, FloatField
from wtforms.validators import DataRequired
from app.models import TempSensor, Fan

def set_fan_and_sensor_from_obj(form, auto):
    form.temp_sensor_name.choices = [sensor.name for sensor in TempSensor.query.all()]
    form.fan_name.choices = [fan.name for fan in Fan.query.all()]
    if auto:
      if auto.temp_sensor and not form.save.data == True:
        form.temp_sensor_name.data = auto.temp_sensor.name
      if auto.fan and not form.save.data == True:
        form.fan_name.data = auto.fan.name
    return form

class AutomationForm(FlaskForm):
    name = HiddenField('Name')
    temp_sensor_name = SelectField('Choose a sensor', validate_choice=False)
    fan_name = SelectField('Choose a fan', validate_choice=False)
    temp_max = FloatField('Maximum temperature')
    temp_min = FloatField('Minimum temperature')
    enabled = BooleanField('Enabled', render_kw={'class': 'enable'})
    edit = SubmitField('Edit automation', render_kw={'class': 'btn btn-outline-warning'})
    delete = SubmitField('Delete automation', render_kw={'class': 'btn btn-outline-danger'})
    cancel = SubmitField('Cancel', render_kw={'class': 'btn btn-outline-secondary'})
    save = SubmitField('Save automation', render_kw={'class': 'btn btn-outline-primary'})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self = set_fan_and_sensor_from_obj(self, kwargs.get('obj'))

class EditAutomationForm(AutomationForm):
    disp_title = StringField('Display title')
    name = StringField('Name', validators=[DataRequired()])
    temp_max = FloatField('Maximum temperature', validators=[DataRequired()])
    temp_min = FloatField('Minimum temperature', validators=[DataRequired()])
