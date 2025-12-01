from os import write
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, explode
from pyspark.sql.types import *

randomuser_schema = StructType([
    StructField("results", ArrayType(
        StructType([
            StructField("gender", StringType()),
            StructField("name", StructType([
                StructField("title", StringType()),
                StructField("first", StringType()),
                StructField("last", StringType())
            ])),
            StructField("location", StructType([
                StructField("street", StructType([
                    StructField("number", IntegerType()),
                    StructField("name", StringType())
                ])),
                StructField("city", StringType()),
                StructField("state", StringType()),
                StructField("country", StringType()),
                StructField("postcode", StringType()),  # can be int or string, safer as string
                StructField("coordinates", StructType([
                    StructField("latitude", StringType()),
                    StructField("longitude", StringType())
                ])),
                StructField("timezone", StructType([
                    StructField("offset", StringType()),
                    StructField("description", StringType())
                ]))
            ])),
            StructField("email", StringType()),
            StructField("login", StructType([
                StructField("uuid", StringType()),
                StructField("username", StringType()),
                StructField("password", StringType()),
                StructField("salt", StringType()),
                StructField("md5", StringType()),
                StructField("sha1", StringType()),
                StructField("sha256", StringType())
            ])),
            StructField("dob", StructType([
                StructField("date", StringType()),  # ISO timestamp
                StructField("age", IntegerType())
            ])),
            StructField("registered", StructType([
                StructField("date", StringType()),
                StructField("age", IntegerType())
            ])),
            StructField("phone", StringType()),
            StructField("cell", StringType()),
            StructField("id", StructType([
                StructField("name", StringType()),
                StructField("value", StringType())
            ])),
            StructField("picture", StructType([
                StructField("large", StringType()),
                StructField("medium", StringType()),
                StructField("thumbnail", StringType())
            ])),
            StructField("nat", StringType())
        ])
    )),
    StructField("info", StructType([
        StructField("seed", StringType()),
        StructField("results", IntegerType()),
        StructField("page", IntegerType()),
        StructField("version", StringType())
    ]))
])


# Start Spark session
spark = SparkSession.builder \
    .appName("KafkaToPostgres") \
    .getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

# Read from Kafka #.option("kafka.bootstrap.servers", "kafka-container:9092") \
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka-container:29092") \
    .option("subscribe", "randomuser-topic") \
    .option("startingOffsets", "latest") \
    .load()


# Kafka value is in bytes, convert to string
json_df = df.selectExpr("CAST(value AS STRING) as json_str")

parsed_df = json_df.withColumn("json_data", from_json(col("json_str"), randomuser_schema))

# Expand into columns
final_df = parsed_df.select("json_data.*")

users_df = final_df.select(explode(col("results")).alias("user"))

# Flatten nested fields into columns
flat_df = users_df.select(
    col("user.gender").alias("gender"),
    col("user.name.title").alias("title"),
    col("user.name.first").alias("first_name"),
    col("user.name.last").alias("last_name"),
    col("user.location.street.number").alias("street_number"),
    col("user.location.street.name").alias("street_name"),
    col("user.location.city").alias("city"),
    col("user.location.state").alias("state"),
    col("user.location.country").alias("country"),
    col("user.location.postcode").alias("postcode"),
    col("user.location.coordinates.latitude").alias("latitude"),
    col("user.location.coordinates.longitude").alias("longitude"),
    col("user.location.timezone.offset").alias("tz_offset"),
    col("user.location.timezone.description").alias("tz_description"),
    col("user.email").alias("email"),
    col("user.login.uuid").alias("login_uuid"),
    col("user.login.username").alias("username"),
    col("user.login.password").alias("password"),
    col("user.dob.date").alias("dob_date"),
    col("user.dob.age").alias("dob_age"),
    col("user.registered.date").alias("registered_date"),
    col("user.registered.age").alias("registered_age"),
    col("user.phone").alias("phone"),
    col("user.cell").alias("cell"),
    col("user.id.name").alias("id_name"),
    col("user.id.value").alias("id_value"),
    col("user.picture.large").alias("picture_large"),
    col("user.picture.medium").alias("picture_medium"),
    col("user.picture.thumbnail").alias("picture_thumbnail"),
    col("user.nat").alias("nationality")
)


# write streams to console for debugging
query = flat_df.writeStream \
    .outputMode("append") \
    .format("console") \
    .option("truncate", "false") \
    .trigger(processingTime="10 seconds") \
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