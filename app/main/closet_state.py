from statemachine import StateMachine, State
from statemachine.states import States
#from app import db
from enum import Flag, auto

class ClosetState(Flag):
  OFF = auto()
  LOW = auto()
  HIGH = auto()
  EMERGENCY = auto()

class ClosetMachine(StateMachine):
  states = States.from_enum(ClosetState, initial=ClosetState.OFF)
  thresholds = {'warm': 75, 'hot': 85, 'problem': 90}

  sensor_updated = (
    states.OFF.to(states.LOW, cond='is_warm')
    | states.OFF.to(states.HIGH, cond='is_hot')
    | states.OFF.to(states.EMERGENCY, cond='is_problem')
    | states.LOW.to(states.OFF, cond='is_cool')
    | states.LOW.to(states.HIGH, cond='is_hot')
    | states.LOW.to(states.EMERGENCY, cond='is_problem')
    | states.HIGH.to(states.OFF, cond='is_cool')
    | states.HIGH.to(states.LOW, cond='is_warm')
    | states.HIGH.to(states.EMERGENCY, cond='is_problem')
    | states.EMERGENCY.to(states.OFF, cond='is_cool')
    | states.EMERGENCY.to(states.LOW, cond='is_warm')
    | states.EMERGENCY.to(states.HIGH, cond='is_hot')
    | states.OFF.to.itself(internal=True)
    | states.LOW.to.itself(internal=True)
    | states.HIGH.to.itself(internal=True)
    | states.EMERGENCY.to.itself(internal=True)
  )

  async def is_cool(self, temp: int):
    return temp < self.thresholds['warm']

  async def is_warm(self, temp: int):
    cond = temp >= self.thresholds['warm'] and temp < self.thresholds['hot']
    print(f'evaluating is warm: {cond}')
    return temp >= self.thresholds['warm'] and temp < self.thresholds['hot']

  async def is_hot(self, temp: int):
    return temp >= self.thresholds['hot'] and temp < self.thresholds['problem']

  async def is_problem(self, temp: int):
    return temp >= self.thresholds['problem']
  
  async def after_transition(self, event: str, source: State, target: State, event_data):
        print(f"Running {event} from {source!s} to {target!s}: {event_data.trigger_data.kwargs!r}")

  async def on_enter_OFF(self):
     print('entering Off state')

  async def on_enter_LOW(self):
     print('entering Low state')

  async def on_enter_HIGH(self):
     print('entering High state')

  async def on_enter_EMERGENCY(self):
     print('entering Emergency state')
