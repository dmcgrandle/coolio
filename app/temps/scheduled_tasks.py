from app import scheduler, db
from app.temps import bp
from app.temps.models import Sensor 
import os, glob, sys, time
import sqlalchemy as sa
from rq import get_current_job
from app import db, scheduler
from app.temps.models import TempTask, Sensor, TempReading

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

print('Initializing scheduled_tasks')

def read_temp(file):
    f = open(file, 'r')
    lines = f.readlines()
    f.close()
    position = lines[1].find('t=')+2
    temperature_f = -460 # absolute zero - indicates an error.  Or the heat death of the universe.
    if position != -1:
      temperature_string = lines[1][position:]
      temperature_c = float(temperature_string) / 1000.0
      temperature_f = temperature_c * 9.0 / 5.0 + 32.0
    return temperature_f

@scheduler.task('interval', id='job_sync', seconds=10, max_instances=1, start_date="2000-01-01 12:19:00",)
def interval_temp_reading():
  with db.app.app_context():
    try:
      sensors = Sensor.query.all()
      if (sensors.__len__ == 0):
        sensor = Sensor(id='0000006a41e9')
        sensors = [ sensor ]
      for sensor in sensors:
        file = '/sys/bus/w1/devices/28-' + sensor.id + '/w1_slave'
        f = open(file, 'r')
        lines = f.readlines()
        f.close()
        position = lines[1].find('t=')+2
        temperature = -460 # absolute zero - indicates an error.  Or the heat death of the universe.
        if position != -1:
          temperature_string = lines[1][position:]
          temperature_c = float(temperature_string) / 1000.0
          temperature = temperature_c * 9.0 / 5.0 + 32.0
        reading = TempReading(sensor_id=sensor.id, temp=temperature)
        db.session.add(reading)
        db.session.commit()
      readings = TempReading.query.all()
      print (readings)
      print (Sensor.query.all())
    except Exception:
      db.app.logger.error('Unhandled exception', exc_info=sys.exc_info())
    finally:
      pass
