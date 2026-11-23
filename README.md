# Azure + Databricks Lakehouse Pipeline

A personal Data Engineering project: an end-to-end **ETL/ELT Lakehouse
pipeline** on Azure and Databricks, following the same architecture I used
in my UM6P internship - public API in, Power BI-ready Gold tables out.

## Architecture

```
Public API --(Azure Data Factory / Airflow)--> Landing (raw JSON)
           --(Databricks notebook 01)-------> Bronze (Delta, raw + metadata)
           --(Databricks notebook 02)-------> Silver (dedup, clean, typed)
           --(Databricks notebook 03)-------> Gold (incremental MERGE)
           --(Power BI)---------------------> Dashboard on Gold tables
```

## Incremental loading - the key idea

The Gold notebook never reloads the whole table. It uses a Delta Lake
**MERGE** (upsert) on the business key: matched rows are updated, new rows
are inserted, untouched rows cost nothing. That is what makes a daily
pipeline fast and cheap as data grows.

## Contents

| Path | What it does |
|---|---|
| `adf/pipeline.json` | Azure Data Factory pipeline: Web activity -> Copy to landing -> 3 Databricks notebooks in sequence, daily trigger |
| `notebooks/01_bronze.py` | Land raw API JSON in Bronze Delta with ingestion metadata |
| `notebooks/02_silver.py` | Deduplication (latest ingestion wins), null handling, standardisation |
| `notebooks/03_gold.py` | Incremental MERGE load into the Gold Delta table |
| `sql/gold_tables.sql` | Gold table DDL |
| `powerbi/dax_measures.md` | DAX measures for the Power BI dashboard |

## Stack

Microsoft Azure (Data Factory, Databricks) - PySpark - Delta Lake -
Power BI / DAX - SQL

## Resume (Francais)

Projet personnel de pipeline ETL/ELT Lakehouse de bout en bout : ingestion
d'une API publique (Azure Data Factory / Airflow), transformations PySpark
sur Databricks en architecture Bronze / Silver / Gold (Delta Lake),
chargement incremental par MERGE, et exposition des tables Gold dans un
dashboard Power BI.

---
Omar Khemmi - Data Engineer - Casablanca, Morocco
