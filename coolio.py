import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db, create_app
from app.temps.models import Sensor, TempReading, TempTask
from app.fans.models import Fan, SpeedChange

app = create_app()

@app.shell_context_processor
def make_shell_context():
  return {'sa': sa, 'so': so, 'db': db, 'Fan': Fan, 'Speed': SpeedChange, 'Sensor': Sensor, 'Temp': TempReading, 'TempTask': TempTask}

#if __name__ == "__main__":
#  app.run(host='0.0.0.0', debug=True, use_reloader=False)