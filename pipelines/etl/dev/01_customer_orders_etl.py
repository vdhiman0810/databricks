# Databricks notebook source
from pyspark.sql.functions import col, current_timestamp, sum as spark_sum, to_date, trim, upper

dbutils.widgets.text(
    "input_path",
    "dbfs:/Volumes/test_databricks/tennis/tennis_volume/etl/raw/customer_orders_raw.csv",
    "Input Path",
)
dbutils.widgets.text(
    "output_root",
    "dbfs:/Volumes/test_databricks/tennis/tennis_volume/etl/output",
    "Output Root",
)
dbutils.widgets.text("pipeline_name", "customer_orders_etl_demo", "Pipeline Name")

input_path = dbutils.widgets.get("input_path")
output_root = dbutils.widgets.get("output_root")
pipeline_name = dbutils.widgets.get("pipeline_name")

bronze_path = f"{output_root}/bronze"
silver_path = f"{output_root}/silver"
gold_path = f"{output_root}/gold"

print(f"Starting ETL pipeline: {pipeline_name}")
print(f"Extract source: {input_path}")

# Extract
raw_df = (
    spark.read
    .option("header", "true")
    .option("inferSchema", "true")
    .csv(input_path)
)

bronze_df = raw_df.withColumn("ingestion_timestamp", current_timestamp())

# Transform
silver_df = (
    bronze_df
    .withColumn("customer_id", upper(trim(col("customer_id"))))
    .withColumn("product_name", trim(col("product_name")))
    .withColumn("order_date", to_date("order_date"))
    .withColumn("gross_amount", col("quantity") * col("unit_price"))
    .filter(col("quantity") > 0)
    .dropDuplicates(["order_id"])
)

gold_df = (
    silver_df.groupBy("customer_id")
    .agg(
        spark_sum("gross_amount").alias("total_revenue"),
        spark_sum("quantity").alias("total_units")
    )
    .orderBy(col("total_revenue").desc())
)

# Load
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

(
    gold_df.write
    .format("delta")
    .mode("overwrite")
    .save(gold_path)
)

print(f"Bronze path: {bronze_path}")
print(f"Silver path: {silver_path}")
print(f"Gold path: {gold_path}")
print(f"Rows extracted: {raw_df.count()}")
print(f"Rows transformed: {silver_df.count()}")
print(f"Rows loaded to gold: {gold_df.count()}")

display(gold_df)
