PySpark Kafka Streaming Pipeline and Chatbot to answer the enduser prompts
==========================================================================

This project demonstrates a real-time data pipeline that ingests user data from the Random User API, streams it through Kafka, processes it using PySpark Structured Streaming, and stores the results in a PostgreSQL database. A chatbot interface can then query the database to answer user questions.

📷 Architecture Diagram
-----------------------

Refer to the attached image for a visual representation of the pipeline.
![alt text](<Architecture diagram.png>)

🧱 Architecture Overview
------------------------

**Pipeline Flow:**
1.  **Random User API** →
2.  **Kafka (randomuser-topic)** →
3.  **PySpark Structured Streaming** →
4.  **PostgreSQL** →
5.  **Chatbot Query Interface**
    

🐳 Docker Setup
---------------
### Docker Compose Services

*   **Postgres**: Stores processed user data.
*   **Zookeeper**: Required for Kafka coordination.
*   **Kafka**: Event streaming platform.
*   **Spark Master & Worker**: PySpark cluster for streaming and transformation.
    
### Cassandra (Optional)

*   Commented out in [docker-compose.yml](https://docker-compose.yml) for future expansion.
    
### Network

*   All services are connected via a custom bridge network app-network.
    
🐍 Dockerfile for Spark
-----------------------

Installs Python and kafka-python for producer/consumer scripts.

`   FROM apache/spark:latest  USER root  RUN apt-get update && apt-get install -y python3-pip \      && pip3 install kafka-python  USER spark   `

🔧 Kafka Commands
------------------

### Create Topic

` docker exec -it kafka-container bash  kafka-topics --create --topic test-topic --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1   `

🐍 Python Scripts and commands
-------------------------------

🔧 Kafka Producer Command for execution
----------------------------------------
`/home/epm/mywork/pyspark-streaming-project/pyspark-streaming-project/venv/bin/python /home/epm/mywork/pyspark-streaming-project/pyspark-streaming-project/app/python/api-to-kafka/producer.py`

⚡ Spark Submit Command for execution
--------------------------------------

Fetches necessary jars from Maven Central at runtime:

`docker exec spark-master /opt/spark/bin/spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.13:4.0.1,org.apache.spark:spark-token-provider-kafka-0-10_2.13:4.0.1,org.postgresql:postgresql:42.7.3 --conf spark.jars.ivy=/tmp/.ivy2 /app/python/kafka-to-postgres/consumer.py`

🧪 Example Chatbot Query
------------------------

`   How many users are from France?   `

This query is answered by fetching data from the PostgreSQL database populated by the Spark consumer.

📁 Volumes
----------

*   ./sql: SQL scripts for initializing PostgreSQL.
*   ./app: Python application code for Spark and Kafka integration.
    

📌 Notes
--------

*   Ensure all services are up using docker-compose up --build.
*   Kafka listeners are configured for both host and container access.
*   Spark jars are dynamically resolved via Maven.

🧠 Future Enhancements
----------------------

*   Enable Cassandra for scalable NoSQL storage.
*   Add monitoring tools (e.g., Prometheus, Grafana).
*   Extend chatbot capabilities with NLP.
    

🛠 Requirements
---------------

*   Docker Desktop
*   WSL2 (for Windows users)
*   Python 3.8+
*   VS Code

### Final Sample Result: 
<img width="1458" height="330" alt="image" src="https://github.com/user-attachments/assets/dd5175a9-2378-4e13-ad2a-e128a4c35997" />

🔧 Kafka Commands to test the connectivity
-------------------------------------------
### Produce Message (For Testing)
`   echo "new_test_message" | kafka-console-producer --bootstrap-server localhost:9092 --topic test-topic   `

### Consume Message (For Testing)
`   kafka-console-consumer --bootstrap-server localhost:9092 --topic test-topic --from-beginning   `

### Kafka Consumer (Console (For Testing))
`   docker exec -it kafka-container bash  kafka-console-consumer --bootstrap-server localhost:9092 --topic randomuser-topic --from-beginning   `

👨‍💻 Author
------------

**Vamsi Krishna Mannava** — Data Engineering Enthusiast & Integration Optimizer

🐧 Linux Setup Note
-------------------

For Linux users working on Windows, this project can be set up using WSL's Ubuntu with a Python virtual environment (venv) configured for isolation. Docker Desktop is recommended for managing containers seamlessly within this environment, providing a smooth development experience that combines Linux tooling with Windows convenience.
