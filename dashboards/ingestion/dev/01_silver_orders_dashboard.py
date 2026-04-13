# Databricks notebook source
from pyspark.sql.functions import col, count, date_format, round as spark_round, sum as spark_sum

dbutils.widgets.text(
    "silver_path",
    "dbfs:/Volumes/test_databricks/tennis/tennis_volume/output/silver",
    "Silver Path",
)

silver_path = dbutils.widgets.get("silver_path")

silver_df = spark.read.format("delta").load(silver_path)
silver_df.createOrReplaceTempView("silver_customer_orders")

print(f"Loaded silver data from: {silver_path}")
display(silver_df)

# COMMAND ----------

kpi_df = silver_df.agg(
    count("*").alias("total_orders"),
    spark_round(spark_sum("gross_amount"), 2).alias("total_revenue"),
    spark_round(spark_sum("quantity"), 0).alias("units_sold"),
)

display(kpi_df)

# COMMAND ----------

daily_sales_df = (
    silver_df.groupBy(date_format(col("order_date"), "yyyy-MM-dd").alias("order_day"))
    .agg(
        spark_round(spark_sum("gross_amount"), 2).alias("daily_revenue"),
        count("*").alias("daily_orders"),
    )
    .orderBy("order_day")
)

display(daily_sales_df)

# COMMAND ----------

product_sales_df = (
    silver_df.groupBy("product_name")
    .agg(
        spark_round(spark_sum("gross_amount"), 2).alias("revenue"),
        spark_sum("quantity").alias("units_sold"),
    )
    .orderBy(col("revenue").desc())
)

display(product_sales_df)

# COMMAND ----------

customer_sales_df = (
    silver_df.groupBy("customer_id")
    .agg(
        spark_round(spark_sum("gross_amount"), 2).alias("revenue"),
        count("*").alias("orders"),
    )
    .orderBy(col("revenue").desc())
)

display(customer_sales_df)

# COMMAND ----------

print("Suggested dashboard visuals:")
print("1. KPI cards from kpi_df")
print("2. Line chart from daily_sales_df using order_day vs daily_revenue")
print("3. Bar chart from product_sales_df using product_name vs revenue")
print("4. Table from customer_sales_df")
