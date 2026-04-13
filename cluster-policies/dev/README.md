# Cluster policy example

This folder contains the source-controlled Databricks compute policy definition used by the cluster policy CI/CD workflow.

## Policy file

- `shared-job-policy.json`

## Purpose

This sample policy creates a job-only compute policy with:

- Photon enabled
- Latest LTS runtime
- Restricted worker sizes
- Worker count guardrails
- Required governance tags
