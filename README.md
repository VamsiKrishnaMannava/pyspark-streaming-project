


* `2.3-streaming# Spark Streaming Project: Spark, Kafka, and Python Integration

## How to Run

### 1. Start Docker Compose

Start all services (Postgres, Kafka, Spark, etc.):

```bash
docker compose up -d
```

---

### 2. Run the Kafka Producer Script in Spark Container

Open a new terminal and execute:

```bash
docker exec -it spark-container bash
cd /app/python/api-to-kafka
python api-to-kafka.py
```

This script fetches data from the API and sends it to the Kafka topic `randomuser-topic`.

---

### 3. Consume Kafka Messages from the Console

To view messages in the `randomuser-topic` topic, run:

```bash
docker exec -it kafka-container kafka-console-consumer.sh --bootstrap-server kafka-container:9092 --topic randomuser-topic --from-beginning
```

This will print all messages sent to the topic.

---

### For questions or suggestions

If you have changes to suggest to this repo, either
- submit a GitHub issue
- tell me in the course Q/A forum
- submit a pull request!

## Running Spark and Kafka Integration

### 1. Start Docker Compose

Start all services (Postgres, Kafka, Spark, etc.):

```bash
docker compose up -d
```

---

### 2. Run the Kafka Producer Script in Spark Container

Open a new terminal and execute:

```bash
docker exec -it spark-container bash
cd /app/python/api-to-kafka
python api-to-kafka.py
```

This script fetches data from the API and sends it to the Kafka topic `randomuser-topic`.

---

### 3. Consume Kafka Messages from the Console

To view messages in the `randomuser-topic` topic, run:

```bash
docker exec -it kafka-container kafka-console-consumer.sh --bootstrap-server kafka-container:9092 --topic randomuser-topic --from-beginning
```

This will print all messages sent to the topic.

---


