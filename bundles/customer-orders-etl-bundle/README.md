# Customer Orders ETL Asset Bundle

This is a small Databricks Asset Bundle example built from the existing customer orders ETL notebook in this repository.

## What it deploys

- One Databricks job: `customer-orders-etl-<target>`
- One task that runs:
  - `src/01_customer_orders_etl.py`

## Targets

- `dev`
- `prod`

## Example commands

Validate the bundle:

```bash
databricks bundle validate --target dev
```

Deploy the bundle:

```bash
databricks bundle deploy --target dev
```

Run the deployed job:

```bash
databricks bundle run customer_orders_etl_job --target dev
```

## What problem this solves

- Keeps job configuration in source control instead of only in the Databricks UI.
- Reduces deployment drift between development and production.
- Makes it easier to promote the same workload between environments.
- Packages notebook code and job definition together as one deployable unit.

## Notes

- The bundle includes its own copy of the ETL notebook under `src/` so bundle validation and deployment do not depend on cross-folder sync rules.
- Set `DATABRICKS_HOST` in your shell environment before running bundle commands. The bundle intentionally relies on CLI environment authentication instead of embedding the workspace host in `databricks.yml`.
- Authentication can use the same Databricks OIDC or profile-based setup you already use elsewhere.
