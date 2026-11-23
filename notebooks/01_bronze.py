# Databricks notebook source
# MAGIC %md
# MAGIC # 01 - Bronze: ingest a public API into Delta Lake
# MAGIC Ingestion is orchestrated by Azure Data Factory (see `adf/pipeline.json`)
# MAGIC or Airflow; this notebook receives the raw JSON and lands it in Bronze.

# COMMAND ----------

from pyspark.sql import functions as F

API_LANDING = "/Volumes/lakehouse/bronze/landing/api"   # raw JSON dropped by ADF
BRONZE_TABLE = "/Volumes/lakehouse/bronze/delta/api_records"

raw = spark.read.option("multiline", True).json(API_LANDING)

bronze = (raw
          .withColumn("ingestion_date", F.current_date())
          .withColumn("source", F.lit("public_api")))

bronze.write.format("delta").mode("append").save(BRONZE_TABLE)
print(f"Bronze rows: {bronze.count()}")
