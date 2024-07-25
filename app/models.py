"""datetime Module providing datetime and timezone."""
from datetime import datetime, timezone
from typing import ClassVar
import sqlalchemy as sa
import sqlalchemy.orm as so
import RPi.GPIO as GPIO
from app import db, scheduler
from .environment_state import EnvStateMachine


def copy_to_obj_from_form(obj, form):
    """Function to copy form data into class variables."""
    for key, value in form.data.items():
        if hasattr(obj, key):
            setattr(obj, key, value)
    return obj


class Sensor(db.Model):
    """General class for a Sensor such as Temperature, Humidity, etc"""
    id: so.Mapped[str] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64), unique=True)
    # future: other than temperature sensor
    type: so.Mapped[str] = so.mapped_column(sa.String(64))

class TempSensor(Sensor):
    """Temperature Sensor class, derived from Sensor"""
    model: so.Mapped[str] = so.mapped_column(sa.String(64))  # exact model

    auto: so.WriteOnlyMapped['Automation'] = so.relationship(
        back_populates='temp_sensor')
    readings: so.WriteOnlyMapped['TempReading'] = so.relationship(
        back_populates='temp_sensor')

    def __repr__(self):
        return f'<Temp Sensor {self.name} type: {self.type} model: {self.model}>'

    def __init__(self, form=None):
        super().__init__()
        if form:
            self.copy_from_form(form)
        # return self

    def copy_from_form(self, form):
        """class method to call general copy function"""
        copy_to_obj_from_form(self, form)
        return self

# Reading is the database table that holds historical timestamped sensor readings


class Reading(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc))


class TempReading(Reading):
    # the temperature in degrees Fahrenheit
    temp: so.Mapped[float] = so.mapped_column()

    temp_sensor_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey(TempSensor.id), index=True)
    temp_sensor: so.Mapped[TempSensor] = so.relationship(
        back_populates='readings')

    def __repr__(self):
        return f'<Temp Reading: {self.temp_sensor.name} Time: {self.timestamp} Temp {self.temp}>'


class Fan(db.Model):
    id: so.Mapped[str] = so.mapped_column(sa.String(36), primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64), unique=True)
    has_swtch: so.Mapped[bool] = so.mapped_column()
    swtch_pin: so.Mapped[int] = so.mapped_column()
    has_pwm: so.Mapped[bool] = so.mapped_column()
    pwm_channel: so.Mapped[int] = so.mapped_column()
# current_state variables:
    swtch: so.Mapped[bool] = so.mapped_column()
    speed: so.Mapped[int] = so.mapped_column()
# mapped var pointing to table of past speed changes
    speed_changes: so.WriteOnlyMapped['SpeedChange'] = so.relationship(
        back_populates='fan', passive_deletes=True)
    auto: so.WriteOnlyMapped['Automation'] = so.relationship(
        back_populates='fan', passive_deletes=True)

    def __repr__(self):
        return '<Fan {} - on? {} - last speed {}>'.format(self.name, self.is_on, self.speed)

    def __init__(self, form=None):
        super().__init__()
        if form:
            self.copy_from_form(form)
        self.swtch = False
        self.speed = 0
        # return self

    def copy_from_form(self, form):
        copy_to_obj_from_form(self, form)
        if self.speed:
            # workaround because DecimalRangeField can't coerce to int
            self.speed = round(self.speed)
        return self


class SpeedChange(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    speed: so.Mapped[int] = so.mapped_column()
    timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc))
    change_reason: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    fan_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey(Fan.id), index=True)
# mapped var pointing to the fan this speed_change is for
    fan: so.Mapped[Fan] = so.relationship(back_populates='speed_changes')

    def __repr__(self):
        return f'<Speed {self.speed} Change Reason {self.change_reason}, fan {self.fan}>'


class Automation(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64), unique=True)
    temp_max: so.Mapped[float] = so.mapped_column()
    temp_min: so.Mapped[float] = so.mapped_column()
    enabled: so.Mapped[bool] = so.mapped_column()
    fan_id: so.Mapped[str] = so.mapped_column(
        sa.ForeignKey(Fan.id), index=True)
    temp_sensor_id: so.Mapped[str] = so.mapped_column(
        sa.ForeignKey(TempSensor.id), index=True)

    fan: so.Mapped[Fan] = so.relationship(back_populates='auto')
    temp_sensor: so.Mapped[TempSensor] = so.relationship(
        back_populates='auto', lazy='subquery')

    sm: ClassVar[EnvStateMachine] = None

    def __init__(self, form=None):
        super().__init__()
        if form:
            self.copy_from_form(form)
        # return self

    def copy_from_form(self, form):
        copy_to_obj_from_form(self, form)
        # if not self.temp_sensor:
        self.temp_sensor = TempSensor.query.filter_by(
            name=form.temp_sensor_name.data).first()
        # if not self.fan:
        self.fan = Fan.query.filter_by(name=form.fan_name.data).first()
        # return self

    def start_automation(self):
        from .sensors.sensor_tasks import DS18B20_temp_reading, Internal_Pi_temp_reading
        # setup the GPIO pins
        GPIO.setup(self.fan.swtch_pin, GPIO.OUT)
        # activate the state machine
        sm = EnvStateMachine(self)
        sm.activate_initial_state()
        # start regular temp readings
        if self.temp_sensor.model == 'DS18B20':
            scheduler.add_job(func=DS18B20_temp_reading, args=[
                             sm, self.temp_sensor, self.id], trigger='interval', minutes=5, id=f'auto-{self.id}')
        elif self.temp_sensor.model == 'Internal Pi':
            scheduler.add_job(func=Internal_Pi_temp_reading, args=[
                             sm, self.temp_sensor, self.id], trigger='interval', minutes=5, id=f'auto-{self.id}')

    def stop_automation(self):
        # start regular temp readings
        scheduler.remove_job(id=f'auto-{self.id}')
        GPIO.cleanup(self.fan.swtch_pin)
        GPIO.setup(self.fan.swtch_pin, GPIO.IN)
        # if os.environ.get('WERKZEUG_RUN_MAIN') == "true":
        # with app.app_context():
        #   print('load scheduler')
        #   from app.sensors import scheduled_tasks
        #   scheduler.start()

        #  from app.main.environment_state import EnvStateMachine
        #  app.sm = EnvStateMachine()
        #  app.sm.activate_initial_state()
