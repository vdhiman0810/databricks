# Silver Dashboard Guide

## Goal

Build a dashboard on top of the silver output created by the ingestion pipeline.

## Files

- `.github/workflows/databricks-dashboard-deploy.yml`
- `dashboards/ingestion/dev/01_silver_orders_dashboard.py`

## What this dashboard shows

- Total orders
- Total revenue
- Units sold
- Daily revenue trend
- Revenue by product
- Revenue by customer

## Silver data source

The dashboard notebook reads from:

- `dbfs:/Volumes/test_databricks/tennis/tennis_volume/output/silver`

## How to use it

1. Push the dashboard notebook or run the workflow manually.
2. Open this notebook in Databricks:
   - `/Shared/dashboards/ingestion/dev/01_silver_orders_dashboard`
3. Run the notebook.
4. For each displayed result, use Databricks visualization options to create:
   - KPI cards from `kpi_df`
   - line chart from `daily_sales_df`
   - bar chart from `product_sales_df`
   - detail table from `customer_sales_df`
5. Save the notebook or convert the query logic into an AI/BI dashboard if you want a published dashboard experience.

## Why this approach

AI/BI dashboards are the preferred Databricks dashboard type, but they usually need an interactive authoring step or a serialized dashboard definition tied to a SQL warehouse. This notebook-based dashboard is the fastest working starting point from your CI/CD repo.
