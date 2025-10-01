import os
from dotenv import load_dotenv
# from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
# from apscheduler.executors.pool import ThreadPoolExecutor

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'my-not-so-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    INTERVAL_TASK_ID = os.environ.get('INTERVAL_TASK_ID') or 'interval-task-id'

    SCHEDULER_API_ENABLED = os.environ.get('SCHEDULER_API_ENABLED') or True

    # Riverbed specific API and Webhook secrets
    RVBD_ACCESS_TOKEN_URI =  os.environ.get('RVBD_ACCESS_TOKEN_URI')
    RVBD_API_SCOPE =  os.environ.get('RVBD_API_SCOPE')
    RVBD_BASE_URI =  os.environ.get('RVBD_BASE_URI')
    RVBD_TENANT_ID =  os.environ.get('RVBD_TENANT_ID')
    RVBD_CLIENT_ID =  os.environ.get('RVBD_CLIENT_ID')
    RVBD_CLIENT_CRED =  os.environ.get('RVBD_CLIENT_CRED')
    RVBD_WEBHOOK_URL =  os.environ.get('RVBD_WEBHOOK_URL')

#    SCHEDULER_JOBSTORES = {
#        'default': SQLAlchemyJobStore(url='sqlite:///flask_context.db') # will persist jobs across reboots
#    }
#    SCHEDULER_EXECUTORS = {
#        'default': ThreadPoolExecutor(1)
#        }
