from app import scheduler, db
from app.temps.models import Sensor 
import os, glob, sys, time
import sqlalchemy as sa
from rq import get_current_job
from app import create_app, db, scheduler
from app.temps.models import TempTask, Sensor, TempReading

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

print('Initializing scheduled_tasks')

def read_temp_raw(file):
    f = open(file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp(file):
    lines = read_temp_raw(file)
    while lines[0].strip()[-3:] != 'YES':
      time.sleep(0.2)
      lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
      temp_string = lines[1][equals_pos+2:]
      temp_c = float(temp_string) / 1000.0
      temp_f = temp_c * 9.0 / 5.0 + 32.0
      return temp_c, temp_f

@scheduler.task('interval', id='job_sync', seconds=10, max_instances=1, start_date="2000-01-01 12:19:00",)
def interval_temp_reading():
  print('running temp task!')
  with scheduler.app.app_context():
    print('Running temp reading')
    sensors = Sensor.query.all()
    if (sensors.__len__ == 0):
       sensor = Sensor(id='0000006a41e9')
       sensors = [ sensor ]
    for sensor in sensors:
      #temp_dir = '/sys/bus/w1/devices'
      #device_folder = 'temp' # use for testing if there is no sensor attached
      #device_folder = glob.glob(temp_dir + '/28-' + sensor.id) #first temp sensor is 0
      device_file = '/sys/bus/w1/devices/28-' + sensor.id + '/w1_slave'
      print('device_file is', device_file)
      temp_c, temp_f = read_temp(device_file)
      reading = TempReading()
      reading.sensor_id = sensor.id
      reading.temp = temp_f
#      db.session.commit()
