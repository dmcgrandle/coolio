import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

p = GPIO.PWM(18, 1000)
p.start(0)

time.sleep(4)

try:
    while True:
        p.ChangeDutyCycle(100)
        print('100')
        time.sleep(10)
        p.ChangeDutyCycle(50)
        print('50')
        time.sleep(10)
        p.ChangeDutyCycle(0)
        print('0')
        time.sleep(10)
            
except KeyboardInterrupt:
    pass

p.ChangeDutyCycle(0)
p.stop()
GPIO.cleanup()