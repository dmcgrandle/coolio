import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db, create_app
from app.models import Sensor, TempSensor, Reading, TempReading, Automation, Fan, SpeedChange

app = create_app()

@app.shell_context_processor
def make_shell_context():
  return {'sa': sa, 'so': so, 'db': db, 'Fan': Fan, 'Speed': SpeedChange, 'Sensor': Sensor, 
          'TempSensor': TempSensor, 'Reading': Reading, 'TempReading': TempReading, 'Automation': Automation}

#if __name__ == "__main__":
#  app.run(host='0.0.0.0', debug=True, use_reloader=False)