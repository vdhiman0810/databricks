# Databricks GitHub OIDC demo

This repository deploys a Databricks notebook to a selected `dev`, `qa`, or `prod` folder in a single Databricks workspace by using GitHub Actions with Databricks GitHub OIDC authentication.

## Repository structure

- `.github/workflows/databricks-oidc-deploy.yml`
- `.github/workflows/databricks-job-on-change.yml`
- `.github/workflows/databricks-workflow-change-trigger.yml`
- `.github/workflows/databricks-ingestion-cicd.yml`
- `.github/workflows/databricks-dashboard-deploy.yml`
- `.github/workflows/databricks-etl-cicd.yml`
- `.github/workflows/databricks-secret-scope-cicd.yml`
- `.github/workflows/databricks-keyvault-secret-scope-cicd.yml`
- `.github/workflows/databricks-cluster-policy-cicd.yml`
- `.github/env/dev.env.sample`
- `.github/env/qa.env.sample`
- `.github/env/prod.env.sample`
- `github-oidc-demo/dev/demo.py`
- `github-oidc-demo/qa/demo.py`
- `github-oidc-demo/prod/demo.py`
- `github-oidc-job-demo/dev/customer_health_check.py`
- `github-oidc-workflow-audit/dev/workflow_change_audit.py`
- `pipelines/ingestion/dev/01_ingest_customer_orders.py`
- `data/ingestion/dev/customer_orders.csv`
- `INGESTION_PIPELINE_GUIDE.md`
- `dashboards/ingestion/dev/01_silver_orders_dashboard.py`
- `DASHBOARD_GUIDE.md`
- `pipelines/etl/dev/01_customer_orders_etl.py`
- `data/etl/dev/customer_orders_raw.csv`
- `ETL_PIPELINE_GUIDE.md`
- `cluster-policies/dev/shared-job-policy.json`
- `CLUSTER_POLICY_GUIDE.md`
- `secret-scope/dev/README.md`
- `secret-scope-keyvault/dev/README.md`
- `SECRET_SCOPE_GUIDE.md`
- `KEYVAULT_SECRET_SCOPE_GUIDE.md`

## GitHub environment configuration

Create GitHub environments named `dev`, `qa`, and `prod`.

For each environment, add these variables:

- `DATABRICKS_HOST`
- `DATABRICKS_CLIENT_ID`
- `DATABRICKS_CLUSTER_ID`

Sample files are available here for reference only:

- `.github/env/dev.env.sample`
- `.github/env/qa.env.sample`
- `.github/env/prod.env.sample`

Typical values:

- `DATABRICKS_HOST=https://adb-xxxxxxxxxxxxxxxx.x.azuredatabricks.net`
- `DATABRICKS_CLIENT_ID=<Databricks federated service principal application id>`
- `DATABRICKS_CLUSTER_ID=<existing job cluster id>`

If you are testing with only one Databricks workspace, use the same `DATABRICKS_HOST` and `DATABRICKS_CLIENT_ID` values in all three GitHub environments.

Actual GitHub Environment variable location:

- GitHub repository
- `Settings`
- `Environments`
- Select `dev`, `qa`, or `prod`
- Add `DATABRICKS_HOST` and `DATABRICKS_CLIENT_ID` under environment variables

## Databricks federation policy reminder

If you use GitHub environments in the workflow, the subject in the Databricks federated credential policy usually maps to:

- `repo:<org>/<repo>:environment:dev`
- `repo:<org>/<repo>:environment:qa`
- `repo:<org>/<repo>:environment:prod`

## How to run

Go to GitHub Actions, start `Databricks OIDC Multi-Env Deploy`, and choose `dev`, `qa`, or `prod`.

The workflow deploys only the selected notebook:

- `dev` -> `/Shared/github-oidc-demo/dev/demo`
- `qa` -> `/Shared/github-oidc-demo/qa/demo`
- `prod` -> `/Shared/github-oidc-demo/prod/demo`

After the notebook is imported, the workflow also creates or updates a Databricks job named:

- `github-oidc-demo-dev`
- `github-oidc-demo-qa`
- `github-oidc-demo-prod`

