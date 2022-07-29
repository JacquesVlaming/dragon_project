import Adafruit_DHT
import requests
import RPi.GPIO as GPIO
import time
import datetime
import csv

with open(r'/home/dragon/dragon_project/schedule.csv', mode='r') as inp:
    reader = csv.reader(inp)
    dict_from_csv = {rows[0]: rows[1] for rows in reader}

temp_variance = 0.5
# ideal = 25
ideal = dict_from_csv[str(datetime.datetime.now().hour)]
upper_limit = float(ideal) + temp_variance
lower_limit = float(ideal) - temp_variance

pin = 4
thingspeak_key = 'ENOI1RNJHYXDY80C'
sensor_type = 22

GPIO.setmode(GPIO.BCM)
# GPIO.setwarnings(False)
GPIO.setup(20, GPIO.IN)
# GPIO.setwarnings(False)

while True:
    try:
        humidity, temperature = Adafruit_DHT.read_retry(sensor_type, pin)
        print('Current Temp: ' + str(temperature))
        if not GPIO.input(20) and (temperature > upper_limit):
            GPIO.setup(20, GPIO.HIGH)
            print('Turning Off')
        elif temperature < lower_limit:
            GPIO.setup(20, GPIO.LOW)
            print('Turning On')

        r = requests.post('https://api.thingspeak.com/update.json', data={'api_key': thingspeak_key,
                                                                          'field1': round(temperature, 1),
                                                                          'field2': humidity,
                                                                          'field3': not GPIO.input(20)})
        time.sleep(60)
    except:
        pass
