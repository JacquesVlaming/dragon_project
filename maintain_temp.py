import Adafruit_DHT
import requests
import RPi.GPIO as GPIO
# import time


def relay_state(raw_state):
    if raw_state == 0:
        return 1
    else:
        return 0


def set_state(set_pin, new_state):
    if new_state == 'high':
        GPIO.setup(set_pin, GPIO.LOW)
    elif new_state == 'low':
        GPIO.setup(set_pin, GPIO.HIGH)
    else:
        print('unknown state')


upper_limit = 25

lower_limit = 24

GPIO.setmode(GPIO.BCM)

pin = 4

thingspeak_key = 'ENOI1RNJHYXDY80C'

sensor_type = 22

humidity, temperature = Adafruit_DHT.read_retry(sensor_type, pin)

# print('Current temp: ' + str(temperature))

GPIO.setmode(GPIO.BCM)

# current_state = 0

if temperature < lower_limit:
    set_state(20, 'high')
    # print('Heater on')
    current_state = 1

if upper_limit > temperature > lower_limit:
    set_state(20, 'low')
    # print('Heater off')
    current_state = 0

r = requests.post('https://api.thingspeak.com/update.json', data={'api_key': thingspeak_key, 'field1': temperature,
                                                                  'field2': humidity, 'field3': current_state})

time.sleep(60)
