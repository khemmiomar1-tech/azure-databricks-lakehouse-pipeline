# Databricks notebook source
# MAGIC %md
# MAGIC # 02 - Silver: clean the Bronze API records
# MAGIC Deduplication on the business key, null handling, standardised types.

# COMMAND ----------

from pyspark.sql import functions as F
from pyspark.sql.window import Window

BRONZE_TABLE = "/Volumes/lakehouse/bronze/delta/api_records"
SILVER_TABLE = "/Volumes/lakehouse/silver/delta/api_records"

bronze = spark.read.format("delta").load(BRONZE_TABLE)

# Deduplicate: latest ingestion wins
w = Window.partitionBy("id").orderBy(F.col("ingestion_date").desc())
silver = (bronze.withColumn("_rn", F.row_number().over(w))
          .filter("_rn = 1").drop("_rn")
          .filter(F.col("id").isNotNull())
          .withColumn("name", F.trim(F.col("name")))
          .withColumn("email", F.lower(F.trim(F.col("email"))))
          .withColumn("ingestion_date", F.to_date("ingestion_date")))

silver.write.format("delta").mode("overwrite").save(SILVER_TABLE)
print(f"Silver rows: {silver.count()}")
