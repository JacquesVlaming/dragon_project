import RPi.GPIO as GPIO
import datetime
import time
import requests

thingspeak_key = 'ENOI1RNJHYXDY80C'

uvb_times = [6, 7, 8, 9, 10, 11, 12, 13, 15, 16, 17, 18]

GPIO.setmode(GPIO.BCM)

light_state = 0
uvb_light_state = 0


def set_state(set_pin, new_state):
    if new_state == 'high':
        GPIO.setup(set_pin, GPIO.LOW)
    elif new_state == 'low':
        GPIO.setup(set_pin, GPIO.HIGH)
    else:
        print('unknown state')


while True:
    hour = datetime.datetime.now().hour

    if hour in uvb_times:
        set_state(21, 'high')
        light_state = 1

    else:
        set_state(21, 'low')
        light_state = 0

    print(light_state)

    r = requests.post('https://api.thingspeak.com/update.json', data={'api_key': thingspeak_key,
                                                                      'field6': light_state})
    time.sleep(60)
