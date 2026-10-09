# Argo CD GitOps application lifecycle

## 1. Prepare the Git source

Create an environment path/overlay with versioned manifests or Helm values. Ensure secrets are encrypted or fetched from an approved secret manager; never commit plaintext. CI validates schema, policy, rendered diff, image digest, and security checks. Protect the branch/tag and require review for deployment paths.

## 2. Install and secure Argo CD

Use supported version, SSO/RBAC, TLS, network restrictions, admin credential rotation, and monitored controller/repo-server capacity. Register only required clusters and repositories with least privilege. Keep repository credentials and cluster credentials out of broadly readable namespaces.

## 3. Define AppProject boundary

Allowlist source repos, destination clusters/namespaces, and resource kinds. Avoid wildcard projects for tenant workloads. Use a test app to verify a forbidden repo/destination/kind is rejected.

## 4. Register and synchronize Application

Set repo URL, revision, path, project, destination, and sync policy. Start with manual sync in a sandbox; review rendered/live diff; synchronize; check resource health and application SLO. Introduce auto-sync/self-heal after ownership and drift semantics are understood. Keep prune disabled until ownership/deletion safeguards are established.

## 5. Operate drift and rollback

For OutOfSync, inspect diff and identify manual change/controller mutation. Fix desired state in Git, not by repeated live edits. For bad release, revert the Git commit or deploy the previous immutable digest through a reviewed change; verify data/schema compatibility. Monitor sync, health, reconciliation errors, and repo-server latency.

## 6. Delete safely

Remove Application only after deciding resource finalizer/prune behavior and confirming ownership. Inspect PVCs, load balancers, DNS, and external resources. Revoke repo/cluster access when no longer needed. Never delete shared cluster namespace/resources from an app cleanup without ownership proof.
