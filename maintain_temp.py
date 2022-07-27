import Adafruit_DHT
import requests
import RPi.GPIO as GPIO
# import time


def set_state(set_pin, new_state):
    if new_state == 'high':
        GPIO.setup(set_pin, GPIO.LOW)
    elif new_state == 'low':
        GPIO.setup(set_pin, GPIO.HIGH)
    else:
        print('unknown state')


ideal = 24
upper_limit = ideal + 0.5
lower_limit = ideal - 0.5
pin = 4
thingspeak_key = 'ENOI1RNJHYXDY80C'
sensor_type = 22
current_state = 0

GPIO.setmode(GPIO.BCM)

# while True:
humidity, temperature = Adafruit_DHT.read_retry(sensor_type, pin)

print('Current temp: ' + str(temperature))

GPIO.setmode(GPIO.BCM)

if upper_limit > temperature < lower_limit:
    set_state(20, 'high')
    print('Heater on')
    current_state = 1

if upper_limit < temperature > lower_limit:
    set_state(20, 'low')
    print('Heater off')
    current_state = 0

r = requests.post('https://api.thingspeak.com/update.json', data={'api_key': thingspeak_key, 'field1': temperature,
                                                                  'field2': humidity, 'field3': current_state})

    # time.sleep(60)
