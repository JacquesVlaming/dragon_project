import requests
import time
from elasticsearch import Elasticsearch
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

import datetime
print(datetime.datetime.now())

es = Elasticsearch(
    cloud_id=config['ELASTIC']['cloud_id'],
    verify_certs=False,
    ssl_show_warn=False,
    basic_auth=(config['ELASTIC']['user'], config['ELASTIC']['password'])
)

dragon_mapping = {
    "mappings": {
        "properties": {
            "timestamp": {"type": "date"},
            "temperature": {"type": "double"},
            "humidity": {"type": "double"},
            "heater_state": {"type": "text"},
            "light_state": {"type": "text"},
            "ideal_temp": {"type": "double"}
        }
    }
}

es.indices.create(index='dragons_den', body=dragon_mapping)


while True:
    response = requests.get('http://api.open-notify.org/iss-now.json')
    raw = response.json()
    formatted = {'iss_position': {'lat': raw['iss_position']['latitude'],
                                  'lon': raw['iss_position']['longitude']
                                  },
                 # 'timestamp': datetime.datetime.now(),
                 'timestamp': datetime.datetime.fromtimestamp(raw['timestamp']),
                 'message': raw['message']
                 }
    print(formatted)
    es.index(index='iss_position', document=formatted)
    time.sleep(1)

# es.indices.delete(index='iss_position', ignore=[400, 404])
