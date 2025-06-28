from pyspark.sql import SparkSession
from pyspark.sql.functions import lit
import requests
import time
from kafka import KafkaProducer
import json


KAFKA_BROKER = 'kafka-container:9092'
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
    producer.send(topic, value=message.encode('utf-8'))

if __name__ == "__main__":
    # Initialize Kafka producer
    producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER)

    # Spark session (not strictly needed for this polling loop, but included for completeness)
    spark = SparkSession.builder \
        .appName("APIToKafka") \
        .getOrCreate()

    print(f"Starting to poll {API_URL} every {BATCH_INTERVAL} seconds and send to Kafka topic '{KAFKA_TOPIC}'...")

    try:
        while True:
            data = fetch_random_user()
            if data:
                send_to_kafka(producer, KAFKA_TOPIC, data)
                print(f"Sent data to Kafka: {data[:100]}...")  # Print first 100 chars
            else:
                print("Failed to fetch data from API.")
            time.sleep(BATCH_INTERVAL)
    except KeyboardInterrupt:
        print("Stopped by user.")
    finally:
        producer.close()
        spark.stop()