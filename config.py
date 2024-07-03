import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'my-not-so-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://'
    INTERVAL_TASK_ID = os.environ.get('INTERVAL_TASK_ID') or 'interval-task-id'

    SCHEDULER_API_ENABLED = os.environ.get('SCHEDULER_API_ENABLED') or True