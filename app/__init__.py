import logging
from logging.handlers import RotatingFileHandler
import os

from flask import Flask, request, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment
from flask_apscheduler import APScheduler
from config import Config
from rpi_hardware_pwm import HardwarePWM
import RPi.GPIO as GPIO

moment = Moment()
db = SQLAlchemy()
migrate = Migrate()
scheduler = APScheduler()

def create_app(config_class=Config):
  print('in create_app')
  app = Flask(__name__)
  app.config.from_object(config_class)
  db.app = app
  db.init_app(app)
  migrate.init_app(app, db)
  moment.init_app(app)
  scheduler.init_app(app)

  #if os.environ.get('WERKZEUG_RUN_MAIN') == "true":
  with app.app_context():
    print('load scheduler')
    from app.sensors import scheduled_tasks
    scheduler.start()

  from app.errors import bp as errors_bp
  app.register_blueprint(errors_bp)

  from app.sensors import bp as sensors_bp
  app.register_blueprint(sensors_bp, url_prefix='/sensors')

  from app.fans import bp as fans_bp
  app.register_blueprint(fans_bp, url_prefix='/fans')

  from app.main import bp as main_bp
  app.register_blueprint(main_bp)

  app.pwm = [HardwarePWM(pwm_channel=0, hz=60, chip=0), HardwarePWM(pwm_channel=1, hz=60, chip=0)]
  app.pwm[0].start(0)

  GPIO.setmode(GPIO.BCM)

#  from app.main.environment_state import EnvStateMachine
#  app.sm = EnvStateMachine()
#  app.sm.activate_initial_state()

  # if not app.debug and not app.testing:
  if not os.path.exists('logs'):
    os.mkdir('logs')
  file_handler = RotatingFileHandler('logs/coolio.log', maxBytes=10240, backupCount=10)
  file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
  file_handler.setLevel(logging.DEBUG)
  app.logger.addHandler(file_handler)

  app.logger.setLevel(logging.INFO)
  app.logger.info('Coolio startup')

  return app

# from app import routes, models
