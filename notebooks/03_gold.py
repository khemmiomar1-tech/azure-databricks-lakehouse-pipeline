# Databricks notebook source
# MAGIC %md
# MAGIC # 03 - Gold: incremental (MERGE) load for Power BI
# MAGIC Gold is loaded **incrementally**: only new or changed records are merged
# MAGIC into the Gold Delta table - the full table is never reloaded.

# COMMAND ----------

from delta.tables import DeltaTable
from pyspark.sql import functions as F

SILVER_TABLE = "/Volumes/lakehouse/silver/delta/api_records"
GOLD_PATH = "/Volumes/lakehouse/gold/delta/gold_api_records"

silver = spark.read.format("delta").load(SILVER_TABLE)
gold_batch = silver.select("id", "name", "email", "ingestion_date").withColumn("updated_at", F.current_timestamp())

if DeltaTable.isDeltaTable(spark, GOLD_PATH):
    # Incremental load: upsert on the business key
    (DeltaTable.forPath(spark, GOLD_PATH).alias("target")
     .merge(gold_batch.alias("source"), "target.id = source.id")
     .whenMatchedUpdateAll()
     .whenNotMatchedInsertAll()
     .execute())
else:
    # First run only: create the Gold table
    gold_batch.write.format("delta").save(GOLD_PATH)

print("Gold incremental load complete - expose this Delta table to Power BI.")
