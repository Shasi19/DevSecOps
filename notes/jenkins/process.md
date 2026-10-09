# Jenkins pipeline lifecycle

## 1. Prepare controller and agents

Install Jenkins on a supported, patched platform; restrict UI/API ingress; configure SSO/MFA and role permissions; back up configuration and secrets securely. Install only required plugins and test updates in staging. Prefer ephemeral agents with distinct pools for untrusted PRs and protected releases. Controller should not build arbitrary repository code on its own host.

## 2. Configure source and trust

Create scoped SCM credentials/webhook; protect Jenkinsfile/shared-library changes with code review. For PR jobs, do not bind deployment credentials. Restrict script approval and plugin management. Use short-lived cloud identity from an isolated release agent where supported.

## 3. Build pipeline

Use a versioned Jenkinsfile with checkout, test, scan, package, publish, deploy, verify stages. Set timeouts, concurrency, artifact retention, workspace cleanup, and failure notifications. Build once and publish immutable digest plus test/scan evidence. Avoid shell interpolation of untrusted parameters.

## 4. Deploy and verify

Deploy a specific artifact to staging; run smoke/integration checks and observe SLOs. Require an authorized production approval and protected agent/credential scope. Promote the same artifact, verify health, and automatically halt later stages on failure. Keep rollback to prior digest available.

## 5. Operate and troubleshoot

Queued job: inspect labels, executor capacity, online state, cloud-agent provisioning. Checkout failure: SCM credential scope/network/host key/ref. Secret missing: credential scope/folder binding. Controller instability: disk, heap, plugin compatibility, queue, and agent load. Preserve logs safely without exposing secret values.

## 6. Recovery and lifecycle

Back up controller config, job definitions, plugin list, credentials store under approved encryption/access; test restore. Upgrade plugins/core in a staging controller and validate representative jobs. Rotate credentials, remove unused plugins/agents, review admin access, and decommission controller/agents with secret revocation and disk disposal.
