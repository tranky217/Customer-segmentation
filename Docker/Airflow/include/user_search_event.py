from pyspark.sql import SparkSession
from pyspark.sql.functions import col, concat, lit

spark = SparkSession.builder \
    .appName("User with search context") \
    .config("spark.jars", "/opt/spark-apps/postgresql-42.2.22.jar") \
    .getOrCreate()

url = "jdbc:postgresql://34.124.159.66:5432/snowplow"

properties = {
    "user": "snowplow",
    "password": "2107",
    "driver": "org.postgresql.Driver"
}

search_table = "atomic.kuzma_search_new_context_1"
user_table = "atomic.kuzma_user_entity_1"
# geo_table = "atomic.com_snowplowanalytics_snowplow_geolocation_context_1"
# yauaa_table = "atomic.nl_basjes_yauaa_context_1"

search_df = spark.read.jdbc(url, search_table, properties=properties)
user_df = spark.read.jdbc(url, user_table, properties=properties)
# geo_df = spark.read.jdbc(url, geo_table, properties=properties)
# yauaa_df = spark.read.jdbc(url, yauaa_table, properties=properties)

# drop columns and do some transformation
search_df = search_df.withColumnRenamed("root_id", "root_id_search")
search_df = search_df.drop("schema_vendor", "schema_name", "schema_format", "schema_version")
user_df = user_df.withColumnRenamed("root_id", "root_id_user")
user_df = user_df.drop("schema_vendor", "schema_name", "schema_format", "schema_version", "root_tstamp")
user_transformed = user_df.withColumn("user_full_name", concat(col("user_name"), lit(" "), col("user_last_name")))

# perform join 
result_df = user_df.join(search_df, search_df["root_id_search"] == user_transformed["root_id_user"], "inner")
# result_df = result_df.drop("")
result_df.show(5, False)

# write the result to local postgresql
result_df.write.format("jdbc")\
        .option("url", "jdbc:postgresql://demo-database:5432/warehouse")\
        .option("driver", "org.postgresql.Driver")\
        .option("dbtable", "search_event_2")\
        .option("user", "postgres")\
        .option("password", "2107")\
        .save()
