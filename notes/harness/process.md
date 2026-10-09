# Harness delivery pipeline lifecycle

## 1. Model the service and environment

Identify source repo, build artifact, registry, deployment target, owner, and service SLO. Create a service definition and environment/infrastructure mapping that reflects the actual deployment boundary. Do not reuse production connectors in development pipelines unnecessarily.

## 2. Establish connector and delegate trust

Create narrowly scoped connectors for source, registry, cloud, and cluster. Store credentials in approved secret management; prefer short-lived federation. Install delegates in the network segment that must reach targets, with least privilege, egress restrictions, upgrade/health monitoring, and capacity. Protect pipeline/template edit access.

## 3. Build a pipeline

Define stages: validate/test → build → scan → publish immutable artifact → deploy staging → verify → production approval → deploy/verify. Set input validation, timeout, retry class, concurrency, artifacts, and failure strategy. Build once and record digest/commit/provenance. Reusable templates should be versioned and reviewed.

## 4. Verify and promote

In staging, run smoke/integration checks and compare error/latency signals to baseline. Promotion uses the same artifact digest. Gate production with authorized approver and protected environment; verify actual workload readiness, not just API acceptance. Define rollback to previous known-good digest.

## 5. Troubleshoot

Pipeline queued: delegate capacity, selector, execution queue. Connector error: auth expiry/scope, endpoint/DNS/TLS. Deploy API succeeds but service bad: health check, runtime logs, dependency access, traffic shift. Repeated step: inspect retry semantics and idempotency; do not retry migration/non-idempotent step blindly.

## 6. Operate and retire

Monitor pipeline duration/failure/deployment success, delegate health, connector expiry, and artifact retention. Rotate credentials, review template/connector access, upgrade delegates in rings, and remove unused integrations. Revoke identity before decommissioning a delegate or service.
