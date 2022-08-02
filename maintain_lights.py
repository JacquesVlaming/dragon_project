import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

def set_state(set_pin, new_state):
    if new_state == 'high':
        GPIO.setup(set_pin, GPIO.LOW)
    elif new_state == 'low':
        GPIO.setup(set_pin, GPIO.HIGH)
    else:
        print('unknown state')

set_state(21, 'high')