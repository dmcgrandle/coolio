from datetime import datetime, timezone
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db

class Sensor(db.Model):
    id: so.Mapped[str] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64), unique=True)
    type: so.Mapped[str] = so.mapped_column(sa.String(64)) # future: other than temperature sensor

class TempSensor(Sensor):
    model: so.Mapped[str] = so.mapped_column(sa.String(64)) # exact model
    
    auto: so.WriteOnlyMapped['Automation'] = so.relationship(back_populates='temp_sensor')
    readings: so.WriteOnlyMapped['TempReading'] = so.relationship(back_populates='temp_sensor')

    def __repr__(self):
        return f'<Temp Sensor {self.name} type: {self.type} model: {self.model}>'
    
# Reading is the database table that holds historical timestamped sensor readings
class Reading(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    timestamp: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))

class TempReading(Reading):
    temp: so.Mapped[float] = so.mapped_column() # the temperature in degrees Fahrenheit

    temp_sensor_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(TempSensor.id), index=True)
    temp_sensor: so.Mapped[TempSensor] = so.relationship(back_populates='readings')

    def __repr__(self):
        return f'<Temp Reading: {self.sensor.name} Time: {self.timestamp} Temp {self.temp}>'

class Fan(db.Model):
    id: so.Mapped[str] = so.mapped_column(sa.String(36), primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64), unique=True)
    has_swtch: so.Mapped[bool] = so.mapped_column()
    swtch_pin: so.Mapped[int] = so.mapped_column()
    has_pwm: so.Mapped[bool] = so.mapped_column()
    pwm_pin: so.Mapped[int] = so.mapped_column()
# current_state variables:
    swtch: so.Mapped[bool] = so.mapped_column()
    speed: so.Mapped[int] = so.mapped_column()
# mapped var pointing to table of past speed changes
    speed_changes: so.WriteOnlyMapped['SpeedChange'] = so.relationship(back_populates='fan', passive_deletes=True)
    auto: so.WriteOnlyMapped['Automation'] = so.relationship(back_populates='fan', passive_deletes=True)
    
    def __repr__(self):
        return '<Fan {} - on? {} - last speed {}>'.format(self.name, self.is_on, self.speed)
    
    def __init__(self, form=None):
        super().__init__()
        if form: self.copy_from_form(form)
        self.swtch = False
        self.speed = 0
        return self

    def copy_from_form(self, form):
        for key, value in form.data.items():
          if hasattr(self, key):
            setattr(self, key, value)
        if self.speed:
          self.speed = round(self.speed) # workaround because DecimalRangeField can't coerce to int
        return self

class SpeedChange(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    speed: so.Mapped[int] = so.mapped_column()
    timestamp: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
    change_reason: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    fan_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Fan.id), index=True)
# mapped var pointing to the fan this speed_change is for
    fan: so.Mapped[Fan] = so.relationship(back_populates='speed_changes')

    def __repr__(self):
        return '<Speed {}'.format(self.speed)+', Change Reason {}'.format(self.change_reason)+', fan {}>'.format(self.fan)

class Automation(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64), unique=True)
    temp_max: so.Mapped[float] = so.mapped_column()
    temp_min: so.Mapped[float] = so.mapped_column()
    enabled: so.Mapped[bool] = so.mapped_column()
    sensor_name: so.Mapped[str] = so.mapped_column(sa.String(64))
    fan_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Fan.id), index=True)
    temp_sensor_id: so.Mapped[str] = so.mapped_column(sa.ForeignKey(TempSensor.id), index=True)
    
    fan: so.Mapped[Fan] = so.relationship(back_populates='auto')
    temp_sensor: so.Mapped[TempSensor] = so.relationship(back_populates='auto')

    def __init__(self, form=None):
        super().__init__()
        if form:
          self.copy_from_form(form)
        return self
    
    def copy_from_form(self, form):
        self.name = form.name.data
        self.sensor_name = form.sensor_name.data
        self.fan_name = form.fan_name.data
        self.temp_max = form.temp_max.data
        self.temp_min = form.temp_min.data
        if form.enabled.data == None:
          self.enabled = False
        else:
          self.enabled = form.enabled.data
        return self
