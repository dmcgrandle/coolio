from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, validators, IntegerField, SubmitField
from wtforms.validators import DataRequired

class EditSensorForm(FlaskForm):
    disp_title = StringField('Display Title')
    name = StringField('Name', validators=[DataRequired()])
    serial = StringField('Serial', validators=[DataRequired()])
    type = SelectField('Sensor Type', choices=[('None', ''), ('Temp Sensor', 'Temp Sensor')], validate_choice=False)
    model = SelectField('Sensor Model', choices=[('None', ''), ('DS18B20', 'DS18B20')], validate_choice=True)
    submit = SubmitField('Save Fan')

class SensorForm(FlaskForm):
    name = IntegerField('Temp', validators=[DataRequired()])
    serial = StringField('Serial')
    type = StringField('Sensor Type')
    model = StringField('Sensor Model')
    edit = SubmitField('Edit Fan', render_kw={'class': 'btn btn-outline-warning'})
    delete = SubmitField('Delete Fan', render_kw={'class': 'btn btn-outline-danger'})

