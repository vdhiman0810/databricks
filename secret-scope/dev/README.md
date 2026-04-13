# Databricks-backed secret scope example

This folder is the source marker for the Databricks-backed secret scope CI/CD workflow.

## Scope created

- `github-oidc-demo-scope-dev`

## Optional sample secret

If the GitHub environment secret `DATABRICKS_SAMPLE_SECRET_VALUE` is configured, the workflow creates:

- scope: `github-oidc-demo-scope-dev`
- key: `sample-api-token`

## Optional ACL grant

If the GitHub environment variable `DATABRICKS_SECRET_SCOPE_PRINCIPAL` is configured, the workflow grants:

- principal: value of `DATABRICKS_SECRET_SCOPE_PRINCIPAL`
- permission: `READ`
