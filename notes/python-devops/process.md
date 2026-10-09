# Python DevOps automation lifecycle

## 1. Create an isolated project

Choose supported Python version, create virtual environment, declare dependencies, lock transitive versions/hashes per organization policy, and define CLI contract. Separate business logic from cloud/API/subprocess boundaries. Add type hints and documented exit codes.

## 2. Implement input and identity boundaries

Parse args with `argparse`; validate paths, URLs, identifiers, ranges, and environment. Use workload identity/secret manager; never log token/header/body. Use standard TLS verification. Treat API/JSON, subprocess output, and model/tool responses as untrusted; validate schemas.

## 3. Bound I/O and retries

Set connect/read/subprocess timeouts. Check HTTP status and response schema. Retry only selected transient errors with bounded exponential backoff/jitter and `Retry-After`; ensure operation is idempotent or uses idempotency key. Return explicit failure, not success-shaped defaults.

## 4. Test

Unit-test pure logic; mock API/subprocess boundary for deterministic errors; integration-test against sandbox service; test timeout, 401/403, 429/5xx, malformed data, partial completion, and duplicate execution. Add static typing/lint/dependency/security checks to CI.

## 5. Package and deploy

Build reproducibly; scan and publish immutable wheel/container; run as least-privilege identity with resource limits; externalize config/secrets. Add structured logs/metrics with redaction, owner, and runbook. Pin the artifact digest/version for rollback.

## 6. Operate and retire

Monitor invocation count, duration, failure class, retries, and downstream quota. On failure capture correlation/request IDs without sensitive content. Rotate credentials/revoke identity and remove schedules, artifacts, and permissions when retiring the automation.
