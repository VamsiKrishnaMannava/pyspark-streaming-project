
import requests
import json

KAFKA_BROKER = 'kafka-broker:9092'
KAFKA_TOPIC = 'randomuser-topic'
API_IRL = 'https://randomuser.me/api/'
BATCH_INTERVAL = 10  # seconds

def fetch_random_user():
    response  = requests.get(API_IRL)
    return response.text

#print(json.dumps(fetch_random_user()))

print(fetch_random_user())

