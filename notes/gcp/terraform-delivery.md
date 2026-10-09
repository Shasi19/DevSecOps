# GCP infrastructure delivery with Terraform

## 1. Repository and state model

Separate reusable modules from environment roots. Pin Terraform/provider versions, commit the dependency lock file, and review provider upgrades. State is sensitive operational data: use a controlled GCS backend with uniform access, encryption, versioning/retention suited to recovery, and state locking supported by the selected backend/version. Restrict backend IAM and audit access.

```text
infra/
  modules/
    project/
    network/
    cloud-run-service/
  environments/
    dev/
    prod/
      main.tf
      variables.tf
      outputs.tf
```

Keep credentials and secret payloads out of source, plans, outputs, and CI logs. Terraform `sensitive` flags redact some output but do not guarantee a secret is absent from state.

## 2. CI identity and delivery gates

Use Workload Identity Federation from the CI provider; constrain issuer claims and map only the expected protected repository/branch/environment. Separate plan and apply permissions where feasible. Require plan review and protected production approval. Do not allow pull-request code from forks to access state or cloud credentials.

```mermaid
flowchart LR
  PR[Pull request] --> CHECK[fmt + validate + scan]
  CHECK --> PLAN[Plan with read/plan identity]
  PLAN --> REVIEW[Review diff + policy]
  REVIEW --> APPROVE[Protected approval]
  APPROVE --> APPLY[Apply approved plan]
  APPLY --> VERIFY[Runtime verification]
```

Never blindly apply a stale saved plan after the underlying state/config changes. Regenerate/review plans when a run is superseded.

## 3. Deployment steps

```bash
terraform fmt -check -recursive
terraform init -lockfile=readonly
terraform validate
terraform plan -out=tfplan
terraform show tfplan
# Apply only through the approved deployment workflow.
terraform apply tfplan
```

Run `init` in a controlled environment; do not use `-backend=false` for production state. Review deletions/replacements and expected blast radius. Use policy-as-code/security scanning, but treat results as inputs to a contextual review.

## 4. Module and environment design

Expose typed inputs with validation, explicit outputs, and narrow resource ownership. Avoid modules that hide critical security choices or create excessively broad IAM. Separate prod state/account/project from non-prod when blast-radius isolation requires it. Do not depend on one huge root module to order unrelated teams' changes.

## 5. Drift, import, and recovery

When drift appears, identify whether it is emergency change, console edit, or provider normalization. Decide whether code should adopt or reverse it; do not automatically overwrite. Back up state before import/move operations; use `moved` blocks for address refactors when appropriate. `force-unlock` only after confirming the owning operation is dead and the lock ID is correct.

## Troubleshooting

**403 in plan/apply:** inspect active CI principal, federation claims, impersonation permission, project/resource scope, API enablement, and organization policy. **Unexpected replacement:** inspect provider schema/immutable fields and exact plan details. **Lock stuck:** verify no active apply before recovery. Never solve these with Owner or routine `-target`.

## Revision

Plan is a proposal; state maps resources; lock prevents concurrent state mutation; plan may contain secrets; backend access is privileged; drift is a decision; applying is a production change and needs controls.
