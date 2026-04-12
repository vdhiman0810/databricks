# Databricks notebook source
from pyspark.sql.functions import col, current_timestamp, to_date

dbutils.widgets.text("input_path", "dbfs:/tmp/github-ingestion/dev/raw/customer_orders.csv", "Input Path")
dbutils.widgets.text("output_root", "dbfs:/tmp/github-ingestion/dev/output", "Output Root")
dbutils.widgets.text("pipeline_name", "customer_orders_demo", "Pipeline Name")

input_path = dbutils.widgets.get("input_path")
output_root = dbutils.widgets.get("output_root")
pipeline_name = dbutils.widgets.get("pipeline_name")

bronze_path = f"{output_root}/bronze"
silver_path = f"{output_root}/silver"

print(f"Starting pipeline: {pipeline_name}")
print(f"Reading raw file from: {input_path}")

raw_df = (
    spark.read
    .option("header", "true")
    .option("inferSchema", "true")
    .csv(input_path)
)

bronze_df = (
    raw_df
    .withColumnRenamed("order_id", "order_id")
    .withColumn("ingestion_timestamp", current_timestamp())
)

silver_df = (
    bronze_df
    .withColumn("order_date", to_date("order_date"))
    .withColumn("gross_amount", col("quantity") * col("unit_price"))
    .dropDuplicates(["order_id"])
    .filter(col("quantity") > 0)
)

(
    bronze_df.write
    .format("delta")
    .mode("overwrite")
    .save(bronze_path)
)

(
    silver_df.write
    .format("delta")
    .mode("overwrite")
    .save(silver_path)
)

print(f"Bronze data written to: {bronze_path}")
print(f"Silver data written to: {silver_path}")
print(f"Rows ingested: {silver_df.count()}")

display(silver_df)
