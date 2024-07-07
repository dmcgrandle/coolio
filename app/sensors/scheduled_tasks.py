from app import scheduler, db
# from app.sensors import bp
import os, glob, sys, time
from app.sensors.models import TempSensor, TempReading

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

print('Initializing scheduled_tasks')

@scheduler.task('interval', id='temp_reading', seconds=5000, max_instances=1)
def interval_temp_reading():
  with db.app.app_context():
    try:
      sensors = TempSensor.query.all()
      if not sensors:
        sensor = TempSensor(id='0000006a41e9')
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
        reading = TempReading(sensor=sensor, temp=temperature)
        db.session.add(reading)
        db.session.commit()
      readings = TempReading.query.all()
      print (readings)
      print (TempSensor.query.all())
    except Exception:
      db.app.logger.error('Unhandled exception', exc_info=sys.exc_info())
    finally:
      pass
