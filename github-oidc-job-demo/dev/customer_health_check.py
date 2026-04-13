# Databricks notebook source
dbutils.widgets.text("env", "dev", "Environment")
dbutils.widgets.text("quality_threshold", "0.95", "Quality Threshold")
dbutils.widgets.text("alert_email", "data-team@example.com", "Alert Email")

env = dbutils.widgets.get("env")
quality_threshold = float(dbutils.widgets.get("quality_threshold"))
alert_email = dbutils.widgets.get("alert_email")

print(f"Running customer health check in {env}")
print(f"Alert contact: {alert_email}")

sample_data = [
    ("cust-001", 0.98, "active"),
    ("cust-002", 0.92, "review"),
    ("cust-003", 0.97, "active"),
    ("cust-004", 0.88, "review"),
]

df = spark.createDataFrame(sample_data, ["customer_id", "quality_score", "status"])
df.createOrReplaceTempView("customer_health")

result_df = spark.sql(
    f"""
    SELECT
      customer_id,
      quality_score,
      status,
      CASE
        WHEN quality_score >= {quality_threshold} THEN 'pass'
        ELSE 'needs_attention'
      END AS quality_result
    FROM customer_health
    """
)

display(result_df)

failed_count = result_df.filter("quality_result = 'needs_attention'").count()
print(f"Records below threshold: {failed_count}")
