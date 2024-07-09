from statemachine import StateMachine, State
from app.sensors.scheduled_tasks import TempReading
from app import db

class Closet(StateMachine):
  off = State(initial=True)
  low = State()
  med = State()
  high = State()
  emergency = State()

  sensor_updated = (
    off.to(low, cond='is_warm')
    | off.to.itself(internal=True)
    | low.to(off, cond='is_cool')
    | low.to.itself(internal=True)
    | low.to(med, cond='is_warmer')
    | med.to(low, cond='is_warm')
    | med.to.itself(internal=True)
    | med.to(high, cond='is_hot')
    | high.to(med, cond='is_warmer')
    | high.to.itself(internal=True)
    | high.to(emergency, cond='is_problem')
    | emergency.to(high, cond='is_hot')
    | emergency.to.itself(internal=True)
  )

  