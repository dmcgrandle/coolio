from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, validators, IntegerField, SubmitField
from wtforms.validators import DataRequired

class EditTempSensorForm(FlaskForm):
    disp_title = StringField('Display Title')
    name = StringField('Name', validators=[DataRequired()])
    id = StringField('Serial', validators=[DataRequired()])
    type = SelectField('Sensor Type', choices=['', 'Temp Sensor'], validate_choice=False)
    model = SelectField('Sensor Model', choices=['', 'DS18B20'], validate_choice=False)
    submit = SubmitField('Save Sensor')

class SensorForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    type = StringField('Sensor Type')
    edit = SubmitField('Edit Sensor', render_kw={'class': 'btn btn-outline-warning'})
    delete = SubmitField('Delete Sensor', render_kw={'class': 'btn btn-outline-danger'})

class NewSensorForm(FlaskForm):
    type = SelectField('Sensor Type', choices=['', 'Temp Sensor'], validate_choice=False)
    cancel = SubmitField('Cancel', render_kw={'class': 'btn btn-outline-secondary'})
    next = SubmitField('Next', render_kw={'class': 'btn btn-outline-success'})