The job uses the environment's `DATABRICKS_CLUSTER_ID` and is triggered immediately with `databricks jobs run-now`.

## New auto-trigger example

There is also a separate workflow for a new use case from scratch:

- Workflow: `.github/workflows/databricks-job-on-change.yml`
- Notebook folder: `notebooks/dev/`
- Example notebook: `notebooks/dev/sample_new_notebook.py`
- Databricks job naming pattern: `github-oidc-notebook-dev-<notebook-name>`

This workflow triggers automatically on pushes to:

- `notebooks/dev/**`

It detects changed notebooks in the local repo, imports each notebook to Databricks, creates or updates a job for each one, and triggers the run in the `dev` GitHub Environment.

This notebook auto-deploy workflow is configured to use Databricks serverless compute for notebook jobs, so it does not require `DATABRICKS_CLUSTER_ID`.

## Trigger Databricks on workflow changes

There is a separate workflow that is fully dedicated to workflow-file changes:

- Workflow: `.github/workflows/databricks-workflow-change-trigger.yml`
- Notebook: `github-oidc-workflow-audit/dev/workflow_change_audit.py`
- Databricks job name: `github-oidc-workflow-change-audit-dev`

This workflow triggers when files under `.github/workflows/**` change on `main`.

It creates or updates a Databricks job and then runs it, passing:

- Git branch name
- Git commit SHA
- Trigger source

This workflow is also configured for Databricks serverless compute, so it does not require `DATABRICKS_CLUSTER_ID`.

## End-to-end ingestion pipeline example

There is also a complete ingestion pipeline sample:

- Workflow: `.github/workflows/databricks-ingestion-cicd.yml`
- Notebook: `pipelines/ingestion/dev/01_ingest_customer_orders.py`
- Sample source file: `data/ingestion/dev/customer_orders.csv`
- Guide: `INGESTION_PIPELINE_GUIDE.md`

This example shows a CI/CD flow where GitHub pushes both code and sample data into Databricks, creates or updates a job, and runs the ingestion pipeline automatically.

## Silver dashboard example

There is also a dashboard-ready notebook for the silver layer:

- Workflow: `.github/workflows/databricks-dashboard-deploy.yml`
- Notebook: `dashboards/ingestion/dev/01_silver_orders_dashboard.py`
- Guide: `DASHBOARD_GUIDE.md`

This deploys a notebook that reads the silver Delta output and produces KPI, trend, product, and customer-level views suitable for building a Databricks dashboard.

## End-to-end ETL example

There is also a full ETL example:

- Workflow: `.github/workflows/databricks-etl-cicd.yml`
- Notebook: `pipelines/etl/dev/01_customer_orders_etl.py`
- Sample raw data: `data/etl/dev/customer_orders_raw.csv`
- Guide: `ETL_PIPELINE_GUIDE.md`

This example covers extract, transform, and load end to end, writing bronze, silver, and gold Delta outputs in Databricks.

## Databricks-backed secret scope example

There is also a secret scope CI/CD example:

- Workflow: `.github/workflows/databricks-secret-scope-cicd.yml`
- Marker folder: `secret-scope/dev/`
- Guide: `SECRET_SCOPE_GUIDE.md`

This workflow creates a Databricks-backed secret scope, optionally adds a sample secret from GitHub Secrets, and can grant scope ACLs.

## Azure Key Vault-backed secret scope example

There is also a workflow for linking Databricks to an already existing Azure Key Vault:

- Workflow: `.github/workflows/databricks-keyvault-secret-scope-cicd.yml`
- Marker folder: `secret-scope-keyvault/dev/`
- Guide: `KEYVAULT_SECRET_SCOPE_GUIDE.md`

This workflow creates an Azure Key Vault-backed Databricks secret scope. The actual secret values continue to live in Azure Key Vault and must be managed there.

## Cluster policy CI/CD example

There is also a workflow for managing a Databricks compute policy from source control:

- Workflow: `.github/workflows/databricks-cluster-policy-cicd.yml`
- Policy definition: `cluster-policies/dev/shared-job-policy.json`
- Guide: `CLUSTER_POLICY_GUIDE.md`

This workflow creates or updates a Databricks job-only compute policy using the JSON definition stored in the repository.
