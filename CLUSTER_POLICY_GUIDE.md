# Databricks Cluster Policy Guide

## Goal

Create or update a Databricks compute policy from GitHub Actions by using Databricks OIDC authentication.

## Files

- `.github/workflows/databricks-cluster-policy-cicd.yml`
- `cluster-policies/dev/shared-job-policy.json`

## What this workflow does

1. Authenticates to Databricks using GitHub OIDC.
2. Reads the policy JSON definition from the repository.
3. Checks whether a cluster policy with the configured name already exists.
4. Updates the existing policy if found.
5. Creates the policy if it does not already exist.
6. Verifies that the policy is available in Databricks.

## GitHub environment setup

Use your `dev` GitHub Environment and configure:

- Variable: `DATABRICKS_HOST`
- Variable: `DATABRICKS_CLIENT_ID`
- Variable: `DATABRICKS_CLUSTER_POLICY_NAME`
- Optional variable: `DATABRICKS_CLUSTER_POLICY_DESCRIPTION`
- Optional variable: `DATABRICKS_POLICY_MAX_CLUSTERS_PER_USER`

## Example values

- `DATABRICKS_CLUSTER_POLICY_NAME=shared-job-policy-dev`
- `DATABRICKS_CLUSTER_POLICY_DESCRIPTION=Managed by GitHub Actions for shared job compute`
- `DATABRICKS_POLICY_MAX_CLUSTERS_PER_USER=2`

## Notes

- This sample policy is job-only and blocks interactive notebook compute.
- The sample node types are Azure VM sizes. Adjust the `node_type_id` values if your workspace uses different SKUs.
- Updating a policy can affect existing compute governed by that policy.
