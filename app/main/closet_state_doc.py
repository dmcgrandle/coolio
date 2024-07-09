"""
State Machine for overall Closet state controlling cooling with Array Fans

conditions:
is_cool: temp < closet_threshold_1 
is_warm: closet_threshold_1 <= temp < closet_threshold_2
is_warmer: closet_threshold_2 <= temp < closet_threshold_3
is_hot: closet_threshold_3 <= temp < closet_threshold_4
is_problem: temp > closet_threshold_4

State: OFF
Initial state
Log time and temp entering state
Turn array fans off and re-read closet_temp_sensor every 10 mins
- if is_warm go to LOW
- if is_cool go to self

State: LOW
Log time and temp entering state
Ensure array fans are on and set to low.
Check temp again in 5 mins.
- if is_warmer go to MED
- if is_warm go to self
- if is_cool go to OFF

State: MED
Log time and temp entering state
Ensure array fans are on and set to med.
Check temp again in 5 mins.
- if is_hot go to HIGH
- if is_warmer go to self
- if is_warm go to LOW

State: HIGH
Log time and temp entering state
Ensure array fans are on and set to high.
Check temp again in 5 mins.
- if is_problem go to EMERGENCY
- if is_hot go to self
- if is_warmer go to MED

State: EMERGENCY
Log time and temp entering state
Ensure array fans are on and set to high.
Send text alert to emergency phone number to get help
Check temp again in 5 mins.
- if is_problem go to self
- if is_hot go to HIGH

"""