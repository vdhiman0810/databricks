# Azure Key Vault-backed secret scope example

This folder is the source marker for the Azure Key Vault-backed Databricks secret scope CI/CD workflow.

## Scope created

- Value from `DATABRICKS_KEYVAULT_SCOPE_NAME`

## Existing Azure Key Vault required

Configure these GitHub Environment variables before running the workflow:

- `AZURE_KEYVAULT_RESOURCE_ID`
- `AZURE_KEYVAULT_DNS_NAME`

## Important note

This workflow links Databricks to an existing Azure Key Vault. Actual secrets must be created and rotated in Azure Key Vault.
