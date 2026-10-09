# GitLab project-to-deployment process

## 1. Establish project controls

Choose group/project visibility; configure members/roles, protected default branch, merge-request approvals, CODEOWNERS/approval rules, required pipeline success, and release/tag protection. Protect CI config and shared components. Inventory runners and their privileged modes.

## 2. Design the pipeline DAG

Add `.gitlab-ci.yml` with stages/jobs, narrow `rules`, pinned base image, explicit timeout, and artifact retention. Validate merge requests using no production secrets. Use cache only for disposable dependencies; artifacts carry build output. Use `needs` for explicit dependencies and avoid building the production artifact twice.

## 3. Isolate runner trust

Use ephemeral isolated runners for untrusted work; keep protected deployment runners separate. Do not enable privileged Docker or mount host sockets for arbitrary project code. Patch runner hosts and restrict network egress. Ensure fork and merge-request pipeline settings do not expose protected variables.

## 4. Promote through environments

Build and scan a single immutable artifact; capture digest/SBOM and commit. Deploy to staging; run smoke and SLO checks. Use protected production environment, approval, and short-lived OIDC/cloud identity. Verify target and rollback artifact; record deployment.

## 5. Diagnose pipeline failures

- Job absent: inspect pipeline source, `rules`, workflow rules, branch and variables.
- Job pending: runner scope/tags/protected eligibility/capacity.
- Artifact absent: `needs`/dependencies, producer status, artifact path and expiry.
- Secret missing/available unexpectedly: variable scope/protection/environment and fork trust.
- Runner compromise concern: disable runner, revoke its credentials, isolate host, inspect jobs/logs and rotate reachable secrets.

## 6. Release and cleanup

Tag only a reviewed commit; use release notes and artifact digest. Remove expired artifacts/caches per retention, rotate tokens, review group membership and runner registration, and retire runners securely.
