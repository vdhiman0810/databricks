# Databricks notebook source
dbutils.widgets.text("env", "prod", "Environment")
dbutils.widgets.text("data_source", "sales_prod", "Data Source")
dbutils.widgets.text("catalog", "main", "Catalog")

env = dbutils.widgets.get("env")
data_source = dbutils.widgets.get("data_source")
catalog = dbutils.widgets.get("catalog")

print(f"Running GitHub OIDC notebook for environment: {env}")
print(f"Using source table: {catalog}.default.{data_source}")

data = [
    ("north", 1255.80),
    ("south", 1104.35),
    ("east", 1522.45),
    ("west", 1198.20),
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
