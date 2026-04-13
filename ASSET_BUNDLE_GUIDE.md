# Databricks Asset Bundle Guide

## Goal

Provide one concrete Databricks Asset Bundle example in this repository so jobs can be defined, versioned, validated, and deployed as code.

## Files

- `bundles/customer-orders-etl-bundle/databricks.yml`
- `bundles/customer-orders-etl-bundle/resources/customer_orders_etl_job.yml`
- `bundles/customer-orders-etl-bundle/README.md`
- `.github/workflows/databricks-asset-bundle-cicd.yml`

## Example use case

This bundle packages the existing customer orders ETL notebook as a deployable Databricks job.

It helps when:

- a team wants the same job definition in `dev` and `prod`
- job settings should be reviewed in pull requests
- deployments should stop depending on manual clicks in the Databricks UI
- a project needs a repeatable deployment artifact for CI/CD

## What problem it solves

- Deployment drift: job definitions stay in Git instead of diverging across workspaces.
- Manual configuration errors: fewer hand-edited jobs in the UI.
- Poor portability: the job can be recreated from the repo in another environment.
- Harder release management: changes to notebooks and job wiring move together.

## Basic workflow

1. Update notebook code or bundle resource YAML in Git.
2. Run `databricks bundle validate`.
3. Run `databricks bundle deploy`.
4. Run `databricks bundle run` or trigger the deployed job from Databricks.

## CI/CD workflow

The repository also includes a GitHub Actions workflow:

- `.github/workflows/databricks-asset-bundle-cicd.yml`

It:

- authenticates to Databricks with GitHub OIDC
- validates the asset bundle
- deploys the bundle to the `dev` target

The bundle example intentionally relies on the Databricks CLI environment variables provided by the workflow, such as `DATABRICKS_HOST`, rather than trying to interpolate the host inside `databricks.yml`.
