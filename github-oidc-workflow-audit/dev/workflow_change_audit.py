# Databricks notebook source
dbutils.widgets.text("trigger_source", "github_workflow_change", "Trigger Source")
dbutils.widgets.text("branch", "main", "Branch")
dbutils.widgets.text("commit_sha", "local-test", "Commit SHA")

trigger_source = dbutils.widgets.get("trigger_source")
branch = dbutils.widgets.get("branch")
commit_sha = dbutils.widgets.get("commit_sha")

print(f"Trigger source: {trigger_source}")
print(f"Branch: {branch}")
print(f"Commit SHA: {commit_sha}")

events = [
    ("workflow_file_changed", branch, commit_sha, "ready"),
    ("job_triggered", branch, commit_sha, "success"),
]

df = spark.createDataFrame(events, ["event_name", "branch", "commit_sha", "status"])
display(df)

summary_df = spark.sql(
    """
    SELECT status, COUNT(*) AS total
    FROM values
      ('workflow_file_changed', 'ready'),
      ('job_triggered', 'success')
    AS audit(event_name, status)
    GROUP BY status
    """
)

display(summary_df)
