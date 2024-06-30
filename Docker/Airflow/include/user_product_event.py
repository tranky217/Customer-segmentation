from pyspark.sql import SparkSession
from pyspark.sql.functions import year, month, dayofweek, dayofmonth, hour, date_format
from pyspark.sql.functions import col, concat, lit
from pyspark.sql import functions as F
from pyspark.sql.types import DateType
# import ru.yandex.clickhouse._

spark = SparkSession.builder \
    .appName("PostgreSQL GCP Connection with PySpark") \
    .config("spark.jars", "/opt/spark-apps/postgresql-42.2.22.jar") \
    .getOrCreate()

url = "jdbc:postgresql://34.124.159.66:5432/snowplow"

properties = {
    "user": "snowplow",
    "password": "2107",
    "driver": "org.postgresql.Driver"
}

user_table = "atomic.kuzma_user_entity_1"
product_table = "atomic.kuzma_product_entity_1"
event_table = "atomic.kuzma_product_event_1"
enrich_table ="atomic.nl_basjes_yauaa_context_1"
geolocation_table = "atomic.com_snowplowanalytics_snowplow_geolocation_context_1"


user_df = spark.read.jdbc(url, user_table, properties=properties)
product_df = spark.read.jdbc(url, product_table, properties=properties)
event_df = spark.read.jdbc(url, event_table, properties=properties)
enrich_df = spark.read.jdbc(url, enrich_table, properties=properties)
geo_df = spark.read.jdbc(url, geolocation_table, properties=properties)

# transform enrich
# operating_system_name
# device_name
# agent_name
# root_id

geo_df = geo_df.select("root_id", "latitude", "longitude")
geo_transformed = geo_df.withColumnRenamed("root_id", "root_id_geo")

enrich_transformed = enrich_df.select("root_id", "device_name", "agent_name", "operating_system_name")
enrich_transformed = enrich_transformed.withColumnRenamed("root_id", "root_id_enrich")

# transform for event 
transformed_event = event_df.select("root_id", "root_tstamp", "action", "target")
transformed_event = (transformed_event
                    .withColumn("interaction_date", F.to_date(date_format(col("root_tstamp").cast("timestamp"), "yyyy-MM-dd")))
                    .withColumn("year", year(col="root_tstamp"))
                    .withColumn("month", month(col="root_tstamp"))
                    .withColumn("day_in_month", dayofmonth(col="root_tstamp"))
                    .withColumn("day_of_week", dayofweek(col="root_tstamp"))
                    .withColumn("hour_of_day", hour(col="root_tstamp") + 7))
# transformed_event.show(5, False)
transformed_event = transformed_event.withColumnRenamed("root_id", "root_id_event")

# transform for product
product_transformed = product_df.select("root_id", "product_id", "brand_name", "category", "gender", "price", "product_name", "production_date", "rating", "size", "total_reviews")
product_transformed = product_transformed.withColumnRenamed("root_id", "root_id_product")
product_transformed = product_transformed.withColumn("production_date", product_transformed["production_date"].cast(DateType()))

# transform of user
user_transformed = user_df.withColumn("user_full_name", concat(col("user_name"), lit(" "), col("user_last_name")))
user_transformed = user_transformed.withColumnRenamed("root_id", "root_id_user")
user_transformed = user_transformed.select("root_id_user", "user_id", "address", "email", "phone", "user_full_name")

# perform join
result_df = user_transformed.join(product_transformed, product_transformed["root_id_product"] == user_transformed["root_id_user"], "inner")
result_df = result_df.join(transformed_event, transformed_event["root_id_event"] == result_df["root_id_user"], "inner")
result_df = result_df.join(enrich_transformed, enrich_transformed["root_id_enrich"] == result_df["root_id_user"], "inner")
result_df = result_df.join(geo_transformed, geo_transformed["root_id_geo"] == result_df["root_id_user"], "inner")

result_df = result_df.drop("root_id_enrich", "root_id_user", "root_id_product", "root_id_geo")
result_df.show(5, False)

result_df.printSchema()
# write to local postgresql
result_df.write.format("jdbc")\
        .option("url", "jdbc:postgresql://demo-database:5432/warehouse")\
        .option("driver", "org.postgresql.Driver")\
        .option("dbtable", "product_event_2")\
        .option("user", "postgres")\
        .option("password", "2107")\
        .save()
