import RPi.GPIO as GPIO
import datetime
import time

times = [16, 17]

GPIO.setmode(GPIO.BCM)


def set_state(set_pin, new_state):
    if new_state == 'high':
        GPIO.setup(set_pin, GPIO.LOW)
    elif new_state == 'low':
        GPIO.setup(set_pin, GPIO.HIGH)
    else:
        print('unknown state')


while True:
    hour = datetime.datetime.now().hour

    if hour in times:
        set_state(21, 'high')
    else:
        set_state(21, 'low')

    time.sleep(60)