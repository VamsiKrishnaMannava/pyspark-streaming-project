# Producer: Python script to fetch random user data from an API and send it to Kafka
# It runs in a loop, fetching data every 10 seconds and sending it to the specified
# Kafka topic. The fetched data is printed to the console for verification.
# app/python/api-to-kafka/api-to-kafka.py
# This script doesn't use spark coding

import requests
import time
from kafka import KafkaProducer
import json

# #KAFKA_BROKER = 'kafka-container:9092'
KAFKA_BROKER = 'localhost:9092'
KAFKA_TOPIC = 'randomuser-topic'
API_URL = 'https://randomuser.me/api/'
BATCH_INTERVAL = 10  # seconds

def fetch_random_user():
    response = requests.get(API_URL)
    if response.status_code == 200:
        return response.text
    else:
        return None

def send_to_kafka(producer, topic, message):
    try:
        future = producer.send(topic, value=message.encode('utf-8'))
        result = future.get(timeout=10)
        print(f"Message delivered: {message[:100]}...")
    except Exception as e:
        print(f"Failed to send to Kafka: {e}")


if __name__ == "__main__":
    # Initialize Kafka producer
    producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER)
    print(f"Starting to poll {API_URL} every {BATCH_INTERVAL} seconds and send to Kafka topic '{KAFKA_TOPIC}'...")
    try:
        while True:
            data = fetch_random_user()
            if data:
                send_to_kafka(producer, KAFKA_TOPIC, data) # Print first 100 chars
            else:
                print("Failed to fetch data from API.")
            time.sleep(BATCH_INTERVAL)
    except KeyboardInterrupt:
        print("Stopped by user.")
    finally:
        producer.close()
# End of script
