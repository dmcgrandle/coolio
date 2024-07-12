from app import scheduler, db
# from app.sensors import bp
import os, glob, sys, time
from app.sensors.models import TempSensor, TempReading
from app import sm

if os.system('sudo modprobe w1-gpio') or os.system('sudo modprobe w1-therm'): # returns zero if all is good, else 256
  sys.exit('No temp sensors detected!\nCoolio requires at least one temp sensor.  Exiting.')

run = 0

temps = [ 69, 70, 71, 72, 75, 75, 85, 90, 95, 90, 85, 75, 70, 65, 60, 70, 80, 90 ]

@scheduler.task('interval', id='temp_reading', seconds=10, max_instances=1)
def interval_temp_reading():
  global run
  with db.app.app_context():
    try:
      sensors = TempSensor.query.all()
      if not sensors:
        sensor = TempSensor(id='0000006a41e9', name='Desk')
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
      print (reading)
      # send ficticious temperatures to simulate
      sm.send('sensor_updated', temp=temps[run])
      print(f'Sent {temps[run]} for run #{run}')
      run += 1
    except Exception as e:
      if e.errno == 2:
        db.app.logger.error(f'Sensor "{sensor.name}" was not found - wrong serial #?', exc_info=sys.exc_info())
      else:
        db.app.logger.error('Unhandled exception', exc_info=sys.exc_info())
    finally:
      pass
