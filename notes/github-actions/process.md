# GitHub Actions secure CI/CD process

## 1. Define trust and event model

Decide which events run for branches, tags, releases, and forks. Treat PR code as untrusted. Do not use privileged `pull_request_target` to execute checked-out fork code. Add path filters only if they cannot skip required security checks.

## 2. Add a validation workflow

Create `.github/workflows/ci.yml`. Set minimal `permissions` at workflow level, explicit job permissions, runner labels, timeouts, concurrency, and dependency setup. Pin actions according to organizational policy; validate action SHA and update through reviewed dependency automation. Run tests/lint/secret and dependency checks without deployment credentials.

## 3. Produce and promote artifact

Build once from a trusted commit; scan; generate provenance/SBOM as required; publish immutable digest; store run/commit metadata. A later environment deploys that same digest. Cache dependencies only as untrusted performance data, not as an artifact of record.

## 4. Configure production identity and gate

Use GitHub OIDC with cloud trust conditions for repository, branch, environment, and audience. Protect the environment with required reviewers and branch/tag rules. Give the deploy job only required token scopes and cloud actions. Verify fork PR cannot receive environment secrets or federated cloud role.

## 5. Verify and rollback

Wait for health checks and SLO signals after deployment; halt promotion on error/latency regression. Roll back to a known-good immutable artifact with an explicit approval/automation policy. Record deployment and outcome.

## Troubleshooting checklist

No run: event/branch/path filters, fork policy, YAML location. Job pending: runner labels/capacity. OIDC denied: issuer, audience, subject claims, environment and role trust. Artifact missing: job `needs`, name/run ID, retention. Secret visible: revoke immediately; logs and masks cannot undo exposure.
