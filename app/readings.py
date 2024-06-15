import sys
import time
import sqlalchemy as sa
from rq import get_current_job
from app import app, db 
from app.models import Task, Sensor, TempReading

#app = create_app()
#app.app_context().push()

def _set_task_progress(progress):
    job = get_current_job()
    if job:
        job.meta['progress'] = progress
        job.save_meta()
        task = db.session.get(Task, job.get_id())
#        task.sensor.add_notification('task_progress', {'task_id': job.get_id(), 'progress': progress})
        if progress >= 100:
            task.complete = True
        db.session.commit()

def read_temperature(sensor_id):
    try:
        sensor = db.session.get(Sensor, sensor_id)
        _set_task_progress(0)
        data = []
        i = 0
        total_temp_readings = db.session.scalar(sa.select(sa.func.count()).select_from(sensor.temps.select().subquery()))
        for temp_reading in db.session.scalars(sensor.temps.select().order_by(TempReading.timestamp.asc())):
            data.append({'temp': temp_reading.temp, 'timestamp': temp_reading.timestamp.isoformat() + 'Z'})
            time.sleep(5)
            i += 1
            _set_task_progress(100 * i // total_temp_readings)
    except Exception:
        _set_task_progress(100)
        app.logger.error('Unhandled exception', exc_info=sys.exc_info())
    finally:
        _set_task_progress(100)

def example(seconds):
    job = get_current_job()
    print('Starting task')
    for i in range(seconds):
        job.meta['progress'] = 100.0 * i / seconds
        job.save_meta()
        print(i)
        time.sleep(1)
    job.meta['progress'] = 100
    job.save_meta()
    print('Task completed')