import os
import sys
from vcgencmd import Vcgencmd
from flask import current_app
from app import db
# from app.sensors import bp
from app.models import TempReading

# returns zero if all is good, else 256
if os.system('sudo modprobe w1-gpio') or os.system('sudo modprobe w1-therm'):
    sys.exit(
        'No temp sensors detected!\nCoolio requires at least one temp sensor.  Exiting.')

# for testing only
#run = [0, 0, 0]
#temps = [70, 90, 80, 75, 70, 65, 75, 80, 75, 65,
#         75, 65, 75, 65, 75, 65, 75, 65, 75, 65, 75]

# @scheduler.task('interval', id='temp_reading', seconds=10, max_instances=1)

def temp_reading_DS18B20(sm, temp_sensor):
    """Function to be run in BackgroundScheduler - needs app.context() to write Readings"""
    #global run
    with db.app.app_context():
        try:
            # sensors = TempSensor.query.all()
            # if not sensors:
            #  sensor = TempSensor(id='0000006a41e9', name='Desk')
            #  sensors = [ sensor ]
            # for sensor in sensors:
            file = '/sys/bus/w1/devices/28-' + temp_sensor.id + '/w1_slave'
            f = open(file, 'r', encoding="utf-8")
            lines = f.readlines()
            f.close()
            position = lines[1].find('t=')+2
            # absolute zero - indicates an error.  Or the heat death of the universe.
            temperature = -460
            if position != -1:
                temperature_string = lines[1][position:]
                temperature_c = float(temperature_string) / 1000.0
                temperature = temperature_c * 9.0 / 5.0 + 32.0  # convert to fahrenheit
            reading = TempReading(temp_sensor=temp_sensor, temp=temperature)
            db.session.add(reading)
            db.session.commit()
            current_app.logger.info(
                f'Temp Sensor "{temp_sensor.name}" temperature taken {temperature}')
            print(reading)
            sm.send('sensor_updated', temp=temperature)
            # send ficticious temperatures to simulate
            # sm.send('sensor_updated', temp=temps[run[run_i]])
            # print(f'Sent {temps[run[run_i]]} for run #{run[run_i]}')
            # run[run_i] += 1
        except FileNotFoundError as e:
            if e:
                current_app.logger.error(
                    f'Sensor "{temp_sensor.name}" was not found - wrong serial #?', exc_info=sys.exc_info())
            else:
                current_app.logger.error(
                    'Unhandled exception', exc_info=sys.exc_info())
        finally:
            pass
            # auto.sm.send('end', end_signal=True)

def temp_reading_Internal_Pi(sm, temp_sensor):
    """Function to be run in BackgroundScheduler - needs app.context() to write Readings"""
    #global run
    with db.app.app_context():
        try:
            vcgm = Vcgencmd()
            temperature_c = vcgm.measure_temp()
            temperature = temperature_c * 9.0 / 5.0 + 32.0  # convert to fahrenheit
            reading = TempReading(temp_sensor=temp_sensor, temp=temperature)
            db.session.add(reading)
            db.session.commit()
            current_app.logger.info(
                f'Temp Sensor "{temp_sensor.name}" temperature taken {temperature}')
            print(reading)
            sm.send('sensor_updated', temp=temperature)
        except Exception:
            current_app.logger.error(
                'Unhandled exception', exc_info=sys.exc_info())
