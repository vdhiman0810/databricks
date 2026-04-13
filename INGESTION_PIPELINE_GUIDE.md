# Ingestion Pipeline Use Case

## Goal

Build a simple CI/CD-driven ingestion pipeline in GitHub that pushes changes to Databricks and runs automatically.

## Use case

This demo ingests a sample customer orders CSV from the GitHub repository, loads it into Databricks as a bronze layer, applies a small transformation to create a silver layer, and runs the pipeline whenever the notebook or source file changes.

## Files

- `.github/workflows/databricks-ingestion-cicd.yml`
- `pipelines/ingestion/dev/01_ingest_customer_orders.py`
- `data/ingestion/dev/customer_orders.csv`

## Flow

1. A change is pushed to `main` in either the pipeline notebook or the sample input file.
2. GitHub Actions authenticates to Databricks using OIDC.
3. The workflow uploads the sample CSV to `dbfs:/tmp/github-ingestion/dev/raw/customer_orders.csv`.
4. The workflow imports the notebook to `/Shared/pipelines/ingestion/dev/01_ingest_customer_orders`.
5. The workflow creates or updates the Databricks job `github-oidc-ingestion-dev`.
6. The workflow triggers the job.
7. The Databricks notebook reads the CSV, writes bronze output, then writes silver output.

## Step-by-step setup

1. Create a GitHub Environment named `dev`.
2. Add these environment variables in GitHub:
   - `DATABRICKS_HOST`
   - `DATABRICKS_CLIENT_ID`
3. Ensure your Databricks federated service principal allows the GitHub subject:
   - `repo:<org>/<repo>:environment:dev`
4. Push this repository to GitHub.
5. Open GitHub Actions and run `Databricks Ingestion CI/CD`, or push a change to one of the watched files.
6. After the workflow runs, check Databricks:
   - Notebook path: `/Shared/pipelines/ingestion/dev/01_ingest_customer_orders`
   - Job name: `github-oidc-ingestion-dev`
   - Raw file: `dbfs:/tmp/github-ingestion/dev/raw/customer_orders.csv`
   - Bronze output: `dbfs:/tmp/github-ingestion/dev/output/bronze`
   - Silver output: `dbfs:/tmp/github-ingestion/dev/output/silver`

## How to extend it

- Add `qa` and `prod` folders with separate GitHub Environments.
- Replace the sample CSV with files from a real landing area or volume.
- Replace DBFS demo paths with Unity Catalog volumes for production.
- Add data quality checks and notifications.
