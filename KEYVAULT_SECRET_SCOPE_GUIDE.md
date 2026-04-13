# Azure Key Vault-backed Secret Scope Guide

## Goal

Create a Databricks secret scope that points to an already existing Azure Key Vault by using GitHub Actions with Databricks OIDC authentication.

## Files

- `.github/workflows/databricks-keyvault-secret-scope-cicd.yml`
- `secret-scope-keyvault/dev/README.md`

## What this workflow does

1. Authenticates to Databricks using GitHub OIDC.
2. Validates that the scope name, Azure Key Vault resource ID, and Azure Key Vault DNS name are configured.
3. Checks whether the Databricks secret scope already exists.
4. Creates the scope as an Azure Key Vault-backed scope if it does not exist.
5. Optionally grants a Databricks ACL on the scope.
6. Verifies the scope with Databricks CLI.

## Important behavior

- This workflow creates a Databricks secret scope backed by an existing Azure Key Vault.
- The scope is a read-only interface from Databricks to Azure Key Vault.
- You must create or update the actual secret values in Azure Key Vault, not with `databricks secrets put-secret`.

## GitHub environment setup

Use your `dev` GitHub Environment and configure:

- Variable: `DATABRICKS_HOST`
- Variable: `DATABRICKS_CLIENT_ID`
- Variable: `DATABRICKS_KEYVAULT_SCOPE_NAME`
- Variable: `AZURE_KEYVAULT_RESOURCE_ID`
- Variable: `AZURE_KEYVAULT_DNS_NAME`
- Optional variable: `DATABRICKS_SECRET_SCOPE_PRINCIPAL`

## Example values

- `DATABRICKS_KEYVAULT_SCOPE_NAME=github-oidc-akv-scope-dev`
- `AZURE_KEYVAULT_RESOURCE_ID=/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.KeyVault/vaults/<vault-name>`
- `AZURE_KEYVAULT_DNS_NAME=https://<vault-name>.vault.azure.net/`

## Notes

- The identity creating the scope needs permission to create Azure Key Vault-backed scopes for that vault.
- `DATABRICKS_SECRET_SCOPE_PRINCIPAL` can be a group name, user email, or service principal application ID.
- The workflow is idempotent for scope creation.
