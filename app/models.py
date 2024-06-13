from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db

class Fan(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64), unique=True)
    # speed is the latest speed reading
    speed: so.Mapped[int] = so.mapped_column()
    # speed_readings is the history list of speeds changed.
    speed_readings: so.WriteOnlyMapped['SpeedChange'] = so.relationship(back_populates='fan')
    def __repr__(self):
        return '<Fan {} - last speed {}>'.format(self.name, self.speed)

class SpeedChange(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    fan_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Fan.id), index=True)
    speed: so.Mapped[int] = so.mapped_column()
    fan: so.Mapped[Fan] = so.relationship(back_populates='speed_readings')
    timestamp: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
    change_reason: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    def __repr__(self):
        return '<Speed {}'.format(self.speed)+', Change Reason {}'.format(self.change_reason)+', fan {}>'.format(self.fan)

class Sensor(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64), unique=True)
    temps: so.WriteOnlyMapped['TempReading'] = so.relationship(back_populates='sensor')
    def __repr__(self):
        return '<Sensor {}>'.format(self.name)
    
class TempReading(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    sensor_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Sensor.id), index=True)
    temp: so.Mapped[int] = so.mapped_column()
    timestamp: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
    sensor: so.Mapped[Sensor] = so.relationship(back_populates='temps')
    def __repr__(self):
        return '<Temp {}>'.format(self.temperature)
