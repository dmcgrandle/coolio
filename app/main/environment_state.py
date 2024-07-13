from statemachine import StateMachine, State
from statemachine.states import States
from enum import Flag, auto

class EnvironmentState(Flag):
  """
  The three states of the environment a fan will be cooling:
  - Cool: fan is off, environment is cool
  - Warm: we are between two threshold temperature values 'min' and 'max'.
    In this state the fan speed will be varied up or down with temperature
    changes.
  - Hot: the max temperature has been exceeded.  Need to send an alert and
    turn fan to max.
  """
  COOL = auto()
  WARM = auto()
  HOT = auto()

class EnvStateMachine(StateMachine):
  states = States.from_enum(EnvironmentState, initial=EnvironmentState.COOL)

  sensor_updated = (
    states.COOL.to(states.WARM, cond='between_min_and_max')
    | states.WARM.to(states.COOL, cond='below_min')
    | states.WARM.to(states.HOT, cond='above_max')
    | states.HOT.to(states.WARM, cond='between_min_and_max')
    | states.WARM.to.itself()
    | states.COOL.to.itself(internal=True)
    | states.HOT.to.itself(internal=True)
  )

  def __init__(self):
    self.thresholds = {'min': 70, 'max': 90}
    self.fan_speed = 0
    self.fan_is_on = False
    self.fan_increment = round(100/(self.thresholds['max'] - self.thresholds['min']))
    super().__init__()

  async def between_min_and_max(self, temp: int):
    return temp >= self.thresholds['min'] and temp <= self.thresholds['max']

  async def below_min(self, temp: int):
    return temp < self.thresholds['min']

  async def above_max(self, temp: int):
    return temp > self.thresholds['max']
  
  async def after_transition(self, event: str, source: State, target: State, event_data):
    print(f"Running {event} from {source!s} to {target!s}: {event_data.trigger_data.kwargs!r}")

  async def on_enter_COOL(self):
    print('entering COOL state')
    self.fan_speed = 0
    print('shutting fan(s) off')
    self.fan_is_on = False

  async def on_enter_WARM(self, temp: int):
    print('entering WARM state')
    self.fan_speed = (temp - self.thresholds['min'])*self.fan_increment
    self.fan_is_on = True

  async def on_enter_HOT(self):
    print('entering HOT state')
    print('Set fan at max')
    self.fan_speed = 100
    print('Send text alert!')
