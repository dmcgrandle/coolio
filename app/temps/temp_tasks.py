import os, glob, sys, time
import sqlalchemy as sa
from rq import get_current_job
from app import create_app, db, scheduler
from app.temps.models import TempTask, Sensor, TempReading

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
temp_dir = '/sys/bus/w1/devices'
#device_folder = 'temp' # use for testing if there is no sensor attached
device_folder = glob.glob(temp_dir + '/28*')[0] #first temp sensor is 0
print('device folder is', device_folder)
device_file = device_folder + '/w1_slave'

app = create_app()
app.app_context().push()

def _set_task_progress(progress):
    job = get_current_job()
    if job:
        job.meta['progress'] = progress
        job.save_meta()
        task = db.session.get(TempTask, job.get_id())
#        task.sensor.add_notification('task_progress', {'task_id': job.get_id(), 'progress': progress})
        if progress >= 100:
            task.complete = True
        db.session.commit()

def read_temperature(sensor_id):
    
    def read_temp_raw():
        f = open(device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines
    
    def read_temp():
        lines = read_temp_raw()
        while lines[0].strip()[-3:] != 'YES':
          time.sleep(0.2)
          lines = read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
          temp_string = lines[1][equals_pos+2:]
          temp_c = float(temp_string) / 1000.0
          temp_f = temp_c * 9.0 / 5.0 + 32.0
          return temp_c, temp_f
    
    print('reading temperature')
    try:
        sensor = db.session.get(Sensor, sensor_id)
        print('sensor', sensor)
        _set_task_progress(0)
        data = []
        return read_temp
#     total_temp_rea5ngs = db.session.scalar(sa.select(sa.func.count()).select_from(sensor.temps.select().subquery()))
#        for temp_reading in db.session.scalars(sensor.temps.select().order_by(TempReading.timestamp.asc())):
#            data.append({'temp': temp_reading.temp, 'timestamp': temp_reading.timestamp.isoformat() + 'Z'})
#            time.sleep(5)
#            i += 1
#            _set_task_progress(100 * i // total_temp_readings)
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

