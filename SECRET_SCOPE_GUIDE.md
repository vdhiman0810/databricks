# Databricks-backed Secret Scope Guide

## Goal

Create a Databricks-backed secret scope from GitHub Actions using Databricks OIDC authentication.

## Files

- `.github/workflows/databricks-secret-scope-cicd.yml`
- `secret-scope/dev/README.md`

## What this workflow does

1. Authenticates to Databricks using GitHub OIDC.
2. Checks whether a secret scope already exists.
3. Creates the scope if it does not exist.
4. Optionally adds a sample secret from GitHub Secrets.
5. Optionally grants ACLs on the scope.
6. Verifies the scope and keys with Databricks CLI.

## Important Databricks behavior

The CLI command:

- `databricks secrets create-scope <scope-name>`

creates a Databricks-backed secret scope by default. Databricks docs describe secret scopes as stored in an encrypted database owned and managed by Databricks. Sources:

- [Secret management](https://docs.databricks.com/aws/en/security/secrets/)
- [CLI secrets command group](https://docs.databricks.com/gcp/en/dev-tools/cli/reference/secrets-commands)

## GitHub environment setup

Use your `dev` GitHub Environment and configure:

- Variable: `DATABRICKS_HOST`
- Variable: `DATABRICKS_CLIENT_ID`
- Optional variable: `DATABRICKS_SECRET_SCOPE_PRINCIPAL`
- Optional secret: `DATABRICKS_SAMPLE_SECRET_VALUE`

## Example outcome

- Scope: `github-oidc-demo-scope-dev`
- Secret key: `sample-api-token`

## Notes

- `DATABRICKS_SECRET_SCOPE_PRINCIPAL` can be a group name, user email, or a service principal application ID.
- The workflow is idempotent for scope creation.
- Secret values should come from GitHub Secrets, not from the repository.
