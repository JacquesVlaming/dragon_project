import Adafruit_DHT
import requests
import RPi.GPIO as GPIO
import time
import datetime
import csv


# with open(r'schedule.csv', mode='r') as inp:
#     reader = csv.reader(inp)
#     dict_from_csv = {rows[0]: rows[1] for rows in reader}


def get_state(pin_state):
    # GPIO.setup(20, GPIO.IN)
    if GPIO.input(pin_state):
        return 0
    else:
        return 1


def set_state(set_pin, new_state):
    if new_state == 'high':
        GPIO.setup(set_pin, GPIO.LOW)
    elif new_state == 'low':
        GPIO.setup(set_pin, GPIO.HIGH)
    else:
        print('unknown state')


temp_variance = 0.5
ideal = 21.5
# ideal = dict_from_csv[str(datetime.datetime.now().hour)]
upper_limit = float(ideal) + temp_variance
lower_limit = float(ideal) - temp_variance

pin = 4
thingspeak_key = 'ENOI1RNJHYXDY80C'
sensor_type = 22
GPIO.setmode(GPIO.BCM)
GPIO.setup(20, GPIO.IN)
current_state = get_state(20)

# while True:
humidity, temperature = Adafruit_DHT.read_retry(sensor_type, pin)

print('Current temp: ' + str(temperature))

if temperature < upper_limit:
    print('Heater on')
    instruction = 'high'
else:
    print('Heater off')
    instruction = 'low'
if temperature > lower_limit or temperature > upper_limit:
    print('Heater off')
    instruction = 'low'
else:
    instruction = 'high'
    print('Heater on')

set_state(20, instruction)
current_state = get_state(20)

r = requests.post('https://api.thingspeak.com/update.json', data={'api_key': thingspeak_key, 'field1': round(temperature, 1),
                                                              'field2': humidity, 'field3': current_state})

    # time.sleep(60)
