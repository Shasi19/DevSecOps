# Terraform infrastructure change process

## 1. Bootstrap state safely

Use a dedicated backend bucket/account with encryption, versioning, access logging, least-privilege IAM, and locking supported by the chosen backend/version. Restrict state access because it can contain credentials and sensitive attributes. Keep prod and non-prod state separate where blast radius requires it. Protect backend bootstrap and recovery credentials.

## 2. Design and validate configuration

Pin Terraform/providers and commit lock file; use typed/validated inputs, locals, outputs, and reusable modules with clear interfaces. Keep secrets out of source and variables where possible; `sensitive` does not remove values from state. Run format, validate, lint, IaC/security scan, and policy checks.

## 3. Plan through CI

Authenticate CI using short-lived federation. A PR identity should not access production state or apply permissions. Generate plan for the exact commit/environment, retain it securely for review, and summarize creates/updates/replacements/deletions and estimated risk/cost. Require code review and protected approval for production.

## 4. Apply and verify

Apply only an approved current plan under state lock. Capture actor, commit, plan artifact, state backend, and result. Verify API-side resource state and application health; reconcile outputs and cost tags. Plan/apply success does not prove service availability.

## 5. Drift/import/recovery

For drift, determine whether to adopt or revert the out-of-band change; update code/state through reviewed workflow. For import/move, back up state, confirm exact remote object/address, and use import/moved-block procedure; plan immediately afterward. Never force-unlock while an apply may still be active.

## 6. Destroy

Use a separate explicit teardown plan in a disposable environment. Review every delete, stateful resource, snapshot, DNS entry, IAM dependency, and shared resource. Require approval; destroy only resources owned by that workspace. Confirm cloud inventory and billing after deletion.

## Troubleshooting

403: identity/scope/org policy; lock: identify active operation; unexpected replacement: immutable provider property/data impact; perpetual diff: normalization or drift; missing object: confirm backend/workspace before import. Avoid routine `-target`, broad permissions, and local-state-only recovery.
