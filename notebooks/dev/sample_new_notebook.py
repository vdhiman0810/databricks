# Databricks notebook source
print("This notebook was auto-detected from the local repo notebooks folder.")

data = [
    ("alpha", 10),
    ("beta", 20),
    ("gamma", 30),
]

df = spark.createDataFrame(data, ["group_name", "metric_value"])
display(df)
