-- Gold layer exposed to Power BI (Delta / Databricks SQL)

CREATE TABLE IF NOT EXISTS gold.gold_api_records (
    id           BIGINT,
    name         STRING,
    email        STRING,
    ingestion_date DATE,
    updated_at   TIMESTAMP  -- set at every incremental MERGE
) USING DELTA;

-- Example check: records updated by the latest incremental load
-- SELECT * FROM gold.gold_api_records WHERE updated_at >= current_date();
