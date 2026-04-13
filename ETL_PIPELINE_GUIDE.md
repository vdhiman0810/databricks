# ETL Pipeline Guide

## Goal

Build a simple end-to-end ETL pipeline with GitHub CI/CD and Databricks.

## Files

- `.github/workflows/databricks-etl-cicd.yml`
- `pipelines/etl/dev/01_customer_orders_etl.py`
- `data/etl/dev/customer_orders_raw.csv`

## What the ETL does

### Extract

- Reads a raw CSV file from a Unity Catalog volume path.

### Transform

- Trims and standardizes customer and product fields
- Converts `order_date` to a date
- Calculates `gross_amount`
- Removes duplicate `order_id` values
- Filters out invalid rows where quantity is not positive

### Load

- Writes bronze Delta data
- Writes silver Delta data
- Writes gold Delta data aggregated by customer

## Paths

- Raw input: `dbfs:/Volumes/test_databricks/tennis/tennis_volume/etl/raw/customer_orders_raw.csv`
- Bronze output: `dbfs:/Volumes/test_databricks/tennis/tennis_volume/etl/output/bronze`
- Silver output: `dbfs:/Volumes/test_databricks/tennis/tennis_volume/etl/output/silver`
- Gold output: `dbfs:/Volumes/test_databricks/tennis/tennis_volume/etl/output/gold`

## CI/CD flow

1. A change is pushed to the ETL notebook, source data, or workflow.
2. GitHub Actions authenticates to Databricks using OIDC.
3. The raw CSV is uploaded to the volume path.
4. The ETL notebook is deployed to the Databricks workspace.
5. A Databricks job named `github-oidc-etl-dev` is created or updated.
6. The job is triggered.
7. Databricks executes extract, transform, and load end to end.

## How to validate

After the workflow runs:

- open `/Shared/pipelines/etl/dev/01_customer_orders_etl`
- verify the Databricks job `github-oidc-etl-dev`
- inspect the Delta outputs under the bronze, silver, and gold paths

## How to extend

- Add data quality tests before writing silver
- Write to Unity Catalog managed tables instead of only Delta paths
- Add separate `qa` and `prod` environments
- Add notifications and SLA checks
