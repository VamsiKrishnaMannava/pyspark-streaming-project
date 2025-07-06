import json
import time
import requests
from pyspark.sql import SparkSession
from pyspark.sql.functions import lit
from pyspark.sql.types import StringType

from threading import Thread
from queue import Queue

# 🔧 Configs
KAFKA_BROKER = 'kafka-broker:9092'
KAFKA_TOPIC = 'randomuser-topic'
API_URL = 'https://randomuser.me/api/'
BATCH_INTERVAL = 10  # seconds

# Shared queue for streaming data
data_queue = Queue()

# 📡 Thread to pull data from API
def fetch_data():
    while True:
        try:
            response = requests.get(API_URL)
            if response.status_code == 200:
                payload = json.dumps(response.json())
                data_queue.put(payload)
        except Exception as e:
            print(f"Error fetching API: {e}")
        time.sleep(BATCH_INTERVAL)

# 🚀 Start the fetch thread
Thread(target=fetch_data, daemon=True).start()

# ⚙️ Define schema-less DataFrame for input
def generate_data():
    while True:
        rows = []
        while not data_queue.empty():
            raw = data_queue.get()
            rows.append((raw,))
        if rows:
            yield rows
        time.sleep(BATCH_INTERVAL)

# 🚂 Create Spark session
spark = SparkSession.builder \
    .appName("API to Kafka Streaming") \
    .getOrCreate()
spark.sparkContext.setLogLevel("WARN")

# 💾 Create streaming DataFrame using memory source
def run_stream():
    for batch_data in generate_data():
        if not batch_data:
            continue
        df = spark.createDataFrame(batch_data, ["value"]).withColumn("topic", lit(KAFKA_TOPIC))
        df.selectExpr("CAST(value AS STRING)", "CAST(topic AS STRING)") \
            .write \
            .format("kafka") \
            .option("kafka.bootstrap.servers", KAFKA_BROKER) \
            .option("topic", KAFKA_TOPIC) \
            .save()
        print(f"🚚 Published batch with {len(batch_data)} records.")

# 🏁 Start the loop
run_stream()
