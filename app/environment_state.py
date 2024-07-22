import math
from statemachine import StateMachine, State
from statemachine.states import States
from enum import Flag, auto
from flask import current_app
from app import db
import RPi.GPIO as GPIO

class EnvironmentState(Flag):
  """
  The three states of the environment a fan will be cooling:
  - Cool: fan is off, environment is cool
  - Warm: we are between two threshold temperature values 'min' and 'max'.
    In this state the fan speed will be varied up or down with temperature
    changes.
  - Hot: the max temperature has been exceeded.  Need to send an alert and
    turn fan to max.
  - Off: This state machine is not active.
  """
  COOL = auto()
  WARM = auto()
  HOT = auto()
  OFF = auto()

class EnvStateMachine(StateMachine):
  states = States.from_enum(EnvironmentState, initial=EnvironmentState.COOL, final=EnvironmentState.OFF)

  sensor_updated = (
    states.COOL.to(states.WARM, cond='between_min_and_max')
    | states.WARM.to(states.COOL, cond='below_min')
    | states.WARM.to(states.HOT, cond='above_max')
    | states.HOT.to(states.WARM, cond='between_min_and_max')
    | states.WARM.to.itself()
    | states.COOL.to.itself(internal=True)
    | states.HOT.to.itself(internal=True)
  )

  end = (
    states.COOL.to(states.OFF, cond='end_signal_detected')
    | states.WARM.to(states.OFF, cond='end_signal_detected')
    | states.HOT.to(states.OFF, cond='end_signal_detected')
  )

  def __init__(self, auto):
    super().__init__()
    self.auto = auto
    GPIO.setup(self.auto.fan.swtch_pin, GPIO.OUT)

  def change_fan_speed(self, new_speed):
    with db.app.app_context():
      self.auto.fan.speed = new_speed
      current_app.pwm[self.auto.fan.pwm_channel].change_duty_cycle(new_speed)
      db.session.commit()
  
  def turn_fan_on_or_off(self, turn_fan_on: bool):
    with db.app.app_context():
      self.auto.fan.swtch = turn_fan_on
      GPIO.output(self.auto.fan.swtch_pin, turn_fan_on)
      db.session.commit()

  async def between_min_and_max(self, temp: float):
    return temp >= self.auto.temp_min and temp <= self.auto.temp_max

  async def below_min(self, temp: float):
    return temp < self.auto.temp_min

  async def above_max(self, temp: float):
    return temp > self.auto.temp_max
  
  async def end_signal_detected(self, end_signal: bool):
    return end_signal
  
  async def after_transition(self, event: str, source: State, target: State, event_data):
    print(f"Running {event} from {source!s} to {target!s}: {event_data.trigger_data.kwargs!r}")

  async def on_enter_COOL(self):
    current_app.logger.info('Statemachine: Entering cooling state')
    self.change_fan_speed(0)
    current_app.logger.info('Statemachine: Shutting fans off')
    self.turn_fan_on_or_off(False)

  async def on_enter_WARM(self, temp: float):
    print('entering WARM state')
    fan_increment = math.floor(100/(self.auto.temp_max - self.auto.temp_min))
    self.change_fan_speed((temp - self.auto.temp_min)*fan_increment)
    self.turn_fan_on_or_off(True)

  async def on_enter_HOT(self):
    current_app.logger.warning('Statemachine: Entering HOT state - sending alert')
    self.change_fan_speed(100)

  async def on_enter_OFF(self):
    current_app.logger.info('Statemachine: Entering final state - OFF')
    self.turn_fan_on_or_off(False)
    self.change_fan_speed(0)
