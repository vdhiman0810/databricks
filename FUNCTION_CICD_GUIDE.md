# Databricks Function CI/CD Guide

## Goal

Create or update a SQL function in the existing `tennis` schema from GitHub Actions by using Databricks OIDC authentication and serverless SQL compute.

## Files

- `.github/workflows/databricks-function-cicd.yml`
- `sql/functions/tennis/get_player_tier.sql`

## What this workflow does

1. Authenticates to Databricks using GitHub OIDC.
2. Starts an existing serverless SQL warehouse.
3. Executes the function SQL from the repository through the Databricks SQL Statement Execution API.
4. Verifies the deployed function with `DESCRIBE FUNCTION EXTENDED`.

## GitHub environment setup

Use your `dev` GitHub Environment and configure:

- Variable: `DATABRICKS_HOST`
- Variable: `DATABRICKS_CLIENT_ID`
- Variable: `DATABRICKS_WAREHOUSE_ID`

## Example value

- `DATABRICKS_WAREHOUSE_ID=<existing serverless sql warehouse id>`

## Use case this solves

- Keeps shared SQL function logic in source control.
- Avoids manual edits in the Databricks SQL editor.
- Makes deployments repeatable with `CREATE OR REPLACE FUNCTION`.
- Lets you promote the same function definition across environments.
- Uses serverless SQL compute, so no job cluster management is required.

## Notes

- This workflow assumes the `main.tennis` schema already exists.
- The OIDC identity must have permission to use the target SQL warehouse and create functions in the target schema.
