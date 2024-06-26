from datetime import datetime, timezone
from typing import Optional
from flask import current_app
import sqlalchemy as sa
import sqlalchemy.orm as so
import redis
import rq
from app import db

class Fan(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64), unique=True)
    # if the fan has a switch controllable my the raspberry pi, save the is_on state
    is_on: so.Mapped[bool] = so.mapped_column()
    # speed_readings is the history list of speeds changed.
    # speed is the latest speed reading
    speed: so.Mapped[int] = so.mapped_column()
    speed_readings: so.WriteOnlyMapped['SpeedChange'] = so.relationship(back_populates='fan')
    def __repr__(self):
        return '<Fan {} - on? {} - last speed {}>'.format(self.name, self.is_on, self.speed)

class SpeedChange(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    speed: so.Mapped[int] = so.mapped_column()
    timestamp: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
    change_reason: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    fan_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Fan.id), index=True)

    fan: so.Mapped[Fan] = so.relationship(back_populates='speed_readings')

    def __repr__(self):
        return '<Speed {}'.format(self.speed)+', Change Reason {}'.format(self.change_reason)+', fan {}>'.format(self.fan)
