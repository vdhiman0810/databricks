# Databricks notebook source
dbutils.widgets.text("env", "dev", "Environment")
dbutils.widgets.text("data_source", "sales_dev", "Data Source")
dbutils.widgets.text("catalog", "main", "Catalog")

env = dbutils.widgets.get("env")
data_source = dbutils.widgets.get("data_source")
catalog = dbutils.widgets.get("catalog")

print(f"Running GitHub OIDC notebook for environment: {env}")
print(f"Using source table: {catalog}.default.{data_source}")

data = [
    ("north", 1200.50),
    ("south", 980.25),
    ("east", 1430.10),
    ("west", 1115.75),
]

df = spark.createDataFrame(data, ["region", "sales_amount"])
df.createOrReplaceTempView("regional_sales")

summary_df = spark.sql(
    """
    SELECT
      region,
      sales_amount,
      CASE
        WHEN sales_amount >= 1200 THEN 'above_target'
        ELSE 'monitor'
      END AS status
    FROM regional_sales
    """
)

display(summary_df)
print(f"Notebook completed successfully for {env}")
