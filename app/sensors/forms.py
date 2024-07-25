from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, validators, IntegerField, SubmitField
from wtforms.validators import DataRequired


class EditTempSensorForm(FlaskForm):
    disp_title = StringField('Display title')
    name = StringField('Name', validators=[DataRequired()])
    id = StringField('Serial', validators=[DataRequired()])
    type = SelectField('Sensor type', choices=[
                       '', 'Temp Sensor'], validate_choice=False)
    model = SelectField('Sensor model', choices=[
                        '', 'DS18B20', 'Internal Pi'], validate_choice=False)
    cancel = SubmitField('Cancel', render_kw={
                         'class': 'btn btn-outline-secondary'})
    save = SubmitField('Save', render_kw={'class': 'btn btn-outline-success'})


class SensorForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    type = StringField('Sensor type')
    edit = SubmitField('Edit sensor', render_kw={
                       'class': 'btn btn-outline-warning'})
    delete = SubmitField('Delete sensor', render_kw={
                         'class': 'btn btn-outline-danger'})


class NewSensorForm(FlaskForm):
    type = SelectField('Sensor type', choices=[
                       '', 'Temp Sensor'], validate_choice=False)
    cancel = SubmitField('Cancel', render_kw={
                         'class': 'btn btn-outline-secondary'})
    next = SubmitField('Next', render_kw={'class': 'btn btn-outline-success'})
