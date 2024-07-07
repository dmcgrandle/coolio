from datetime import datetime, timezone
from typing import Optional
from flask import current_app
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db

class Sensor(db.Model):
    id: so.Mapped[str] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64), unique=True)
    type: so.Mapped[str] = so.mapped_column(sa.String(64)) # could be other than temperature sensor

    readings: so.WriteOnlyMapped['Reading'] = so.relationship(back_populates='sensor')

    def __repr__(self):
        return '<Sensor {} type: {}>'.format(self.name, self.type)
    
    def take_reading(self):
        pass

class TempSensor(Sensor):
    model: so.Mapped[str] = so.mapped_column(sa.String(64)) # exact model

    def __repr__(self):
        return '<Temp Sensor {} type: {} model: {}>'.format(self.name, self.type, self.model)
    
    
# Reading is the database table that holds historical timestamped sensor readings
class Reading(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    sensor_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Sensor.id), index=True)
    temp: so.Mapped[int] = so.mapped_column() # the temperature in degrees Fahrenheit
    timestamp: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))

    sensor: so.Mapped[Sensor] = so.relationship(back_populates='readings')

    def __repr__(self):
        return '<Time: {} Temp {}>'.format(self.timestamp, self.temp)

class TempReading(Reading):
    pass