import Adafruit_DHT
import requests
import RPi.GPIO as GPIO
import time
import datetime
import csv

times = [8, 9, 10, 11]

pin = 4
thingspeak_key = 'ENOI1RNJHYXDY80C'
sensor_type = 22

GPIO.setmode(GPIO.BCM)
GPIO.setup(20, GPIO.IN)

heater_state = 0

while True:
    try:
        hour = datetime.datetime.now().hour

        with open(r'/home/dragon/dragon_project/schedule.csv', mode='r') as inp:
            reader = csv.reader(inp)
            dict_from_csv = {rows[0]: rows[1] for rows in reader}

        temp_variance = 0.5
        # ideal = 25
        ideal = dict_from_csv[str(datetime.datetime.now().hour)]
        upper_limit = float(ideal) + temp_variance
        lower_limit = float(ideal) - temp_variance

        humidity, temperature = Adafruit_DHT.read_retry(sensor_type, pin)
        print('Current Temp: ' + str(temperature))

        if not GPIO.input(20) and (temperature > upper_limit):
            GPIO.setup(20, GPIO.HIGH)
            print('Turning Off')
            heater_state = 0

        elif temperature < lower_limit:
            GPIO.setup(20, GPIO.LOW)
            print('Turning On')
            heater_state = 1

        if hour in times:
            GPIO.setup(21, GPIO.LOW)
            light_state = 1
        else:
            GPIO.setup(21, GPIO.HIGH)
            light_state = 0

        r = requests.post('https://api.thingspeak.com/update.json', data={'api_key': thingspeak_key,
                                                                          'field1': round(temperature, 1),
                                                                          'field2': humidity,
                                                                          'field3': heater_state,
                                                                          'field4': light_state,
                                                                          'field5': ideal
                                                                          })
        time.sleep(60)
    except:
        pass
