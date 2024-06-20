from datetime import datetime, timezone
from typing import Optional
#from flask import current_app
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

class Sensor(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64), unique=True)

    temps: so.WriteOnlyMapped['TempReading'] = so.relationship(back_populates='sensor')
    tasks: so.WriteOnlyMapped['Task'] = so.relationship(back_populates='sensor')

    def __repr__(self):
        return '<Sensor {}>'.format(self.name)
    
#    def add_notification(self, name, data):
#        db.session.execute(self.notifications.delete().where(Notification.name == name))
#        return name
    
    def launch_task(self, name, description, *args, **kwargs):
        rq_job = current_app.task_queue.enqueue(f'app.tasks.{name}', self.id, *args, **kwargs)
        task = Task(id=rq_job.get_id(), name=name, description=description, user=self)
        db.session.add(task)
        return task

    def get_tasks_in_progress(self):
        query = self.tasks.select().where(Task.complete == False)
        return db.session.scalars(query)

    def get_task_in_progress(self, name):
        query = self.tasks.select().where(Task.name == name, Task.complete == False)
        return db.session.scalar(query)
    
# TempReading is the database table that holds historical timestamped temperature readings
class TempReading(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    sensor_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Sensor.id), index=True)
    temp: so.Mapped[int] = so.mapped_column()
    timestamp: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))

    sensor: so.Mapped[Sensor] = so.relationship(back_populates='temps')

    def __repr__(self):
        return '<Temp {}>'.format(self.temperature)

# Task is a class that communicates with an independent process through a RQ message queue
# to get temperature readings - this class tracks "task" jobs that are executed, not the actual
# temperature readings (see TempReading class for that)
class Task(db.Model):
    id: so.Mapped[str] = so.mapped_column(sa.String(36), primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(128), index=True)
    description: so.Mapped[Optional[str]] = so.mapped_column(sa.String(128))
    complete: so.Mapped[bool] = so.mapped_column(default=False)
    sensor_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Sensor.id))

    sensor: so.Mapped[Sensor] = so.relationship(back_populates='tasks')

    def get_rq_job(self):
        try:
            rq_job = rq.job.Job.fetch(self.id, connection=current_app.redis)
        except (redis.exceptions.RedisError, rq.exceptions.NoSuchJobError):
            return None
        return rq_job

    def get_progress(self):
        job = self.get_rq_job()
        return job.meta.get('progress', 0) if job is not None else 100