from os import write
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType, IntegerType, DoubleType

# Define schema for the JSON data (simplified for demonstration)
user_schema = StructType() \
    .add("gender", StringType()) \
    .add("email", StringType()) \
    .add("phone", StringType()) \
    .add("cell", StringType()) \
    .add("nat", StringType())

# Start Spark session
spark = SparkSession.builder \
    .appName("KafkaToPostgres") \
    .getOrCreate()

# Read from Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka-container:9092") \
    .option("subscribe", "randomuser-topic") \
    .option("startingOffsets", "latest") \
    .load()

# Kafka value is in bytes, convert to string
json_df = df.selectExpr("CAST(value AS STRING) as json_str")

# Parse JSON and extract fields
parsed_df = json_df.select(from_json(col("json_str"), 
    StructType().add("results", 
        StructType().add("gender", StringType())
                    .add("email", StringType())
                    .add("phone", StringType())
                    .add("cell", StringType())
                    .add("nat", StringType())
    )
).alias("data"))

# Flatten the structure (assuming one result per message)
flat_df = parsed_df.select(
    col("data.results.gender").alias("gender"),
    col("data.results.email").alias("email"),
    col("data.results.phone").alias("phone"),
    col("data.results.cell").alias("cell"),
    col("data.results.nat").alias("nat")
)

# write streams to console for debugging
query = flat_df.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

# Uncomment the following lines to write to Postgres

# # Write to Postgres
# query = flat_df.writeStream \
#     .foreachBatch(lambda batch_df, _: batch_df.write \
#         .format("jdbc") \
#         .option("url", "jdbc:postgresql://postgresdb-container:5432/postgres") \
#         .option("dbtable", "users") \
#         .option("user", "docker") \
#         .option("password", "docker") \
#         .option("driver", "org.postgresql.Driver") \
#         .mode("append") \
#         .save()) \
#     .outputMode("append") \
#     .start()

query.awaitTermination()